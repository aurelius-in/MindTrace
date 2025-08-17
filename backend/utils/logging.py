"""
Logging Utility - Structured logging setup
"""

import logging
import logging.config
import sys
from typing import Dict, Any
from datetime import datetime
import json
from pathlib import Path

from config.settings import settings


class StructuredFormatter(logging.Formatter):
    """
    Structured JSON formatter for logs
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as structured JSON
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)


class CustomLogger:
    """
    Custom logger with structured logging capabilities
    """
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def log_with_context(self, level: str, message: str, **context):
        """
        Log message with additional context
        """
        record = self.logger.makeRecord(
            self.logger.name,
            getattr(logging, level.upper()),
            "",
            0,
            message,
            (),
            None
        )
        record.extra_fields = context
        self.logger.handle(record)
    
    def info(self, message: str, **context):
        """Log info message with context"""
        self.log_with_context("INFO", message, **context)
    
    def warning(self, message: str, **context):
        """Log warning message with context"""
        self.log_with_context("WARNING", message, **context)
    
    def error(self, message: str, **context):
        """Log error message with context"""
        self.log_with_context("ERROR", message, **context)
    
    def debug(self, message: str, **context):
        """Log debug message with context"""
        self.log_with_context("DEBUG", message, **context)
    
    def critical(self, message: str, **context):
        """Log critical message with context"""
        self.log_with_context("CRITICAL", message, **context)


def setup_logging():
    """
    Setup structured logging configuration
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "structured": {
                "()": StructuredFormatter
            },
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "simple" if settings.DEBUG else "structured",
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": settings.LOG_LEVEL,
                "formatter": "structured",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "structured",
                "filename": "logs/error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5
            }
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console", "file", "error_file"],
                "level": settings.LOG_LEVEL,
                "propagate": False
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "handlers": ["console", "error_file"],
                "level": "ERROR",
                "propagate": False
            },
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False
            }
        }
    }
    
    # Apply configuration
    logging.config.dictConfig(logging_config)
    
    # Create main logger
    logger = logging.getLogger(__name__)
    logger.info("Logging setup completed", 
                log_level=settings.LOG_LEVEL,
                debug_mode=settings.DEBUG,
                environment=settings.ENVIRONMENT)


def get_logger(name: str) -> CustomLogger:
    """
    Get a custom logger instance
    """
    return CustomLogger(name)


def log_api_request(request_id: str, method: str, path: str, status_code: int, duration: float, user_id: str = None):
    """
    Log API request details
    """
    logger = get_logger("api")
    logger.info("API Request",
                request_id=request_id,
                method=method,
                path=path,
                status_code=status_code,
                duration=duration,
                user_id=user_id)


def log_api_error(request_id: str, method: str, path: str, error: str, user_id: str = None):
    """
    Log API error details
    """
    logger = get_logger("api")
    logger.error("API Error",
                 request_id=request_id,
                 method=method,
                 path=path,
                 error=error,
                 user_id=user_id)


def log_user_activity(user_id: str, activity_type: str, details: Dict[str, Any] = None):
    """
    Log user activity
    """
    logger = get_logger("user_activity")
    logger.info("User Activity",
                user_id=user_id,
                activity_type=activity_type,
                details=details or {})


def log_security_event(event_type: str, user_id: str = None, details: Dict[str, Any] = None):
    """
    Log security events
    """
    logger = get_logger("security")
    logger.warning("Security Event",
                   event_type=event_type,
                   user_id=user_id,
                   details=details or {})


def log_database_operation(operation: str, table: str, duration: float, success: bool, error: str = None):
    """
    Log database operations
    """
    logger = get_logger("database")
    level = "error" if not success else "info"
    logger.log_with_context(level, "Database Operation",
                           operation=operation,
                           table=table,
                           duration=duration,
                           success=success,
                           error=error)


def log_wellness_event(user_id: str, event_type: str, details: Dict[str, Any] = None):
    """
    Log wellness-related events
    """
    logger = get_logger("wellness")
    logger.info("Wellness Event",
                user_id=user_id,
                event_type=event_type,
                details=details or {})


def log_ai_interaction(user_id: str, interaction_type: str, details: Dict[str, Any] = None):
    """
    Log AI interactions
    """
    logger = get_logger("ai")
    logger.info("AI Interaction",
                user_id=user_id,
                interaction_type=interaction_type,
                details=details or {})


def log_compliance_event(user_id: str, event_type: str, details: Dict[str, Any] = None):
    """
    Log compliance events
    """
    logger = get_logger("compliance")
    logger.info("Compliance Event",
                user_id=user_id,
                event_type=event_type,
                details=details or {})


# Initialize logging when module is imported
setup_logging()
