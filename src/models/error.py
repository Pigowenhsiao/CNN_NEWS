"""
Error Log Entry model with detailed error information and context
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class ErrorLogEntry:
    """
    Detailed error information with context, stack traces, and recovery attempts
    """
    error_id: str  # Unique identifier for the error
    timestamp: datetime  # When the error occurred
    error_type: str  # Type of error (e.g., NETWORK_ERROR, PARSING_ERROR, VALIDATION_ERROR)
    severity: str  # Severity level (DEBUG, INFO, WARN, ERROR, CRITICAL)
    source_component: str  # Component where error originated (e.g., CNN_PARSER, CNBC_PARSER, SCRAPER)
    url: Optional[str]  # URL being processed when error occurred (if applicable)
    error_message: str  # Human-readable error message
    stack_trace: Optional[str]  # Full stack trace for debugging (if available)
    context_data: Optional[Dict[str, Any]]  # Additional context data for troubleshooting
    recovery_attempted: bool  # Whether recovery was attempted (true/false)
    recovery_successful: bool  # Whether recovery was successful (true/false)
    recovery_action: Optional[str]  # Action taken for recovery (if any)