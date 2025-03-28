"""
Logger utilities to prevent duplicate log handlers
"""
import logging

_CONFIGURED_LOGGERS = set()


def get_logger(name):
    """
    Get a logger with a single handler to prevent duplication

    Args:
        name: Name of the logger to configure

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if name in _CONFIGURED_LOGGERS:
        return logger

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.propagate = False

    _CONFIGURED_LOGGERS.add(name)

    return logger
