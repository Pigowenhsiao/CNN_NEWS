"""
Unit tests for logging functionality
"""
import pytest
import logging
import tempfile
import os
from src.utils.logger import setup_logging, log_info, log_warning, log_error, log_debug, log_critical


def test_setup_logging_creates_handlers():
    """Test that setup_logging configures logging infrastructure properly"""
    # Capture initial state to restore later
    initial_handlers = logging.getLogger().handlers[:]
    
    try:
        # Test that setup_logging works without error
        logger = setup_logging(log_level=logging.DEBUG, log_file="test_scraper.log")
        
        # Verify that handlers were added
        assert len(logging.getLogger().handlers) > 0
        
        # Clean up test log file if it was created
        if os.path.exists("test_scraper.log"):
            os.remove("test_scraper.log")
            
    finally:
        # Restore original handlers
        logging.getLogger().handlers[:] = initial_handlers


def test_log_info_function():
    """Test that log_info function records info-level messages"""
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_path = temp_file.name
    
    try:
        # Set up logging to our temporary file
        original_handlers = logging.getLogger().handlers[:]
        logging.getLogger().handlers.clear()
        
        handler = logging.FileHandler(temp_log_path)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Call the log function
        log_info("Test info message", "test_context")
        
        # Close and reopen the handler to ensure the message is written
        handler.close()
        
        # Read the log file and verify the message was recorded
        with open(temp_log_path, 'r') as f:
            content = f.read()
        
        assert "INFO - test_context: Test info message" in content or "INFO" in content and "Test info message" in content
        
    finally:
        # Clean up: restore original handlers and remove temp file
        logging.getLogger().handlers[:] = original_handlers
        if os.path.exists(temp_log_path):
            os.remove(temp_log_path)


def test_log_warning_function():
    """Test that log_warning function records warning-level messages"""
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_path = temp_file.name
    
    try:
        # Set up logging to our temporary file
        original_handlers = logging.getLogger().handlers[:]
        logging.getLogger().handlers.clear()
        
        handler = logging.FileHandler(temp_log_path)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Call the log function
        log_warning("Test warning message", "test_context")
        
        # Close and reopen the handler to ensure the message is written
        handler.close()
        
        # Read the log file and verify the message was recorded
        with open(temp_log_path, 'r') as f:
            content = f.read()
        
        assert "WARNING - test_context: Test warning message" in content or "WARNING" in content and "Test warning message" in content
        
    finally:
        # Clean up: restore original handlers and remove temp file
        logging.getLogger().handlers[:] = original_handlers
        if os.path.exists(temp_log_path):
            os.remove(temp_log_path)


def test_log_error_function():
    """Test that log_error function records error-level messages"""
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_path = temp_file.name
    
    try:
        # Set up logging to our temporary file
        original_handlers = logging.getLogger().handlers[:]
        logging.getLogger().handlers.clear()
        
        handler = logging.FileHandler(temp_log_path)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Call the log function
        log_error("Test error message", "test_context")
        
        # Close and reopen the handler to ensure the message is written
        handler.close()
        
        # Read the log file and verify the message was recorded
        with open(temp_log_path, 'r') as f:
            content = f.read()
        
        assert "ERROR - test_context: Test error message" in content or "ERROR" in content and "Test error message" in content
        
    finally:
        # Clean up: restore original handlers and remove temp file
        logging.getLogger().handlers[:] = original_handlers
        if os.path.exists(temp_log_path):
            os.remove(temp_log_path)


def test_log_debug_function():
    """Test that log_debug function records debug-level messages"""
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_path = temp_file.name
    
    try:
        # Set up logging to our temporary file
        original_handlers = logging.getLogger().handlers[:]
        logging.getLogger().handlers.clear()
        
        handler = logging.FileHandler(temp_log_path)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Call the log function
        log_debug("Test debug message", "test_context")
        
        # Close and reopen the handler to ensure the message is written
        handler.close()
        
        # Read the log file and verify the message was recorded
        with open(temp_log_path, 'r') as f:
            content = f.read()
        
        assert "DEBUG - test_context: Test debug message" in content or "DEBUG" in content and "Test debug message" in content
        
    finally:
        # Clean up: restore original handlers and remove temp file
        logging.getLogger().handlers[:] = original_handlers
        if os.path.exists(temp_log_path):
            os.remove(temp_log_path)


def test_log_critical_function():
    """Test that log_critical function records critical-level messages"""
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_path = temp_file.name
    
    try:
        # Set up logging to our temporary file
        original_handlers = logging.getLogger().handlers[:]
        logging.getLogger().handlers.clear()
        
        handler = logging.FileHandler(temp_log_path)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Call the log function
        log_critical("Test critical message", "test_context")
        
        # Close and reopen the handler to ensure the message is written
        handler.close()
        
        # Read the log file and verify the message was recorded
        with open(temp_log_path, 'r') as f:
            content = f.read()
        
        assert "CRITICAL - test_context: Test critical message" in content or "CRITICAL" in content and "Test critical message" in content
        
    finally:
        # Clean up: restore original handlers and remove temp file
        logging.getLogger().handlers[:] = original_handlers
        if os.path.exists(temp_log_path):
            os.remove(temp_log_path)


def test_get_logger_function():
    """Test that get_logger returns a named logger instance"""
    from src.utils.logger import get_logger
    
    logger = get_logger("test_module")
    assert logger is not None
    assert logger.name == "test_module"
    
    # Test that it can log messages
    # Create a temporary log file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_log_path = temp_file.name
    
    try:
        # Set up a handler for the test logger
        original_handlers = logging.getLogger().handlers[:]
        logging.getLogger().handlers.clear()
        
        handler = logging.FileHandler(temp_log_path)
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # Get a named logger and use it
        test_logger = get_logger("test_module")
        test_logger.info("Test message from named logger")
        
        # Close handler to flush the log
        handler.close()
        
        # Read the log file and verify the message was recorded with the right name
        with open(temp_log_path, 'r') as f:
            content = f.read()
        
        assert "test_module - INFO - Test message from named logger" in content
        
    finally:
        # Clean up: restore original handlers and remove temp file
        logging.getLogger().handlers[:] = original_handlers
        if os.path.exists(temp_log_path):
            os.remove(temp_log_path)


if __name__ == "__main__":
    pytest.main([__file__])