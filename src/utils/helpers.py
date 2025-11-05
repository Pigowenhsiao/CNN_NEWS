"""
Utility functions and helper methods for the news scraper
"""
import asyncio
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import logging


def setup_logging(log_level: int = logging.INFO):
    """
    Configure comprehensive error handling and logging infrastructure
    """
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('scraper.log', mode='a')
            ]
        )


def log_info(message: str, component: str = "general"):
    """
    Log info messages with component context
    """
    logger = logging.getLogger(component)
    logger.info(message)


def log_error(message: str, component: str = "general", error: Exception = None):
    """
    Log error messages with optional exception details
    """
    logger = logging.getLogger(component)
    if error:
        logger.error(f"{message}: {str(error)}", exc_info=True)
    else:
        logger.error(message)


def log_warning(message: str, component: str = "general"):
    """
    Log warning messages with component context
    """
    logger = logging.getLogger(component)
    logger.warning(message)


def log_debug(message: str, component: str = "general"):
    """
    Log debug messages with component context
    """
    logger = logging.getLogger(component)
    logger.debug(message)


def log_critical(message: str, component: str = "general"):
    """
    Log critical messages with component context
    """
    logger = logging.getLogger(component)
    logger.critical(message)


async def safe_request_with_retry(client: httpx.AsyncClient, url: str, max_retries: int = 3) -> Optional[httpx.Response]:
    """
    Safely make HTTP request with retry mechanism for network failures
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            response = await client.get(url)
            return response
        except Exception as e:
            last_exception = e
            log_warning(f"Request attempt {attempt + 1}/{max_retries} failed for {url}: {str(e)}", "utils.helpers")
            
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            else:
                log_error(f"All {max_retries} attempts failed for {url}", "utils.helpers", e)
    
    return None


def handle_request_failure(status_code: int, url: str) -> Dict[str, Any]:
    """
    Handle HTTP request failure with appropriate error classification
    """
    error_details = {
        "url": url,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat(),
        "handled": True
    }
    
    if 400 <= status_code < 500:
        error_details["category"] = "client_error"
        error_details["message"] = f"Client error {status_code} for {url}"
    elif 500 <= status_code < 600:
        error_details["category"] = "server_error" 
        error_details["message"] = f"Server error {status_code} for {url}"
    else:
        error_details["category"] = "other_error"
        error_details["message"] = f"Unexpected status {status_code} for {url}"
    
    return error_details


def handle_parsing_failure(exception: Exception, source: str = "unknown") -> Dict[str, Any]:
    """
    Handle parsing failures during HTML parsing with appropriate classification
    """
    error_details = {
        "source": source,
        "exception_type": type(exception).__name__,
        "message": str(exception),
        "timestamp": datetime.now().isoformat(),
        "handled": True
    }
    
    return error_details


def handle_file_operation_failure(operation: str, file_path: str, exception: Exception) -> Dict[str, Any]:
    """
    Handle file operation failures with appropriate error classification
    """
    error_details = {
        "operation": operation,
        "file_path": file_path,
        "exception_type": type(exception).__name__,
        "message": str(exception),
        "timestamp": datetime.now().isoformat(),
        "handled": True
    }
    
    return error_details