"""Classes for setting up and formatting loggers.

Logician and related classes provide methods for setting up a logger with a console handler,
defining console color codes for use in the formatter to colorize messages by log level, and more.
"""

from __future__ import annotations

import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dsroot import Singleton

from logician.log_formatters import CustomFormatter, FileFormatter
from logician.log_metadata import LogLevel
from logician.time_aware_logger import TimeAwareLogger

# Default values for logger configuration
DEFAULT_LOGGER_NAME_ARG: str | None = None
DEFAULT_LEVEL_ARG: int | str = logging.INFO
DEFAULT_SIMPLE_ARG: bool = False
DEFAULT_SHOW_CONTEXT_ARG: bool = False
DEFAULT_COLOR_ARG: bool = True
DEFAULT_LOG_FILE_ARG: Path | None = None
DEFAULT_TIME_AWARE_ARG: bool = False


class Logger:
    """A powerful, colorful logger for Python applications. The logical choice for Python logging.

    Set up an easy local logger with a console handler. Logs at DEBUG level by default, but can be
    set to any level using the log_level parameter. Uses a custom formatter that includes the time,
    logger name, function name, and log message.

    Args:
        logger_name: The name of the logger. If None, the class or module name is used.
        level: The log level. Defaults to 'INFO'.
        simple: Use simple format that displays only the log message itself. Defaults to False.
        show_context: Show the class and function name in the log message. Defaults to False.
        color: Use color in the log output. Defaults to True.
        log_file: Path to a desired log file. Defaults to None, which means no file logging.
        time_aware: If True, returns a TimeAwareLogger instance. Defaults to False.

    Usage:
        from logician import Logger

        logger = Logger("MyClass")
        logger = Logger.get(self.__class__.__name__, simple=True)
    """

    @classmethod
    def get(
        cls,
        logger_name: str | None = DEFAULT_LOGGER_NAME_ARG,
        level: int | str = DEFAULT_LEVEL_ARG,
        simple: bool = DEFAULT_SIMPLE_ARG,
        show_context: bool = DEFAULT_SHOW_CONTEXT_ARG,
        color: bool = DEFAULT_COLOR_ARG,
        log_file: Path | None = DEFAULT_LOG_FILE_ARG,
        time_aware: bool = DEFAULT_TIME_AWARE_ARG,
    ) -> logging.Logger | TimeAwareLogger:
        """Set up a logger with the given name and log level.

        Args:
            logger_name: The name of the logger. If None, the class or module name is used.
            level: The log level. Defaults to 'INFO'.
            simple: Use simple format that displays only the log message itself. Defaults to False.
            show_context: Show the class and function name in the log message. Defaults to False.
            color: Use color in the log output. Defaults to True.
            log_file: Path to a desired log file. Defaults to None, which means no file logging.
            time_aware: If True, returns a TimeAwareLogger instance. Defaults to False.
        """
        logger = _LogicianImpl().get_logger(
            logger_name, level, simple, show_context, color, log_file
        )
        if time_aware:
            return TimeAwareLogger(logger)
        return logger

    def __new__(
        cls,
        logger_name: str | None = DEFAULT_LOGGER_NAME_ARG,
        level: int | str = DEFAULT_LEVEL_ARG,
        simple: bool = DEFAULT_SIMPLE_ARG,
        show_context: bool = DEFAULT_SHOW_CONTEXT_ARG,
        color: bool = DEFAULT_COLOR_ARG,
        log_file: Path | None = DEFAULT_LOG_FILE_ARG,
    ) -> logging.Logger:
        """Allow direct instantiation as an alternative to .get()."""
        return _LogicianImpl().get_logger(logger_name, level, simple, show_context, color, log_file)


class _LogicianImpl(metaclass=Singleton):
    def get_logger(
        self,
        logger_name: str | None = DEFAULT_LOGGER_NAME_ARG,
        level: int | str = "INFO",
        simple: bool = DEFAULT_SIMPLE_ARG,
        show_context: bool = DEFAULT_SHOW_CONTEXT_ARG,
        color: bool = DEFAULT_COLOR_ARG,
        log_file: Path | None = DEFAULT_LOG_FILE_ARG,
    ) -> logging.Logger:
        """Set up a logger with the given name and log level."""
        logger_name = _LogicianImpl().get_logger_name(logger_name)
        logger = logging.getLogger(logger_name)

        if not logger.handlers:
            log_level = LogLevel.get_level(level)
            logger.setLevel(log_level)

            log_formatter = CustomFormatter(simple=simple, color=color, show_context=show_context)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(log_formatter)
            console_handler.setLevel(log_level)
            logger.addHandler(console_handler)

            if log_file:
                self.add_file_handler(logger, log_file)

            logger.propagate = False

        return logger

    @staticmethod
    def get_logger_name(logger_name: str | None = None) -> str:
        """Generate a logger identifier based on the provided parameters and calling context."""
        if logger_name is not None:
            return logger_name

        import inspect

        # Try to get the calling frame
        frame = inspect.currentframe()
        if frame is not None:
            frame = frame.f_back  # get_logger's frame
            if frame is not None:
                frame = frame.f_back  # get_logger's caller's frame

        # If we have a valid frame, try to identify it
        if frame is not None:
            # Try to get class name first
            if "self" in frame.f_locals:
                return frame.f_locals["self"].__class__.__name__
            if "cls" in frame.f_locals:
                return frame.f_locals["cls"].__name__

            # Get the module name if we can't get the class name
            module = inspect.getmodule(frame)
            if module is not None and hasattr(module, "__name__"):
                return module.__name__.split(".")[-1]

            # Get the filename if we can't get the module name
            filename = frame.f_code.co_filename
            if filename:
                base_filename = Path(filename).name
                return Path(base_filename).stem

        # If we really can't find our place in the universe
        return "unknown"

    def add_file_handler(self, logger: logging.Logger, log_file: Path) -> None:
        """Add a file handler to the given logger.

        Args:
            logger: The logger to add the file handler to.
            log_file: The path to the log file.
        """
        formatter = FileFormatter()
        log_dir = Path(log_file).parent

        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        if not log_file.is_file():
            log_file.touch()

        file_handler = RotatingFileHandler(log_file, maxBytes=512 * 1024)
        file_handler.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
