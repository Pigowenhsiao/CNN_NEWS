"""
Unit tests for output writer functionality
"""
import pytest
import os
import tempfile
from datetime import datetime
from unittest.mock import patch, mock_open
from src.output_writer import (
    generate_filename,
    format_article_markdown,
    write_to_markdown,
    validate_output_requirements
)
from src.models.article import EnhancedNewsArticle


def test_generate_filename_follows_convention():
    """Test that generate_filename creates files following naming convention: US_News_yyyymmdd-hhmm.md"""
    with patch('datetime.datetime') as mock_datetime:
        mock_date = datetime(2025, 11, 3, 10, 30)
        mock_datetime.now.return_value = mock_date
        
        filename = generate_filename()
        
        # Verify the format matches US_News_yyyymmdd-hhmm.md
        assert filename.startswith("US_News_")
        assert filename.endswith(".md")
        # Should be US_News_20251103-1030.md format
        assert "US_News_20251103-1030.md" == filename


def test_format_article_markdown_structure():
    """Test that format_article_markdown creates proper Markdown structure"""
    test_article = EnhancedNewsArticle(
        id="test_id",
        title="Test Article Title",
        content="This is the content of the test article.",
        url="https://example.com/test-article",
        publication_date=datetime(2025, 11, 3, 9, 15, 30),
        source="Test Source"
    )
    
    formatted_content = format_article_markdown(test_article)
    
    # Verify structure elements are present
    assert "## Test Article Title" in formatted_content
    assert "- **Source**: Test Source" in formatted_content
    assert "- **Published**: 2025-11-03 09:15:30" in formatted_content
    assert "- **URL**: https://example.com/test-article" in formatted_content
    assert "This is the content of the test article." in formatted_content
    assert "---" in formatted_content  # Separator


def test_format_article_markdown_empty_article():
    """Test that format_article_markdown handles empty article gracefully"""
    empty_article = EnhancedNewsArticle(
        id="empty_id",
        title="",
        content="",
        url="",
        publication_date=datetime.now(),
        source=""
    )
    
    formatted_content = format_article_markdown(empty_article)
    
    # Should still return properly formatted structure even with empty fields
    assert "## " in formatted_content  # Title header exists
    assert "**Source**" in formatted_content
    assert "**Published**" in formatted_content
    assert "**URL**" in formatted_content


@patch('builtins.open', new_callable=mock_open)
@patch('os.makedirs')
def test_write_to_markdown_creates_file(mock_makedirs, mock_file):
    """Test that write_to_markdown creates a properly formatted Markdown file"""
    test_articles = [
        EnhancedNewsArticle(
            id="1",
            title="First Test Article",
            content="Content of the first test article with sufficient length for validation.",
            url="https://example.com/article1",
            publication_date=datetime(2025, 11, 3, 8, 0, 0),
            source="CNN"
        ),
        EnhancedNewsArticle(
            id="2",
            title="Second Test Article", 
            content="Content of the second test article with sufficient length for validation.",
            url="https://example.com/article2",
            publication_date=datetime(2025, 11, 3, 9, 0, 0),
            source="CNBC"
        )
    ]
    
    # Test that the function creates a file with the correct content
    result_path = write_to_markdown(test_articles, "test_output.md")
    
    # Verify the file was opened for writing
    mock_file.assert_called_once_with("test_output.md", 'w', encoding='utf-8')
    
    # Verify content was written
    written_content = ''.join(call.args[0] for call in mock_file().write.call_args_list)
    assert "# US Financial News Summary" in written_content
    assert "Generated on:" in written_content
    assert "First Test Article" in written_content
    assert "Second Test Article" in written_content
    assert "CNN" in written_content
    assert "CNBC" in written_content


def test_write_to_markdown_with_no_articles():
    """Test that write_to_markdown handles empty article list gracefully"""
    with patch('src.utils.logger.log_info') as mock_log:
        result = write_to_markdown([])
        
        # Should return empty string and log appropriately
        assert result == ""
        mock_log.assert_called_once_with("No articles to write to Markdown file", "OutputWriter")


def test_write_to_markdown_with_custom_filename():
    """Test that write_to_markdown accepts a custom filename"""
    test_article = EnhancedNewsArticle(
        id="1",
        title="Custom Filename Test",
        content="Content with sufficient length for validation.",
        url="https://example.com/test",
        publication_date=datetime(2025, 11, 3, 10, 0, 0),
        source="Test Source"
    )
    
    # Create a temporary directory for the test
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_filename = os.path.join(tmpdir, "custom_news_file.md")
        
        # Use our temporary directory but write to a test file
        result_path = write_to_markdown([test_article], custom_filename)
        
        # Verify the file was created
        assert os.path.exists(custom_filename)


def test_validate_output_requirements_valid_articles():
    """Test that validate_output_requirements returns True for valid articles"""
    valid_articles = [
        EnhancedNewsArticle(
            id="1",
            title="Valid Article",
            content="This is valid content that meets the minimum length requirement for validation.",
            url="https://example.com/valid",
            publication_date=datetime.now(),
            source="CNN"
        )
    ]
    
    result = validate_output_requirements(valid_articles)
    assert result is True


def test_validate_output_requirements_invalid_articles():
    """Test that validate_output_requirements returns False for invalid articles"""
    # Create an article with missing critical fields
    invalid_article = EnhancedNewsArticle(
        id="",  # Invalid - empty ID
        title="",  # Invalid - empty title
        content="",  # Invalid - empty content
        url="",  # Invalid - empty URL
        publication_date=None,  # Invalid - None publication date
        source=""  # Invalid - empty source
    )
    
    result = validate_output_requirements([invalid_article])
    assert result is False


if __name__ == "__main__":
    import sys
    import os
    # Add the src directory to path so imports work
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    
    pytest.main([__file__])