import logging
from typing import Any, Dict, Optional

class PennFlowError(Exception):
    """Base exception class for PennFlow application."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class AWSResourceError(PennFlowError):
    """Exception raised for AWS resource related errors."""
    pass

class AuthenticationError(PennFlowError):
    """Exception raised for authentication related errors."""
    pass

class DatabaseError(PennFlowError):
    """Exception raised for database related errors."""
    pass

def setup_logger(name: str) -> logging.Logger:
    """Set up a logger with the specified name."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def handle_aws_error(error: Exception, context: Dict[str, Any]) -> None:
    """Handle AWS related errors and log them appropriately."""
    logger = setup_logger('aws_error')
    error_message = f"AWS Error in {context.get('operation', 'unknown operation')}: {str(error)}"
    logger.error(error_message)
    raise AWSResourceError(error_message)

def handle_auth_error(error: Exception, context: Dict[str, Any]) -> None:
    """Handle authentication related errors and log them appropriately."""
    logger = setup_logger('auth_error')
    error_message = f"Authentication Error in {context.get('operation', 'unknown operation')}: {str(error)}"
    logger.error(error_message)
    raise AuthenticationError(error_message)

def handle_db_error(error: Exception, context: Dict[str, Any]) -> None:
    """Handle database related errors and log them appropriately."""
    logger = setup_logger('db_error')
    error_message = f"Database Error in {context.get('operation', 'unknown operation')}: {str(error)}"
    logger.error(error_message)
    raise DatabaseError(error_message) 