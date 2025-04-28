import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for the application.
    
    Args:
        name: The name of the logger. If None, returns the root logger.
        
    Returns:
        A configured logger instance that will send logs to OpenTelemetry.
    """
    if name is None:
        return logging.getLogger()
    return logging.getLogger(f"app.{name}") 