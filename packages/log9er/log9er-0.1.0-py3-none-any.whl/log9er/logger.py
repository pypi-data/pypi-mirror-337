import os
import logging
from logging.handlers import RotatingFileHandler, SysLogHandler


class Logger(object):
    """A basic logger supporting stderr, syslog, and rotating local file logging.

    Attributes:
        debug (bool): If True, traceback is logged when `exception=True`.
        logger (logging.Logger | None): The underlying logger instance, if already provided
            or created in `__init__`.
    """

    debug : bool = False
    logger : logging.Logger | None = None

    # Default rotating file handler settings
    max_bytes : int = 10485760
    backup_count : int = 5

    level_map : dict[str, int] = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(
            self,
            name : str = "",
            log : str = "syslog",
            level : int | str = logging.INFO,
            debug : bool = False,
            propagate : bool = False,
            max_bytes : int | None = None,
            backup_count : int | None = None,
            logger : logging.Logger | None = None
    ):
        """Initializes the Logger.

        The `Logger` class provides a flexible interface for logging messages to various
        backends (such as syslog, file-based logging, or stderr) with customizable
        log levels. If an existing `logging.Logger` instance is provided, all other
        initialization parameters (except `debug`) are ignored.

        Args:
            name (str): The name to assign to the logger instance. Required unless an
                external `logger` is provided.
            log (str): The log output destination. For example, `"syslog"` or a file path.
                If `"stderr"`, logs go to standard output.
            level (int | str): The default logging level. Can be a string
                (e.g., `"INFO"`) or an integer constant from the `logging` module
                (e.g., `logging.INFO`).
            debug (bool): If True, enable traceback logging when `exception=True`.
            propagate (bool): Whether log records should propagate to the root logger.
                If True, the root logger also processes these messages (default: False).
            max_bytes (int | None): If provided, and if `log` is a file path, use as the
                `maxBytes` for the `RotatingFileHandler` (default: 10485760).
            backup_count (int | None): If provided, and if `log` is a file path, use as
                the `backup_count` for the `RotatingFileHandler` (default: 5).
            logger (logging.Logger | None): If provided, use this logger instance directly
                and ignore other arguments (except `debug`).

        Raises:
            TypeError: If `logger` is provided but is not an instance of `logging.Logger`.
            ValueError: If `level` is an invalid log level string.
            FileNotFoundError: If `log` is a file path and its directory does not exist.
            OSError: If `log="syslog"` but `/dev/log` is not available on this system.
        """

        self.debug = debug

        # Logger provided? Then ignore other arguments
        if logger is not None:
            if not isinstance(logger, logging.Logger):
                raise TypeError(
                    f"'logger' must be a 'logging.Logger' instance, not {type(logger)}"
                )

            self.logger = logger
            return

        # No logger provided, so 'name' is required
        if not name:
            raise ValueError("'name' is required unless an external 'logger' is provided")

        # Otherwise create a new logger from args
        if isinstance(max_bytes, int):
            self.max_bytes = max_bytes
        if isinstance(backup_count, int):
            self.backup_count = backup_count

        self._init_logger(name, log, level, propagate)

    def _init_logger(
        self,
        name: str,
        log: str,
        level: int | str,
        propagate: bool
    ) -> None:
        """
        Internal helper to create and configure a new logger.
        Raises FileNotFoundError, OSError, or ValueError if invalid arguments.
        """

        # If log is a file path, ensure the directory exists
        if log not in ["stderr", "syslog"]:
            dirpath = os.path.dirname(log)
            if not os.path.isdir(dirpath):
                raise FileNotFoundError(f"Log file directory not found: {dirpath}")

        # Check syslog support
        if log == "syslog" and not os.path.exists("/dev/log"):
            raise OSError("This system does not support 'syslog' logging.")

        # If level is a string, map it to a logging.* constant
        if isinstance(level, str):
            level = level.upper()
            if level not in self.level_map:
                raise ValueError(f"Invalid log level '{level}'")
            level = self.level_map[level]

        # Logger already has handlers? Then let sleeping dogs lie
        logger = logging.getLogger(name)
        if logger.hasHandlers():
            self.logger = logger
            return

        # OK safe to make the logger, now...
        logger.propagate = propagate
        logger.setLevel(level)

        datefmt = "%b %d %H:%M:%S"
        msgfmt = "%(asctime)s %(name)s[%(process)s]: [%(levelname)s] %(message)s"

        # Select a formatter
        if log == "stderr":
            formatter = ErrorColorFormatter(fmt=msgfmt, datefmt=datefmt)
        else:
            formatter = logging.Formatter(msgfmt, datefmt=datefmt)

        # Select a handler
        if log == "stderr":
            handler = logging.StreamHandler()
        elif log == "syslog":
            handler = SysLogHandler(address="/dev/log")
        else:
            # Rotating file
            handler = RotatingFileHandler(
                log, maxBytes=self.max_bytes, backupCount=self.max_bytes
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self.logger = logger

    def log(
        self,
        *msgs : str,
        level : int | str = logging.INFO,
        exception : bool = False,
        prefix : str | None = None
    ) -> None:
        """Logs one or more messages at the specified level.

        If multiple messages are passed, they are joined with a newline+tab ("\n\t").
        If `exception=True`, the messages are prefixed with "Exception:" and a traceback
        is logged if `debug=True`. If a `prefix` string is provided, it is inserted in
        square brackets before the message text.

        Args:
            *msgs (str): One or more strings to log, e.g. `"Hello"`, `"World"`.
            level (int | str): The log level (e.g., `logging.INFO` or `"INFO"`). Defaults
                to `logging.INFO`.
            exception (bool): If True, prefix with "Exception:" and log a traceback if
                `self.debug` is also True.
            prefix (str | None): Optional prefix label. If provided, the log message is
                prefixed with e.g. `"[myfunction] message"`.

        Returns:
            None
        """

        # Convert and join all msgs
        msg = "\n\t".join([str(m) for m in msgs])

        if exception:
            msg = f"Exception: {msg}"

        if prefix:
            msg = f"[{prefix}] {msg}"

        # If level is a string, map it to a logging.* constant
        if not isinstance(level, int) and not isinstance(level, str):
            raise ValueError(f"Invalid log level '{level}'. Must be `logging` level constant or string.")

        if isinstance(level, str):
            level = level.upper()
            if level not in self.level_map:
                raise ValueError(f"Invalid log level '{level}'")
            level = self.level_map[level]

        # If we're dealing with an exception and debug is enabled, log with traceback
        if exception and self.debug:
            # logger.exception() always logs at ERROR level + traceback
            self.logger.exception(msg)
            return

        # Otherwise, if exception=True but debug=False, just log as ERROR without traceback
        if exception:
            level = logging.ERROR

        # Log normally at the resolved level
        if level == logging.DEBUG:
            self.logger.debug(msg)
        elif level == logging.INFO:
            self.logger.info(msg)
        elif level == logging.WARNING:
            self.logger.warning(msg)
        elif level == logging.ERROR:
            self.logger.error(msg)
        elif level == logging.FATAL:
            self.logger.fatal(msg)
        else:
            self.logger.log(level, msg)


class ErrorColorFormatter(logging.Formatter):
    """A custom formatter that applies bold red color for ERROR or CRITICAL messages.

    Attributes:
        BOLD_RED (str): The ANSI escape sequence for bold red text.
        RESET (str): The ANSI escape sequence to reset color.
    """

    BOLD_RED = "\x1b[1;31m"
    RESET = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record.

        If the level is ERROR or CRITICAL, the message is colored in bold red.

        Args:
            record (logging.LogRecord): The record to format.

        Returns:
            str: The formatted log message, colored if needed.
        """

        log_msg = super().format(record)
        if record.levelno >= logging.ERROR:
            return f"{self.BOLD_RED}{log_msg}{self.RESET}"
        return log_msg
