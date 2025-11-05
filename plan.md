# Implementation Plan: Dual Source Financial News Scraper

**Branch**: `001-news-scraper` | **Date**: 2025-11-03 | **Spec**: /specs/001-news-scraper/spec.md
**Input**: Feature specification from `/specs/001-news-scraper/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a dual-source financial news scraper that accesses CNBC Business (https://www.cnbc.com/business/) and CNN Business (https://www.cnn.com/business) pages to gather the latest financial news articles. The system will use Python 3.12.7 with httpx for asynchronous HTTP requests, BeautifulSoup4 for HTML parsing, and python-dateutil for date/time handling.

Key features:
- Concurrent scraping from both CNBC and CNN using asyncio
- Strict 72-hour date filtering to ensure news relevance
- Modular architecture separating parsing, filtering, and output concerns
- Robust error handling for network failures and page structure changes
- Rate limiting by waiting 3-5 seconds between each request to avoid being blocked by websites
- Deduplication by article title to prevent duplicate entries in output
- Output to structured Markdown files with naming convention: US_News_yyyymmdd-hhmm.md
- Automatic cleanup of output files after 30 days to prevent unbounded storage growth
- Comprehensive logging at all levels (including debug information) for troubleshooting

## Technical Context

**Language/Version**: Python 3.12.7
**Primary Dependencies**: httpx (for modern, asynchronous HTTP requests), BeautifulSoup4 (for HTML parsing and data extraction), python-dateutil (for date/time parsing and timezone handling), pytest (for testing)  
**Storage**: File-based (Markdown output), with temporary in-memory storage for processing
**Testing**: pytest for unit and integration tests, with specific focus on date parsing/filtering validation, deduplication logic, and rate limiting functionality
**Logging**: Comprehensive logging at all levels including debug information for troubleshooting
**Target Platform**: Cross-platform Python application (Linux, macOS, Windows)
**Project Type**: Single project with modular architecture
**Performance Goals**: Concurrent scraping from both sources using asyncio, with 80% success rate for content extraction within 30 seconds per article
**Constraints**: Must implement strict 72-hour date filtering, handle both CNBC and CNN page structures independently, comply with website terms of service and rate limits, implement rate limiting with 3-5 second delays, implement deduplication by title
**Scale/Scope**: Designed to process news articles from 2 primary sources (CNBC and CNN) with potential for expansion to additional sources, with 30-day automatic cleanup of output files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Compliance with Constitution Principles:**

1. **Modularity and Readability**: Architecture will implement clear separation of concerns with distinct modules for web scraping (Parsing), date filtering (Filtering), and data storage (Output). Each component will have a single responsibility and be independently testable.

2. **Robust Error Handling**: Implementation will include comprehensive error handling for network request failures (HTTP 4xx/5xx), page structure changes (CSS Selector failures), and malformed URLs. All potential error conditions will be anticipated and handled gracefully.

3. **Efficiency with Asynchronous Requests**: Web requests will use efficient asynchronous patterns with Python's asyncio and httpx library to maximize throughput when scraping multiple news sources concurrently.

4. **Timeliness Enforcement**: Strict date checking logic will be built into the system - only news published within 3 days of the current date will be processed. This is the highest priority principle and will be enforced at the core of the scraping logic.

5. **Data Integrity and Testing Standards**: All successfully scraped news will store title, content, original URL, and publication date. The implementation will include unit tests specifically for date parsing/filtering and integration tests for complete flow.

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
├── deduplication.py      # Article deduplication logic by title
└── utils/                # Utility functions and helpers
    ├── __init__.py
    ├── helpers.py
    └── rate_limiter.py   # Rate limiting with 3-5 second delays

tests/
├── unit/
│   ├── test_date_filter.py      # Unit tests for date parsing/filtering
│   ├── test_cnn_parser.py       # Unit tests for CNN parsing
│   ├── test_cnbc_parser.py      # Unit tests for CNBC parsing
│   ├── test_deduplication.py    # Unit tests for deduplication logic
│   └── test_rate_limiter.py     # Unit tests for rate limiting
├── integration/
│   └── test_end_to_end.py       # Integration tests for complete flow
└── conftest.py                  # Test configuration

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
