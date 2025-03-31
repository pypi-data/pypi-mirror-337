import pytest
import logging
from unittest.mock import patch

from log9er.logger import Logger, ErrorColorFormatter


def test_default_init():
    """Test creating a Logger with default parameters."""
    logger_obj = Logger("Logger")
    assert logger_obj.logger is not None
    assert logger_obj.logger.name == "Logger"


def test_existing_logger():
    """Test passing an existing Logger instance."""
    existing = logging.getLogger("existingLogger")
    logger_obj = Logger(logger=existing)
    # Should wrap the existing logger and ignore other init params
    assert logger_obj.logger is existing


def test_invalid_logger_type():
    """Test passing a non-Logger type to the logger parameter."""
    with pytest.raises(TypeError):
        Logger(logger="not_a_logger")


@patch("os.path.isdir", return_value=False)
def test_file_directory_not_found(mock_isdir):
    """Test that FileNotFoundError is raised if log is a file path and directory doesn't exist."""
    with pytest.raises(FileNotFoundError):
        Logger("Logger", log="non_existent_dir/mylog.log")


@patch("os.path.exists", return_value=False)
def test_syslog_not_supported(mock_exists):
    """Test that OSError is raised if 'syslog' is requested but '/dev/log' doesn't exist."""
    with pytest.raises(OSError):
        Logger("Logger", log="syslog")


def test_invalid_log_level_string():
    """Test that a ValueError is raised on an invalid log level string."""
    with pytest.raises(ValueError):
        Logger(level="FOO_LEVEL")


@patch("logging.Logger.debug")
@patch("logging.Logger.info")
@patch("logging.Logger.warning")
@patch("logging.Logger.error")
@patch("logging.Logger.fatal")
def test_log_method_levels(
    mock_fatal, mock_error, mock_warning, mock_info, mock_debug
):
    """
    Test that calling log() with various levels calls the correct logger method.
    """
    logger_obj = Logger("Logger")

    # Info-level log
    logger_obj.log("This is an info message", level=logging.INFO)
    mock_info.assert_called_with("This is an info message")

    # Warning-level log
    logger_obj.log("Warn here", level=logging.WARNING)
    mock_warning.assert_called_with("Warn here")

    # Error-level log
    logger_obj.log("Error here", level=logging.ERROR)
    mock_error.assert_called_with("Error here")

    # Fatal-level log
    logger_obj.log("Fatal here", level=logging.FATAL)
    mock_fatal.assert_called_with("Fatal here")

    # Debug-level log
    logger_obj.log("Debug info", level=logging.DEBUG)
    mock_debug.assert_called_with("Debug info")


@patch("logging.Logger.exception")
@patch("logging.Logger.error")
def test_log_exception_debug_true(mock_error, mock_exception):
    """
    Test that log() with exception=True and debug=True calls logger.exception(),
    including the message prefixed with "Exception:".
    """
    logger_obj = Logger("Logger", debug=True)
    logger_obj.log("An exception occurred", exception=True)

    mock_exception.assert_called_once_with("Exception: An exception occurred")
    mock_error.assert_not_called()


@patch("logging.Logger.exception")
@patch("logging.Logger.error")
def test_log_exception_debug_false(mock_error, mock_exception):
    """
    Test that log() with exception=True but debug=False calls logger.error()
    with "Exception:" but does not call logger.exception().
    """
    logger_obj = Logger("Logger", debug=False)
    logger_obj.log("Something went wrong", exception=True)

    mock_error.assert_called_once_with("Exception: Something went wrong")
    mock_exception.assert_not_called()


def test_error_color_formatter_no_color_for_info():
    """
    Test that ErrorColorFormatter does not color info-level logs.
    """
    formatter = ErrorColorFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=123,
        msg="Just info",
        args=(),
        exc_info=None
    )
    output = formatter.format(record)
    assert "Just info" in output
    # Ensure that no escape codes appear
    assert ErrorColorFormatter.BOLD_RED not in output


def test_error_color_formatter_error_colored():
    """
    Test that ErrorColorFormatter colors ERROR logs in bold red.
    """
    formatter = ErrorColorFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname=__file__,
        lineno=123,
        msg="Error message",
        args=(),
        exc_info=None
    )
    output = formatter.format(record)
    assert "Error message" in output
    assert ErrorColorFormatter.BOLD_RED in output
    assert ErrorColorFormatter.RESET in output
