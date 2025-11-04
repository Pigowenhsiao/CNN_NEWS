"""
Logging infrastructure with appropriate severity levels
"""
import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """
    Configure comprehensive logging infrastructure with all severity levels
    """
    # Create logger
    logger = logging.getLogger('news_scraper')
    logger.setLevel(log_level)
    
    # Prevent adding multiple handlers if already configured
    if logger.handlers:
        return logger
    
    # Create console handler with a higher log level
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create file handler
    file_handler = logging.FileHandler('scraper.log')
    file_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def log_info(message: str, component: str = "general"):
    """
    Log info message with component context
    """
    logger = logging.getLogger('news_scraper')
    logger.info(f"[{component}] {message}")


def log_error(message: str, component: str = "general"):
    """
    Log error message with component context
    """
    logger = logging.getLogger('news_scraper')
    logger.error(f"[{component}] {message}")


def log_warning(message: str, component: str = "general"):
    """
    Log warning message with component context
    """
    logger = logging.getLogger('news_scraper')
    logger.warning(f"[{component}] {message}")


def log_debug(message: str, component: str = "general"):
    """
    Log debug message with component context
    """
    logger = logging.getLogger('news_scraper')
    logger.debug(f"[{component}] {message}")


def log_critical(message: str, component: str = "general"):
    """
    Log critical message with component context
    """
    logger = logging.getLogger('news_scraper')
    logger.critical(f"[{component}] {message}")