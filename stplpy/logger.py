"""
Logging configuration for Stplpy library.
"""
import logging
from typing import Optional


def get_logger(name: str = "stplpy", level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger for Stplpy.

    Args:
        name: Logger name
        level: Logging level (defaults to INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if no handlers exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    if level is not None:
        logger.setLevel(level)
    elif logger.level == logging.NOTSET:
        logger.setLevel(logging.INFO)

    return logger


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure logging for the entire Stplpy library.

    Args:
        level: Logging level to use
    """
    logger = get_logger()
    logger.setLevel(level)
