
import sys
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime
from logging.handlers import RotatingFileHandler


# ANSI color codes
COLORS = {
    "DEBUG": "\033[36m",      # Cyan
    "INFO": "\033[32m",       # Green
    "WARNING": "\033[33m",    # Yellow
    "ERROR": "\033[31m",      # Red
    "CRITICAL": "\033[35m",   # Magenta
    "RESET": "\033[0m",       # Reset
}


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        levelname = record.levelname
        color = COLORS.get(levelname, COLORS["RESET"])
        
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        
        message = super().format(record)
        
        return f"{color}{message}{COLORS['RESET']}"


class Logger:
    """Structured logger for April."""
    
    def __init__(
        self,
        name: str = "april",
        log_level: str = "INFO",
        log_file: Optional[Path] = None,
        max_bytes: int = 10_485_760,  # 10MB
        backup_count: int = 5,
    ):
        """
        Initialize logger.
        
        Args:
            name: Logger name
            log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Path to log file (optional)
            max_bytes: Max size of log file before rotation
            backup_count: Number of backup files to keep
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.logger.propagate = False
        
        self.logger.handlers.clear()
        
        self._add_console_handler()
        
        if log_file:
            self._add_file_handler(log_file, max_bytes, backup_count)
    
    def _add_console_handler(self) -> None:
        """Add colored console handler."""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        formatter = ColoredFormatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(
        self,
        log_file: Path,
        max_bytes: int,
        backup_count: int,
    ) -> None:
        """Add rotating file handler."""
        # Ensure directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, extra=kwargs)
    
    def exception(self, message: str, **kwargs) -> None:
        """Log exception with traceback."""
        self.logger.exception(message, extra=kwargs)


# Global logger instance
_default_logger: Optional[Logger] = None


def setup_logger(
    name: str = "april",
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
) -> Logger:
    """
    Setup the global logger.
    
    Args:
        name: Logger name
        log_level: Log level
        log_file: Path to log file
    
    Returns:
        Configured logger instance
    """
    global _default_logger
    _default_logger = Logger(
        name=name,
        log_level=log_level,
        log_file=log_file or Path.home() / ".april" / "logs" / "april.log",
    )
    return _default_logger


def get_logger() -> Logger:
    """
    Get the global logger instance.
    
    Returns:
        Logger instance
    
    Raises:
        RuntimeError: If logger hasn't been setup
    """
    if _default_logger is None:
        raise RuntimeError("Logger not initialized. Call setup_logger() first.")
    return _default_logger