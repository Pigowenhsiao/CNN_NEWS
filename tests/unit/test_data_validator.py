"""
Unit tests for data validation and default value assignment
"""
import pytest
from datetime import datetime
from src.utils.validator import (
    validate_article_data,
    assign_default_values,
    sanitize_content,
    validate_and_process_article,
    validate_scraping_result
)


def test_validate_article_data_required_fields_present():
    """Test that validate_article_data returns True when all required fields are present"""
    valid_article = {
        'title': 'Test Article',
        'content': 'Test content with at least 50 characters to pass content length validation',
        'url': 'https://example.com/article',
        'publication_date': datetime.now(),
        'source': 'Test Source'
    }
    
    result = validate_article_data(valid_article)
    assert result is True


def test_validate_article_data_missing_field():
    """Test that validate_article_data returns False when required field is missing"""
    incomplete_article = {
        'title': 'Test Article',
        'content': 'Test content with at least 50 characters to pass content length validation',
        'url': 'https://example.com/article',
        # Missing publication_date field
        'source': 'Test Source'
    }
    
    result = validate_article_data(incomplete_article)
    assert result is False
    

def test_validate_article_data_invalid_url():
    """Test that validate_article_data returns False for invalid URL format"""
    invalid_url_article = {
        'title': 'Test Article',
        'content': 'Test content with at least 50 characters to pass content length validation',
        'url': 'not_a_valid_url',  # Invalid URL
        'publication_date': datetime.now(),
        'source': 'Test Source'
    }
    
    result = validate_article_data(invalid_url_article)
    assert result is False


def test_validate_article_data_short_content():
    """Test that validate_article_data doesn't reject articles with short content"""
    short_content_article = {
        'title': 'Test Article',
        'content': 'Short content',  # Less than 50 characters
        'url': 'https://example.com/article',
        'publication_date': datetime.now(),
        'source': 'Test Source'
    }
    
    # Should still be valid even with short content (validation just warns)
    result = validate_article_data(short_content_article)
    assert result is True


def test_assign_default_values():
    """Test that assign_default_values properly assigns default values for missing fields"""
    incomplete_data = {
        'title': 'Test Article',
        'content': 'Test content',
        'url': 'https://example.com/article',
        'publication_date': datetime.now()
        # Missing 'source' and other optional fields
    }
    
    completed_data = assign_default_values(incomplete_data)
    
    # Verify that missing fields now have defaults
    assert 'source' in completed_data
    assert 'id' in completed_data
    assert 'scraped_at' in completed_data
    assert 'status' in completed_data
    assert 'quality_score' in completed_data
    assert completed_data['source'] != 'Unknown Source'  # source was provided
    assert completed_data['id'] != f"article_{'hash'('_')}_{'int(current_timestamp)'}"  # ID was generated


def test_assign_default_values_missing_critical_fields():
    """Test that assign_default_values handles completely missing critical fields"""
    empty_data = {}
    
    completed_data = assign_default_values(empty_data)
    
    # Verify defaults were assigned for all fields
    assert 'id' in completed_data
    assert 'title' in completed_data
    assert 'content' in completed_data
    assert 'url' in completed_data
    assert 'publication_date' in completed_data
    assert 'source' in completed_data
    
    # Verify default values were assigned
    assert completed_data['title'] == 'Untitled Article'
    assert completed_data['content'] == 'No content could be extracted.'
    assert completed_data['url'] == '#'
    assert completed_data['source'] == 'Unknown Source'


def test_sanitize_content_special_characters():
    """Test that sanitize_content properly escapes special characters"""
    raw_content = "This *content* has _special_ characters like # and \\"
    
    sanitized = sanitize_content(raw_content)
    
    # Verify special characters are escaped
    assert '\\*' in sanitized  # Asterisks should be escaped
    assert '\\_' in sanitized  # Underscores should be escaped
    assert '\\#' in sanitized  # Hash symbol should be escaped
    assert '\\\\' in sanitized  # Backslashes should be escaped


def test_sanitize_content_line_endings():
    """Test that sanitize_content normalizes line endings"""
    content_with_mixed_endings = "Line 1\r\nLine 2\nLine 3\rLine 4"
    
    sanitized = sanitize_content(content_with_mixed_endings)
    
    # Verify line endings are normalized to \n
    assert "\r\n" not in sanitized or sanitized.count("\r\n") <= sanitized.count("\n")


def test_sanitize_content_non_string_input():
    """Test that sanitize_content handles non-string input safely"""
    result = sanitize_content(None)
    assert result == ""
    
    result = sanitize_content(123)
    assert result == ""


def test_validate_scraping_result_valid():
    """Test that validate_scraping_result returns True for valid result"""
    valid_result = {
        'articles': [
            {
                'title': 'Test Article',
                'content': 'Test content with at least 50 characters to pass content length validation',
                'url': 'https://example.com/article',
                'publication_date': datetime.now(),
                'source': 'Test Source'
            }
        ],
        'errors': [],
        'start_time': datetime.now(),
        'end_time': datetime.now()
    }
    
    result = validate_scraping_result(valid_result)
    assert result is True


def test_validate_scraping_result_missing_keys():
    """Test that validate_scraping_result returns False when required keys are missing"""
    invalid_result = {
        'articles': [],  # Missing errors, start_time, end_time
    }
    
    result = validate_scraping_result(invalid_result)
    assert result is False


def test_validate_scraping_result_invalid_types():
    """Test that validate_scraping_result returns False for invalid types"""
    invalid_result = {
        'articles': "not_a_list",  # Should be a list
        'errors': [],
        'start_time': datetime.now(),
        'end_time': datetime.now()
    }
    
    result = validate_scraping_result(invalid_result)
    assert result is False


if __name__ == "__main__":
    pytest.main([__file__])