"""
Unit tests for date filtering logic
"""
import pytest
from datetime import datetime, timedelta, timezone
from src.utils.date_parser import is_within_72_hours, format_date_for_output
from src.models.article import NewsArticle


def test_is_within_72_hours_true():
    """Test that articles within 72 hours return True"""
    # Create a date 2 hours ago
    past_date = datetime.now(timezone.utc) - timedelta(hours=2)
    assert is_within_72_hours(past_date) == True


def test_is_within_72_hours_false():
    """Test that articles older than 72 hours return False"""
    # Create a date 73 hours ago
    past_date = datetime.now(timezone.utc) - timedelta(hours=73)
    assert is_within_72_hours(past_date) == False


def test_is_within_72_hours_exactly_72_hours():
    """Test that articles exactly at 72 hours return True"""
    past_date = datetime.now(timezone.utc) - timedelta(hours=72)
    assert is_within_72_hours(past_date) == True


def test_is_within_72_hours_none():
    """Test that None input returns False"""
    assert is_within_72_hours(None) == False


def test_format_date_for_output():
    """Test that dates are formatted correctly for output"""
    test_date = datetime(2023, 5, 15, 14, 30, 45)
    formatted = format_date_for_output(test_date)
    assert formatted == "2023-05-15 14:30:45"


def test_format_date_for_output_with_timezone():
    """Test that timezone-aware dates are formatted correctly"""
    test_date = datetime(2023, 5, 15, 14, 30, 45, tzinfo=timezone.utc)
    formatted = format_date_for_output(test_date)
    assert formatted == "2023-05-15 14:30:45"


def test_format_date_for_output_none():
    """Test that None input returns empty string"""
    assert format_date_for_output(None) == ""


if __name__ == "__main__":
    pytest.main([__file__])