"""
Additional unit tests for date parsing functionality
"""
import pytest
from datetime import datetime
from src.utils.date_parser import parse_article_date


def test_parse_cnn_date_formats():
    """Test parsing of various CNN date formats"""
    # Test common CNN date formats
    cnn_dates = [
        "Published: May 12, 2023",
        "Updated: 2023-05-12T10:30:00Z",
        "2023-05-12T17:30:00.000000Z",
        "May 12, 2023 at 10:30 AM",
    ]
    
    for date_str in cnn_dates:
        result = parse_article_date(date_str, "cnn")
        assert result is not None
        assert isinstance(result, datetime)


def test_parse_cnbc_date_formats():
    """Test parsing of various CNBC date formats"""
    # Test common CNBC date formats
    cnbc_dates = [
        "5:30 PM EST May 12, 2023",
        "2023-05-12T17:30:00.000000Z",
        "Published May 12, 2023",
        "May 12, 2023, 5:30 PM",
    ]
    
    for date_str in cnbc_dates:
        result = parse_article_date(date_str, "cnbc")
        assert result is not None
        assert isinstance(result, datetime)


def test_parse_invalid_date():
    """Test that invalid dates return None"""
    invalid_dates = [
        "",
        "not a date",
        "May 12",
        "2023",
        None,
    ]
    
    for date_str in invalid_dates:
        result = parse_article_date(date_str, "cnn") if date_str is not None else parse_article_date("", "cnn")
        # For None input specifically
        if date_str is None:
            result = parse_article_date(None, "cnn")
        assert result is None


def test_parse_date_case_insensitive():
    """Test that date parsing works regardless of case"""
    date_strings = [
        "PUBLISHED: May 12, 2023",
        "published: May 12, 2023",
        "Published: May 12, 2023",
    ]
    
    for date_str in date_strings:
        result = parse_article_date(date_str, "cnn")
        assert result is not None
        assert result.year == 2023
        assert result.month == 5
        assert result.day == 12


if __name__ == "__main__":
    pytest.main([__file__])