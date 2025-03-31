
# Table of Contents

-   [Introduction](#orgc3998f7)
    -   [Is Log9er For You?](#orgb98c5ce)
    -   [Features](#org24e260a)
-   [Installation](#org8b9bb4b)
-   [Usage](#org3609dcf)
    -   [Initialize Logger](#org4089f40)
    -   [Log Method](#orga19ad04)
-   [Authors](#orgb57b666)

**Log the same way, everywhere**


<a id="orgc3998f7"></a>

# Introduction

**Log9er** is a simple, opinionated Python `logging` wrapper class.

You can use it to normalize `logging` footprints across multiple projects, reducing boilerplate in development, and making it easier to create a uniform experience for log reading and parsing.


<a id="orgb98c5ce"></a>

## Is Log9er For You?

Log9er is tiny, because it replaces the standard Python library approach `logger.debug(m)` with `logger.log(m, level=logging.DEBUG)`.

That's really the only big difference: It's parameterized, not declarative. The smaller difference is that it's intended to be passed around between related classes in a project, to enforce uniformity in the logs.

Log9er is for devs who have written too many `def log()` methods that clash with the other ones they've written. **Like me.**

Just do this instead:

    from log9er import Logger
    
    class Foo:
        def __init__(self, logger:Logger=None):
    
            # Pass a `log9er.Logger` in, or make a new one?
            # If new, we use `logging.getLogger()` to make sure it really is new.
    
            self.logger = logger or Logger(self.__class__.__name__)
    
            # Attach the `Logger.log()` method to your class.
    
            self.log = self.logger.log
    
            # Then log something at default `INFO` log-level.
    
            self.log(f"Initialized {self.__class__.__name__} with logger: {self.logger}")

This approach isn't for every project. For example, legacy projects with a lot of logging won't find it worthwhile to refactor.

But for those who want to have a `self.log()` method instead of a globally namespaced `logging.{LOGLEVEL}()` function&#x2026; **Log9er** might be for you.


<a id="org24e260a"></a>

## Features

Python's standard `logging` library is extremely flexible. It's like Photoshop.

**Log9er** is really very inflexible. It just gives you a `Logger` class and `Logger.log()` method that wrap Python's `logging` library methods, and gives you some basic ways to override some parameters.

The main benefit is uniformity of usage in development, reading, and parsing of logging across projects in the same ecosystem, or written by the same developer.

-   Reduce boilerplate logging logic across projects.
-   Log to `stderr`, `syslog`, or size-based rotating log files.
-   Reuse the same name to use the same Python `logging` logger.
-   Exception formatting, with traceback if the logger is in debug mode.

That's about it. Read the code. This is stupid-simple logging. It's not fancy.

Maybe that makes it elegant.


<a id="org8b9bb4b"></a>

# Installation

**Log9er** is available on PyPi, so just use `pip` or its alternatives to do something like:

    pip install log9er


<a id="org3609dcf"></a>

# Usage

**Log9er** is a library, so you have to write some Python.

See the bundled [API Documentation](docs/pdoc/index.html) for reference, but here are the broad strokes.

    import log9er
    
    # Make a basic logger that prints to stderr
    logger = log9er.Logger("HelloWorld", log="stderr")
    
    # Grab the log function
    log = logger.log
    
    # Log something
    log("Hello, World!")
    
    # Output:
    # Mar 29 13:34:46 HelloWorld[472647]: [INFO] HelloWorld!


<a id="org4089f40"></a>

## Initialize Logger

The `Logger` class provides a flexible interface for logging messages to various backends (such as syslog, file-based logging, or stderr) with customizable log levels.

If an existing Python built-in `logging.Logger` instance is provided, all other initialization parameters (except `debug`) are ignored.


### Arguments

-   **name (str)**: The name to assign to the logger instance, unless `logger` provided.

-   **log (str)**: The log output destination. For example, `syslog` or a file path. If `stderr`, logs go to standard output.
    -   If `log` is set to `stderr`, then error-level messages will be in output in red, if supported by your terminal emulator.

-   **level (int | str)**: The default logging level. Can be a string (e.g., `INFO` ) or an integer constant from the `logging` module (e.g., `logging.INFO` ).

-   **propagate (bool)**: Whether log records should propagate to the root logger. If True, the root logger also processes these messages (default: False).

-   **debug (bool)**: If True, enable traceback logging when `exception=True`.

-   **max\_bytes (int | None)**: If provided, and if `log` is a file path, use as the `maxBytes` for the `RotatingFileHandler` (default: `10485760`).

-   **backup\_count (int | None)**: If provided, and if `log` is a file path, use as the `backup_count` for the `RotatingFileHandler` (default: `5`).

-   **logger (logging.Logger | None)**: If provided, use this logger instance directly and ignore other arguments (except `debug`).


### Raises

`TypeError`: If `logger` is provided but is not an instance of `logging.Logger`.
`ValueError`: If `level` is an invalid log level string.
`FileNotFoundError`: If `log` is a file path and its directory does not exist.
`OSError`: If `log="syslog"` but `/dev/log` is not available on this system.


### Default System Log Example

By default, `Logger` will log to `syslog`, at log level `INFO`.

This makes it easier to initialize the most common use case.

    import logging
    from log9er import Logger
    
    # The 'name' arg is required for a new Logger
    logger = Logger("Example")
    
    # The above is equivalent to the following
    logger = Logger(
        name = "Example",             # 'name' is the 1st kwarg for simplicity
        log = "syslog",
        level = logging.INFO,
        propagate = False,
        debug = False,
        max_bytes = (10*1024*1024),
        backup_count = 5,
        logging = None
    )


### Stream Log Example

Another common use case would be to stream the logging to console. For convenience, we call this the `stderr` option, since by default the Python `logging.StreamHandler` outputs to `stderr`, and **Log9er** uses this default.

In addition, if the console supports it, then error-level messages will appear in red.

If your CLI application supports a debug mode, you can pass this through to get full traceback of exceptions.

    from log9er import Logger
    
    logger = Logger("Example", log="stderr", debug=True)


### Rotating File Log Example

Here's an example of initializing `Logger` using all possible arguments and keyword arguments (except `logger`).

Here we override the default `max_bytes` and `backup_count` for rotating log files, and limit the logger to error-level items.

**Note** that `name` is a **required** argument unless `logger` is passed.

    from log9er import Logger
    
    logger = Logger(
        "Example",
        log = "/var/log/example.log",
        level = "ERROR",
        propagate = True,
        debug = True,
        max_bytes = (5*1024*1024),
        backup_count = 3
    )


### Inject Logger Example

In addition, you can pass an existing Python `logging.Logger` object into the `log9er.Logger` wrapper.

**Log9er** will not override anything in the passed-in logger. It will not change the name, formatter, or handler defined on the given logger.

All it will do is provide the `log9er.Logger.log()` method to call the underlying `logging.log()` method. This allows the user to implement a uniform and parameterized approach to logging in related applications.

A less common use case would be to normalize an external Python `logging.Logger` for implementation in code that was written for a `log9er.Logger`.

    import logging
    import log9er
    
    # 1. Suppose we already have a logging.Logger...
    
    logging.basicConfig(level=logging.INFO)       # default level is WARNING
    logger1 = logging.getLogger()                 # default logger name is "root"
    logger1.info("Hello from logging.Logger!")
    
    # Output:
    # INFO:root:Hello from logging.Logger!
    
    # 2. Create a log9er.Logger from the above
    
    logger2 = log9er.Logger(logger=logger1)       # name not required if logger is passed
    logger2.log("Hello from log9er.Logger!")
    
    # Output:
    # INFO:root:Hello from log9er.Logger!


<a id="orga19ad04"></a>

## Log Method

The initialized `Logger` class provides the `Logger.log()` method, which may be used directly on the object, or attached to your custom class, as seen in the [Is Log9er For You?](#orgb98c5ce) section.

While `log()` is a simple wrapper on Python's `logger`, it does have a few differences worth mentioning:

-   **Multiple Messages**: You can provide multiple messages as positional arguments, and they will be concatenated with a newline and a tab.

-   **Log Level**: You can supply a string like `level="DEBUG"` or the usual constant like `level=logging.DEBUG`.

-   **Exceptions**: You can set `exception=True` to treat the messages as an exception. Messages will be prefixed with `Exception:` and in debug mode, this method will also dump the traceback.

-   **Prefix**: You can set `prefix="myfunction"` or any other string to prefix your message(s), emphasized by placing the prefix in brackets.


### Arguments

-   **\*msgs (str)**: One or more strings to log, e.g., `log("Hello", "World")`.

-   **level (int | str)**: The log level, e.g., `logging.INFO` or `INFO` . Defaults to `logging.INFO`.

-   **exception (bool)**: If True, prefix with "Exception:" and log a traceback if `self.debug` is also True.

-   **prefix (str | None)**: Optional prefix label. If provided, the log message is prefixed with, e.g. `[myfunction] message`.


### Multiple Messages

One of the bigger differences between Python's `logging` and `log9er` is that it accepts multiple messages, and will format them for you on multiple lines, with tabs to indent subsequent message parts.

    logger.log("Message 1", "Message 2", "Message 3", level=logging.WARNING)
    
    # Output:
    # Mar 29 17:14:10 Dummy[491147]: [WARNING] Message 1
    #	Message 2
    #	Message 3


### Log Level

As seen above, the `level` argument accepts `logging` constants.

It also accepts simple case-insensitive string values:

    logger.log("DEBUG constant", level=logging.DEBUG)
    logger.log("INFO is the default")
    logger.log("WARNING in upper case", level="WARNING")
    logger.log("ERROR in lower case", level="error")
    logger.log("CRITICAL in sarcastic case", level="CriTiCaL")

It will throw an exception if the level is invalid:

    logger.log("Bad log level 'foo'", level="foo")
    
    # Output:
    # ValueError: Invalid log level 'FOO'


### Exceptions

In **Log9er**, you just tell `log()` that the message is an exception, and if it's in debug mode, then it will also dump traceback.

With debug mode **disabled**, an exception only logs a single line:

    >>> logger = log9er.Logger("Logger", log="stderr")
    >>> try:
    ...     raise Exception("NO debug mode!")
    ... except Exception as ex:
    ...     logger.log(ex, exception=True)
    ...
    Mar 29 18:13:30 Logger[498590]: [ERROR] Exception: NO debug mode!

With debug mode **enabled**, we also get the traceback of the exception:

    >>> logger = log9er.Logger("Logger", log="stderr", debug=True)
    >>> try:
    ...     raise Exception("YES debug mode!")
    ... except Exception as ex:
    ...     logger.log(ex, exception=True)
    ...
    Mar 29 18:16:13 Logger[498590]: [ERROR] Exception: YES debug mode!
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
    Exception: YES debug mode!

**Log9er** simply wraps Python's built-in `logging.exception()` function for this traceback feature. It doesn't do anything special, or surprising.


### Prefix

Logging only helps if it tells us what we need to know. The `prefix` argument allows you to set an arbitrary identifier in brackets prior to the message.

For example:

    >>> logger.log("Prefixed message", prefix="Example")
    Mar 29 18:23:34 Logger[498590]: [INFO] [Example] Prefixed message


<a id="orgb57b666"></a>

# Authors

This is a dead-simple wrapper. It's practically a toy, except that it's just so handy.

I doubt anyone else will work on it.

Joseph Edwards VIII <joseph8th at gmail.com>

