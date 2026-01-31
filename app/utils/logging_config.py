"""Logging configuration for the application.

This module provides structured logging setup that can be configured
for different environments (development vs production).
"""

import logging
import sys
from typing import Optional


class RequestFormatter(logging.Formatter):
    """Custom formatter that includes request context when available."""

    def format(self, record):
        # Try to add request context if available
        try:
            from flask import request, has_request_context

            if has_request_context():
                record.url = request.url
                record.method = request.method
                record.remote_addr = request.remote_addr
            else:
                record.url = "-"
                record.method = "-"
                record.remote_addr = "-"
        except Exception:
            record.url = "-"
            record.method = "-"
            record.remote_addr = "-"

        return super().format(record)


def configure_logging(app, level: Optional[str] = None):
    """Configure application logging.

    Sets up logging with appropriate format based on debug mode:
    - Debug mode: Human-readable format with colors
    - Production mode: Structured format suitable for log aggregation

    Args:
        app: Flask application instance
        level: Optional logging level override (DEBUG, INFO, WARNING, ERROR)
    """
    # Determine log level
    if level:
        log_level = getattr(logging, level.upper(), logging.INFO)
    elif app.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Set format based on environment
    if app.debug:
        # Human-readable format for development
        formatter = RequestFormatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
    else:
        # Structured format for production
        formatter = RequestFormatter(
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(method)s %(url)s | %(remote_addr)s | %(message)s"
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Set Flask app logger
    app.logger.setLevel(log_level)

    # Reduce noise from some verbose libraries
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    app.logger.info(f"Logging configured at {logging.getLevelName(log_level)} level")


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name.

    Args:
        name: Logger name (typically __name__ of the module)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
