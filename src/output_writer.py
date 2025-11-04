"""
Markdown output formatting and file writing with naming convention
"""
import os
import sys
from datetime import datetime
from typing import List
from pathlib import Path

# Add the src directory to Python path for absolute imports
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

from models.article import EnhancedNewsArticle


def generate_filename() -> str:
    """
    Generate filename following the naming convention: US_News_yyyymmdd-hhmm.md
    Example: US_News_20251103-1230.md
    """
    now = datetime.now()
    filename = f"US_News_{now.strftime('%Y%m%d-%H%M')}.md"
    return filename


def format_article_markdown(article: EnhancedNewsArticle) -> str:
    """
    Format a single article in Markdown format with required fields
    
    Args:
        article (EnhancedNewsArticle): Article to format in Markdown
        
    Returns:
        str: Formatted Markdown content for the article
    """
    # Format the publication date to required format: YYYY-MM-DD HH:MM:SS
    formatted_date = article.publication_date.strftime('%Y-%m-%d %H:%M:%S') if article.publication_date else "N/A"
    
    # Construct the Markdown content for this article
    markdown_content = f"## {article.title}\n\n"
    markdown_content += f"- **Source**: {article.source}\n"
    markdown_content += f"- **Published**: {formatted_date}\n"
    markdown_content += f"- **URL**: {article.url}\n\n"
    markdown_content += f"{article.content}\n\n"
    markdown_content += "---\n\n"  # Separator between articles
    
    return markdown_content


def validate_output_requirements(articles: List[EnhancedNewsArticle]) -> bool:
    """
    Validate that all articles meet the output requirements before writing to file
    
    Each article entry must include: source website, title, publication date (formatted as YYYY-MM-DD HH:MM:SS), 
    URL, and article content
    
    Args:
        articles (List[EnhancedNewsArticle]): Articles to validate
        
    Returns:
        bool: True if all articles meet requirements, False otherwise
    """
    for article in articles:
        if not all([
            article.source,
            article.title,
            article.url,
            article.content,
            article.publication_date
        ]):
            return False
    
    return True


def write_to_markdown(articles: List[EnhancedNewsArticle], filename: str = None) -> str:
    """
    Write processed articles to a formatted Markdown file following the naming convention
    
    Args:
        articles (List[EnhancedNewsArticle]): List of articles to write to file
        filename (str): Optional filename; if not provided, will use naming convention
        
    Returns:
        str: Path to the created Markdown file
    """
    if not articles:
        print("No articles to write to Markdown file")
        return ""
    
    # Generate filename if not provided
    if not filename:
        filename = generate_filename()
    
    # Validate that all articles have required fields
    if not validate_output_requirements(articles):
        print("Warning: Some articles do not meet output requirements")
    
    # Prepare the complete Markdown content
    content = f"# US Financial News Summary\n\n"
    content += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # Add each article to the content
    for article in articles:
        content += format_article_markdown(article)
    
    # Ensure the output directory exists
    directory = os.path.dirname(filename) if os.path.dirname(filename) else '.'
    os.makedirs(directory, exist_ok=True)
    
    try:
        # Write the content to the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Successfully wrote {len(articles)} articles to {filename}")
        
        return os.path.abspath(filename)
        
    except Exception as e:
        print(f"Error writing to file {filename}: {str(e)}")
        return ""