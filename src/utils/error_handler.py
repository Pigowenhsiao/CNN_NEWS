"""
Comprehensive error handling module for all network operations, parsing activities, and file operations
"""
import logging
import asyncio
from typing import Dict, Any, Optional
import traceback
from datetime import datetime


def handle_request_failure(status_code: int, url: str) -> Dict[str, Any]:
    """
    Handle HTTP request failures with comprehensive error logging
    """
    error_map = {
        404: "Page not found",
        403: "Access forbidden - possibly blocked by website",
        429: "Rate limit exceeded - request throttled",
        500: "Internal server error",
        502: "Bad gateway",
        503: "Service unavailable",
        504: "Gateway timeout"
    }
    
    error_type = "NETWORK_ERROR"
    severity = "ERROR"
    if status_code in [429]:
        severity = "WARN"  # Rate limiting is expected behavior
    elif status_code >= 500:
        severity = "CRITICAL"
    elif status_code >= 400:
        severity = "ERROR"
    
    message = error_map.get(status_code, f"Request failed with status {status_code}")
    
    return {
        "error_type": error_type,
        "status_code": status_code,
        "url": url,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "severity": severity
    }


def handle_parsing_failure(element_type: str, url: str, details: str = "") -> Dict[str, Any]:
    """
    Handle page structure changes and parsing failures
    """
    return {
        "error_type": "PARSING_ERROR",
        "element_type": element_type,
        "url": url,
        "details": details,
        "message": f"Parsing failed for {element_type} at {url}",
        "timestamp": datetime.now().isoformat(),
        "severity": "ERROR"
    }


def log_error(exception: Exception, context: str = "", url: str = "") -> Dict[str, Any]:
    """
    Create and log error entry with full context and stack trace
    """
    error_entry = {
        "error_id": f"error_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
        "timestamp": datetime.now().isoformat(),
        "error_type": type(exception).__name__,
        "severity": "CRITICAL" if "critical" in str(exception).lower() else "ERROR",
        "context": context,
        "url": url,
        "message": str(exception),
        "stack_trace": traceback.format_exc(),
        "recovery_attempted": False,
        "recovery_successful": False,
        "recovery_action": None
    }
    
    # Log the error using the logging infrastructure
    logging.error(f"Error in {context} ({url}): {str(exception)}\n{traceback.format_exc()}")
    
    return error_entry


def handle_timeout_error(operation: str, timeout_duration: float, context: str = "") -> Dict[str, Any]:
    """
    Handle network timeout errors
    """
    return {
        "error_type": "TIMEOUT_ERROR",
        "operation": operation,
        "timeout_duration": timeout_duration,
        "context": context,
        "message": f"Operation {operation} timed out after {timeout_duration} seconds",
        "timestamp": datetime.now().isoformat(),
        "severity": "WARN"
    }


def handle_dns_failure(domain: str, context: str = "") -> Dict[str, Any]:
    """
    Handle DNS resolution failures
    """
    return {
        "error_type": "DNS_ERROR", 
        "domain": domain,
        "context": context,
        "message": f"DNS resolution failed for domain {domain}",
        "timestamp": datetime.now().isoformat(),
        "severity": "ERROR"
    }


def log_warning(message: str, context: str = "", url: str = "") -> None:
    """
    Log warning messages with appropriate context
    """
    logging.warning(f"Warning in {context} ({url}): {message}")


def log_info(message: str, context: str = "", url: str = "") -> None:
    """
    Log informational messages
    """
    logging.info(f"Info for {context} ({url}): {message}")


def log_debug(message: str, context: str = "", url: str = "") -> None:
    """
    Log debug messages
    """
    logging.debug(f"Debug for {context} ({url}): {message}")


async def safe_request_with_retry(client, url: str, max_retries: int = 3, delay: float = 1.0):
    """
    Safely execute a request with retry mechanism and comprehensive error handling
    """
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            response = await client.get(url)
            return response
        except Exception as e:
            last_exception = e
            log_warning(f"Request attempt {attempt + 1} failed: {str(e)}", "safe_request_with_retry", url)
            
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                await asyncio.sleep(delay * (2 ** attempt))  # Exponential backoff
            
    # If all retries failed, log critical error
    error_entry = log_error(last_exception, "safe_request_with_retry", url)
    return None