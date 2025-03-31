import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional


class JsonFormatter(logging.Formatter):
    """Formatter that outputs JSON strings after parsing the LogRecord."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the LogRecord into a JSON string."""
        log_data: Dict[str, Any] = {
            "t": datetime.utcnow().isoformat(),
            "m": record.getMessage(),
        }

        # If args has data, add it to the log_data
        if record.args:
            log_data["data"] = record.args

        # Add exception info if it exists
        if record.exc_info:
            log_data["exc"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logger(
    name: str,
    level: int = logging.INFO,
    stream: Optional[Any] = None,
) -> logging.Logger:
    """Set up a logger with JSON formatting.

    Args:
        name: The name of the logger
        level: The logging level (default: INFO)
        stream: The stream to write logs to (default: None, uses sys.stderr)

    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove any existing handlers
    logger.handlers = []

    # Create console handler
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance, creating it if it doesn't exist.

    Args:
        name: The name of the logger

    Returns:
        A logger instance
    """
    return logging.getLogger(name)
