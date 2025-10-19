"""
Logging utility for the LangGraph Lead Generation System.

Provides consistent logging across all agents and tools.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str, log_level: str = "INFO") -> logging.Logger:
    """
    Set up a logger with consistent formatting.
    
    Args:
        name: Name of the logger (usually __name__)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Console handler (simplified output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler (detailed output)
    log_filename = log_dir / f"leadgen_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get an existing logger or create a new one.
    
    Args:
        name: Name of the logger
    
    Returns:
        Logger instance
    """
    # Get log level from environment variable
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    # Check if logger already exists
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger = setup_logger(name, log_level)
    
    return logger


# Create a default logger for the module
logger = get_logger(__name__)


if __name__ == "__main__":
    # Test the logger
    test_logger = get_logger("test")
    test_logger.debug("This is a debug message")
    test_logger.info("This is an info message")
    test_logger.warning("This is a warning message")
    test_logger.error("This is an error message")
    test_logger.critical("This is a critical message")
    print(f"\nLogs saved to: logs/leadgen_{datetime.now().strftime('%Y%m%d')}.log")
