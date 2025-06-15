"""
Logging utilities with stack trace support
"""
import logging
import logging.config
import traceback
from typing import Any, Optional

from config import config


def setup_logging():
    """Setup logging configuration with stack trace support for errors"""
    logging.config.dictConfig(config.get_log_config())


def log_error_with_traceback(logger: logging.Logger, message: str, exception: Optional[Exception] = None):
    """
    Log error message with full stack trace
    
    Args:
        logger: Logger instance
        message: Error message
        exception: Exception object (optional)
    """
    error_msg = f"{message}"
    
    if exception:
        error_msg += f": {str(exception)}"
    
    # Always include full stack trace for errors
    stack_trace = traceback.format_exc()
    full_message = f"{error_msg}\nStack Trace:\n{stack_trace}"
    
    logger.error(full_message)


def log_info_with_context(logger: logging.Logger, message: str, context: Optional[dict] = None):
    """
    Log info message with optional context
    
    Args:
        logger: Logger instance
        message: Info message
        context: Additional context information
    """
    if context:
        logger.info(f"{message} | Context: {context}")
    else:
        logger.info(message)


def log_warning_with_context(logger: logging.Logger, message: str, context: Optional[dict] = None):
    """
    Log warning message with optional context
    
    Args:
        logger: Logger instance
        message: Warning message
        context: Additional context information
    """
    if context:
        logger.warning(f"{message} | Context: {context}")
    else:
        logger.warning(message)


class StructuredLogger:
    """Structured logger class for consistent logging across the application"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def info(self, message: str, **kwargs):
        """Log info with structured data"""
        if kwargs:
            log_info_with_context(self.logger, message, kwargs)
        else:
            self.logger.info(message)
    
    def warning(self, message: str, **kwargs):
        """Log warning with structured data"""
        if kwargs:
            log_warning_with_context(self.logger, message, kwargs)
        else:
            self.logger.warning(message)
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log error with stack trace and structured data"""
        context = kwargs if kwargs else None
        if context:
            message += f" | Context: {context}"
        log_error_with_traceback(self.logger, message, exception)
    
    def debug(self, message: str, **kwargs):
        """Log debug with structured data"""
        if kwargs:
            self.logger.debug(f"{message} | Context: {kwargs}")
        else:
            self.logger.debug(message)