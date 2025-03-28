"""
This module provides context managers for temporarily silencing output.

- Muffle: Context manager that temporarily silences output (alternative to stouputils.decorators.silent())
- LogToFile: Context manager to log to a file every calls to the print functions in stouputils.print

.. image:: https://raw.githubusercontent.com/Stoupy51/stouputils/refs/heads/main/assets/ctx_module.gif
  :alt: stouputils ctx examples
"""

# Imports
import os
import sys
from typing import IO, TextIO, Callable, Any
from .print import logging_to
from .io import super_open

# Context manager to temporarily silence output
class Muffle:
	""" Context manager that temporarily silences output.

	Alternative to stouputils.decorators.silent()
	
	Examples:
		>>> with Muffle():
		...     print("This will not be printed")
	"""
	def __init__(self, mute_stderr: bool = False) -> None:
		self.mute_stderr: bool = mute_stderr
		""" Attribute remembering if stderr should be muted """
		self.original_stdout: TextIO = sys.stdout
		""" Attribute remembering original stdout """
		self.original_stderr: TextIO = sys.stderr
		""" Attribute remembering original stderr """

	def __enter__(self) -> None:
		""" Enter context manager which redirects stdout and stderr to devnull """
		# Redirect stdout to devnull
		sys.stdout = open(os.devnull, "w")

		# Redirect stderr to devnull if needed
		if self.mute_stderr:
			sys.stderr = open(os.devnull, "w")

	def __exit__(self, exc_type: type[BaseException]|None, exc_val: BaseException|None, exc_tb: Any|None) -> None:
		""" Exit context manager which restores original stdout and stderr """
		# Restore original stdout
		sys.stdout.close()
		sys.stdout = self.original_stdout

		# Restore original stderr if needed
		if self.mute_stderr:
			sys.stderr.close()
			sys.stderr = self.original_stderr


# Context manager to log to a file
class LogToFile:
	""" Context manager to log to a file.

	This context manager allows you to temporarily log output to a file while still printing normally.
	The file will receive log messages without ANSI color codes.

	Args:
		path (str): Path to the log file
		mode (str): Mode to open the file in (default: "w")
		encoding (str): Encoding to use for the file (default: "utf-8")

	Examples:
		.. code-block:: python

			> import stouputils as stp
			> with stp.LogToFile("output.log"):
			>     stp.info("This will be logged to output.log and printed normally")
	"""
	def __init__(self, path: str, mode: str = "w", encoding: str = "utf-8") -> None:
		self.path: str = path
		""" Attribute remembering path to the log file """
		self.mode: str = mode
		""" Attribute remembering mode to open the file in """
		self.encoding: str = encoding
		""" Attribute remembering encoding to use for the file """
		self.file: IO[Any] = super_open(self.path, mode=self.mode, encoding=self.encoding)
		""" Attribute remembering opened file """

	def __enter__(self) -> None:
		""" Enter context manager which opens the log file and adds it to the logging_to list """
		# Add file to logging_to list
		logging_to.add(self.file)

	def __exit__(self, exc_type: type[BaseException]|None, exc_val: BaseException|None, exc_tb: Any|None) -> None:
		""" Exit context manager which closes the log file and removes it from the logging_to list """
		# Close file
		self.file.close()

		# Remove file from logging_to list
		logging_to.discard(self.file)
	
	@staticmethod
	def common(logs_folder: str, filepath: str, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
		""" Common code used at the beginning of a program to launch main function

		Args:
			logs_folder (str): Folder to store logs in
			filepath    (str): Path to the main function
			func        (Callable[..., Any]): Main function to launch
			*args       (tuple[Any, ...]): Arguments to pass to the main function
			**kwargs    (dict[str, Any]): Keyword arguments to pass to the main function
		Returns:
			Any: Return value of the main function
		
		Examples:
			>>> if __name__ == "__main__":
			...     LogToFile.common(f"{ROOT}/logs", __file__, main)
		"""
		# Import datetime
		from datetime import datetime

		# Build log file path
		file_basename: str = os.path.splitext(os.path.basename(filepath))[0]
		date_time: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
		date_str, time_str = date_time.split("_")
		log_filepath: str = f"{logs_folder}/{file_basename}/{date_str}/{time_str}.log"

		# Launch function with arguments if any
		with LogToFile(log_filepath):
			return func(*args, **kwargs)

