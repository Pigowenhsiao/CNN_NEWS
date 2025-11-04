# Implementation Plan: Dual Source Financial News Scraper Update

**Branch**: `002-news-scraper-update` | **Date**: 2025-11-03 | **Spec**: /specs/002-news-scraper-update/spec.md
**Input**: Feature specification from `/specs/002-news-scraper-update/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of enhancements to the dual-source financial news scraper that accesses CNBC Business (https://www.cnbc.com/business/) and CNN Business (https://www.cnn.com/business) pages to gather the latest financial news articles. The system will use Python 3.12.7 with httpx for asynchronous HTTP requests, BeautifulSoup4 for HTML parsing, and python-dateutil for date/time handling.

Key enhancements:
- Comprehensive error handling for all network operations, parsing activities, and file operations
- Detailed logging with appropriate severity levels (DEBUG, INFO, WARN, ERROR)
- Graceful recovery from network timeouts, DNS failures, and HTTP error responses
- Continued processing when individual articles fail, without affecting overall execution
- Optimized concurrent scraping to reduce total execution time by at least 15%
- Memory usage limited to under 500MB during normal operation
- Connection pooling to reduce overhead of repeated HTTP requests
- Caching of parsed content to avoid redundant processing of identical articles
- Enhanced deduplication algorithm considering content similarity in addition to title matching
- Validation of all scraped data fields with default values for missing information
- Consistent formatting with proper escaping and encoding
- Handling of articles with very long content without memory issues
- Rate limiting by implementing 3-5 second delays between requests to avoid being blocked by websites
- Automatic cleanup of output files after 30 days to prevent unbounded storage growth
- Data integrity validation to ensure all required fields are properly stored

## Technical Context

**Language/Version**: Python 3.12.7
**Primary Dependencies**: httpx (for modern, asynchronous HTTP requests), BeautifulSoup4 (for HTML parsing and data extraction), python-dateutil (for date/time parsing and timezone handling), pytest (for testing)  
**Storage**: File-based (Markdown output), with temporary in-memory storage for processing
**Testing**: pytest for unit and integration tests, with specific focus on error handling, performance optimization, deduplication logic, and data quality validation
**Logging**: Comprehensive logging at all levels including debug information for troubleshooting
**Target Platform**: Cross-platform Python application (Linux, macOS, Windows)
**Project Type**: Single project with modular architecture
**Performance Goals**: Concurrent scraping from both sources using asyncio, with 15% improvement in execution time and memory usage below 500MB
**Constraints**: Must implement comprehensive error handling, maintain performance improvements, handle long content without memory issues, comply with website terms of service and rate limits, implement rate limiting with 3-5 second delays, implement deduplication by title and content similarity
**Scale/Scope**: Designed to process news articles from 2 primary sources (CNBC and CNN) with potential for expansion to additional sources, with 30-day automatic cleanup of output files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Compliance with Constitution Principles:**

1. **Modularity and Readability**: Architecture will implement clear separation of concerns with distinct modules for web scraping (Parsing), error handling (ErrorHandling), performance optimization (Optimization), and data quality (Quality). Each component will have a single responsibility and be independently testable.

2. **Robust Error Handling**: Implementation will include comprehensive error handling for network request failures (HTTP 4xx/5xx), page structure changes (CSS Selector failures), and malformed URLs. All potential error conditions will be anticipated and handled gracefully without crashing the application.

3. **Efficiency with Asynchronous Requests**: Web requests will use efficient asynchronous patterns with Python's asyncio and httpx library to maximize throughput when scraping multiple news sources concurrently.

4. **Timeliness Enforcement**: Strict date checking logic built in - only news published within 3 days of the current date will be processed; otherwise, it must be skipped. This is the highest priority principle and will be enforced at the core of the scraping logic.

5. **Data Integrity and Testing Standards**: All successfully scraped news will store title, content, original URL, and publication date. The implementation will include unit tests specifically for error handling, performance optimization, data quality validation, and integration tests for complete flow.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

src/
├── scraper.py            # Core scraping coordinator using asyncio
├── cnn_parser.py         # CNN-specific parsing logic
├── cnbc_parser.py        # CNBC-specific parsing logic  
├── date_filter.py        # Date/time parsing and 72-hour filtering logic
├── output_writer.py      # Markdown output formatting and file writing
├── deduplication.py      # Article deduplication logic by title and content similarity
├── error_handler.py      # Comprehensive error handling for all operations
├── performance_optimizer.py  # Performance optimization with connection pooling and caching
├── data_validator.py     # Data validation and default value assignment
└── utils/                # Utility functions and helpers
    ├── __init__.py
    ├── helpers.py
    ├── rate_limiter.py   # Rate limiting with 3-5 second delays
    └── logger.py         # Comprehensive logging with severity levels

tests/
├── unit/
│   ├── test_error_handler.py      # Unit tests for error handling
│   ├── test_performance_optimizer.py  # Unit tests for performance optimization
│   ├── test_data_validator.py     # Unit tests for data validation
│   ├── test_deduplication.py      # Unit tests for enhanced deduplication
│   └── test_logger.py             # Unit tests for logging
├── integration/
│   └── test_end_to_end.py         # Integration tests for complete flow
└── conftest.py                    # Test configuration

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
