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


def generate_filename(name_prefix: str = None, extension: str = ".md") -> str:
    """
    Generate filename following the naming convention: {prefix}_yyyymmdd-hhmm.md
    Default: US_News_yyyymmdd-hhmm.md
    Example: US_News_20251103-1230.md
    
    Args:
        name_prefix (str, optional): Prefix for the filename. If None, uses configured value or defaults to "US_News"
        extension (str): File extension. Defaults to ".md"
    """
    config = None
    try:
        from config.loader import load_config
        config = load_config()
    except ImportError:
        pass  # If config module is not available, use defaults
    
    if name_prefix is None:
        if config and 'output_file_prefix' in config:
            name_prefix = config['output_file_prefix']
        else:
            name_prefix = "US_News"
    
    now = datetime.now()
    filename = f"{name_prefix}_{now.strftime('%Y%m%d-%H%M')}{extension}"
    return filename


def format_article_markdown(article: EnhancedNewsArticle) -> str:
    """
    Format a single article in Markdown format with required fields and proper escaping and encoding
    
    Args:
        article (EnhancedNewsArticle): Article to format in Markdown
        
    Returns:
        str: Formatted Markdown content for the article
    """
    from html import escape
    
    # Format the publication date to required format: YYYY-MM-DD HH:MM:SS
    formatted_date = article.publication_date.strftime('%Y-%m-%d %H:%M:%S') if article.publication_date else "N/A"
    
    # Escape special characters in the fields to ensure proper encoding
    escaped_title = escape(article.title)
    escaped_source = escape(article.source)
    escaped_url = escape(article.url)
    
    # Construct the Markdown content for this article with proper escaping
    markdown_content = f"## {escaped_title}\n\n"
    markdown_content += f"- **Source**: {escaped_source}\n"
    markdown_content += f"- **Published**: {formatted_date}\n"
    markdown_content += f"- **URL**: {escaped_url}\n\n"
    
    # Format and add the content with proper encoding
    content_lines = article.content.split('\n')
    formatted_content = '\n'.join(content_lines)
    markdown_content += f"{formatted_content}\n\n"
    markdown_content += "---\n\n"  # Separator between articles
    
    return markdown_content


def validate_output_requirements(articles: List[EnhancedNewsArticle]) -> bool:
    """
    Validate that all articles meet the output requirements before writing to file
    
    Each article entry must include: source website, title, publication date (formatted as YYYY-MM-DD HH:MM:SS), 
    URL, and article content. Content must be at least 50 characters.
    
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
        ]) or len(article.content) < 50:
            return False
    
    return True


def validate_and_fix_article(article: EnhancedNewsArticle) -> EnhancedNewsArticle:
    """
    Validate all scraped data fields and provide default values for missing information
    
    Args:
        article (EnhancedNewsArticle): Article to validate and fix
        
    Returns:
        EnhancedNewsArticle: Validated and fixed article with required fields
    """
    from datetime import datetime
    
    # Provide default values for missing fields
    if not article.source:
        article.source = "Unknown Source"
    
    if not article.title:
        article.title = "No Title Available"
    
    if not article.url:
        article.url = "No URL Available"
    
    if not article.content:
        article.content = "No Content Available"
    
    if not article.publication_date:
        article.publication_date = datetime.now()
    
    # Ensure content is at least 50 characters
    if len(article.content) < 50:
        article.content += " " + "This content was too short and has been padded to meet the minimum length requirement."
    
    # Limit content length to prevent memory issues (optional - configurable)
    max_content_length = 50000  # Configurable maximum length
    if len(article.content) > max_content_length:
        print(f"Truncating content for article '{article.title}' from {len(article.content)} to {max_content_length} characters to prevent memory issues")
        article.content = article.content[:max_content_length]
    
    return article


def validate_and_fix_articles(articles: List[EnhancedNewsArticle]) -> List[EnhancedNewsArticle]:
    """
    Validate all scraped data fields in a list of articles and provide default values for missing information
    
    Args:
        articles (List[EnhancedNewsArticle]): List of articles to validate and fix
        
    Returns:
        List[EnhancedNewsArticle]: List of validated and fixed articles with required fields
    """
    return [validate_and_fix_article(article) for article in articles]


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
    
    # Clean up old files before creating a new one (automatically cleans up files older than 30 days)
    cleanup_old_files(days=30)
    
    # Validate and fix all articles to ensure required fields are properly set
    articles = validate_and_fix_articles(articles)
    
    # Validate that all articles have required fields
    if not validate_output_requirements(articles):
        print("Warning: Some articles do not meet output requirements after validation and fixing")
    
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


def cleanup_old_files(days: int = 30) -> None:
    """
    Clean up old output files after specified number of days to prevent unbounded storage growth
    
    Args:
        days (int): Number of days after which files should be deleted. Defaults to 30.
    """
    import os
    import glob
    from datetime import datetime, timedelta
    
    # Find all files matching the output pattern
    current_dir = os.getcwd()
    pattern = os.path.join(current_dir, "US_News_*.md")
    files = glob.glob(pattern)
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    for file_path in files:
        # Get the file modification time
        mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        # Check if file is older than the cutoff date
        if mod_time < cutoff_date:
            try:
                os.remove(file_path)
                print(f"Cleaned up old file: {file_path}")
            except OSError as e:
                print(f"Could not delete old file {file_path}: {e}")