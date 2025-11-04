"""
Unit tests for deduplication logic by title and content similarity
"""
import pytest
from src.deduplication import (
    Deduplicator,
    remove_duplicates,
    is_article_duplicate,
    add_article_to_dedupe,
    default_deduplicator
)
from src.models.article import EnhancedNewsArticle
from datetime import datetime


def test_deduplicator_initialization():
    """Test that Deduplicator initializes with empty tracking sets"""
    deduper = Deduplicator()
    
    assert len(deduper.unique_titles) == 0
    assert len(deduper.content_hashes) == 0


def test_content_hash_generation():
    """Test that content hashes are generated consistently"""
    deduper = Deduplicator()
    
    content1 = "This is a test article content."
    content2 = "This is a test article content."  # Same content
    content3 = "This is different article content."  # Different content
    
    hash1 = deduper.generate_content_hash(content1)
    hash2 = deduper.generate_content_hash(content2)
    hash3 = deduper.generate_content_hash(content3)
    
    # Same content should produce same hash
    assert hash1 == hash2
    
    # Different content should produce different hash
    assert hash1 != hash3


def test_is_duplicate_by_title():
    """Test duplicate detection based on title"""
    deduper = Deduplicator()
    
    # Create two articles with the same title but different content/URLs
    article1 = EnhancedNewsArticle(
        id="1",
        title="Test Article Title",
        content="First content",
        url="https://example.com/1",
        publication_date=datetime.now(),
        source="CNN"
    )
    
    article2 = EnhancedNewsArticle(
        id="2", 
        title="Test Article Title",  # Same title
        content="Second content",  # Different content
        url="https://example.com/2",  # Different URL
        publication_date=datetime.now(),
        source="CNN"
    )
    
    # First article should not be duplicate
    result1 = deduper.add_article(article1)
    assert result1 is True  # New article, not a duplicate
    
    # Second article should be duplicate based on title
    result2 = deduper.add_article(article2)
    assert result2 is False  # Duplicate detected


def test_is_duplicate_by_content():
    """Test duplicate detection based on content similarity"""
    deduper = Deduplicator()
    
    # Create two articles with same content but different titles/URLs
    content = "This is the exact same content in both articles."
    
    article1 = EnhancedNewsArticle(
        id="1",
        title="First Article",
        content=content,
        url="https://example.com/1",
        publication_date=datetime.now(),
        source="CNN"
    )
    
    article2 = EnhancedNewsArticle(
        id="2",
        title="Second Article",  # Different title
        content=content,  # Same content
        url="https://example.com/2",  # Different URL
        publication_date=datetime.now(),
        source="CNN"
    )
    
    # First article should not be duplicate
    result1 = deduper.add_article(article1)
    assert result1 is True  # New article, not a duplicate
    
    # Second article should be duplicate based on content
    result2 = deduper.add_article(article2)
    assert result2 is False  # Duplicate detected based on content


def test_different_articles_not_flagged_as_duplicates():
    """Test that genuinely different articles are not flagged as duplicates"""
    deduper = Deduplicator()
    
    article1 = EnhancedNewsArticle(
        id="1",
        title="First Unique Article",
        content="This is the content of the first unique article",
        url="https://example.com/1",
        publication_date=datetime.now(),
        source="CNN"
    )
    
    article2 = EnhancedNewsArticle(
        id="2",
        title="Second Unique Article", 
        content="This is the content of the second unique article",
        url="https://example.com/2",
        publication_date=datetime.now(),
        source="CNBC"
    )
    
    # Both articles should be considered unique
    result1 = deduper.add_article(article1)
    assert result1 is True  # New article, not a duplicate
    
    result2 = deduper.add_article(article2)
    assert result2 is True  # Also a new article, not a duplicate


def test_process_articles_removes_duplicates():
    """Test that process_articles removes duplicates from a list"""
    deduper = Deduplicator()
    
    # Reset the deduplicator to start fresh for this test
    deduper.unique_titles.clear()
    deduper.content_hashes.clear()
    
    original_articles = [
        EnhancedNewsArticle(id="1", title="Same Title", content="Content A", url="https://example.com/1", publication_date=datetime.now(), source="CNN"),
        EnhancedNewsArticle(id="2", title="Same Title", content="Content B", url="https://example.com/2", publication_date=datetime.now(), source="CNN"),  # Duplicate title
        EnhancedNewsArticle(id="3", title="Different Title", content="Content C", url="https://example.com/3", publication_date=datetime.now(), source="CNBC"),
        EnhancedNewsArticle(id="4", title="Different Title", content="Content C", url="https://example.com/4", publication_date=datetime.now(), source="CNN")  # Duplicate content
    ]
    
    unique_articles = deduper.process_articles(original_articles)
    
    # Should have reduced from 4 articles to 2 unique ones
    assert len(unique_articles) == 2
    
    # Verify the right articles remain (first of each duplicate set)
    assert unique_articles[0].id == "1"  # First article with "Same Title"
    assert unique_articles[1].id == "3"  # First article with "Different Title" but unique content


def test_global_deduplicator_functions():
    """Test the global deduplicator utility functions"""
    # Reset global instance for test
    default_deduplicator.unique_titles.clear()
    default_deduplicator.content_hashes.clear()
    
    article1 = EnhancedNewsArticle(
        id="1",
        title="Test Article",
        content="Test content",
        url="https://example.com/1",
        publication_date=datetime.now(),
        source="CNN"
    )
    
    article2 = EnhancedNewsArticle(
        id="2",
        title="Test Article",  # Same title (duplicate)
        content="Different content",
        url="https://example.com/2",
        publication_date=datetime.now(),
        source="CNN"
    )
    
    # Test add_article_to_dedupe function
    result1 = add_article_to_dedupe(article1)
    assert result1 is True  # Should be new article
    
    result2 = add_article_to_dedupe(article2)
    assert result2 is False  # Should be duplicate
    
    # Test is_article_duplicate function
    is_dup1 = is_article_duplicate(article1)
    is_dup2 = is_article_duplicate(article2)
    
    assert is_dup1 is False  # First instance was accepted
    assert is_dup2 is True   # Second instance with same title was rejected
    
    # Test remove_duplicates function
    articles_to_dedupe = [article1, article2]
    deduped_articles = remove_duplicates(articles_to_dedupe)
    
    assert len(deduped_articles) == 1  # Should have removed the duplicate
    assert deduped_articles[0].id == "1"  # Should keep the first article


def test_normalized_title_handling():
    """Test that titles are properly normalized for duplicate detection"""
    deduper = Deduplicator()
    
    # Create articles with titles that differ only by whitespace/case
    article1 = EnhancedNewsArticle(
        id="1",
        title="  Test   Article   Title  ",  # Extra whitespace
        content="Content A",
        url="https://example.com/1",
        publication_date=datetime.now(),
        source="CNN"
    )
    
    article2 = EnhancedNewsArticle(
        id="2", 
        title="test article title",  # Different case, no extra whitespace
        content="Content B",
        url="https://example.com/2", 
        publication_date=datetime.now(),
        source="CNN"
    )
    
    # First article should be added
    result1 = deduper.add_article(article1)
    assert result1 is True
    
    # Second article should be detected as duplicate due to normalized comparison
    result2 = deduper.add_article(article2)
    assert result2 is False  # Should be a duplicate after normalization


if __name__ == "__main__":
    pytest.main([__file__])