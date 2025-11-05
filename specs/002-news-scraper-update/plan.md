# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature implements an environment configuration system for the dual-source financial news scraper to externalize the URLs and settings. Instead of hardcoding the CNN and CNBC business URLs in the parser modules, the application will load these values from environment variables, with the ability to specify them in a .env file. This allows for easier configuration changes without modifying source code and provides better flexibility for different environments (development, testing, production).

Key changes include:
1. Implementation of a configuration loader module using python-dotenv
2. Updates to both CNN and CNBC parsers to accept configurable URLs
3. Enhancement of the date filtering system to use configurable timeframes
4. Updates to the rate limiter to use configurable delays
5. Implementation of content validation with minimum length checks (50 characters)
6. Implementation of a retry mechanism with exponential backoff (3 attempts)
7. Implementation of multiple CSS selectors as fallbacks for parsing
8. Implementation of controlled concurrency (maximum 3 concurrent tasks)

The design maintains all existing functionality while adding configurability, and adheres to the project's core principles of modularity, robust error handling, efficiency with asynchronous requests, timeliness enforcement, and data integrity.

## Technical Context

**Language/Version**: Python 3.12.7  
**Primary Dependencies**: httpx (for modern, asynchronous HTTP requests), BeautifulSoup4 (for HTML parsing and data extraction), python-dateutil (for date/time parsing and timezone handling), python-dotenv (for configuration management)  
**Storage**: File-based (Markdown output files)  
**Testing**: pytest (for unit and integration tests)  
**Target Platform**: Linux/Mac/Windows server environment  
**Project Type**: Single project with scraping functionality  
**Performance Goals**: Efficient scraping with 3-5 second rate limiting between requests, concurrent scraping from both sources using asyncio, with 80% success rate for content extraction within 30 seconds per article  
**Constraints**: Must only process articles published within 72 hours; needs to handle rate limiting and avoid being blocked by websites; limit memory usage to under 500MB during normal operation  
**Scale/Scope**: Designed for daily scraping of financial news from CNN and CNBC business sections

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Check

- ✅ **Modularity and Readability**: The design maintains clear separation of concerns with distinct modules for web scraping (Parsing), date filtering (Filtering), and data storage (Output). Configuration is isolated in its own module.
- ✅ **Robust Error Handling**: The design includes comprehensive error handling for network request failures, page structure changes, and content validation failures with retry mechanisms.
- ✅ **Efficiency with Asynchronous Requests**: The design uses efficient asynchronous patterns with Python's asyncio and httpx library to maximize throughput when scraping multiple news sources concurrently.
- ✅ **Timeliness Enforcement**: Strict date checking logic is built into the system - only news published within a configurable timeframe (default 72 hours) will be processed.
- ✅ **Data Integrity and Testing Standards**: The design includes validation for content quality (minimum 50 characters) and maintains all required fields throughout the processing pipeline.

### Gates

- [GATE 1] Are configuration changes isolated from business logic? ✅ Yes
- [GATE 2] Does implementation maintain existing error handling? ✅ Yes
- [GATE 3] Will the approach maintain current performance with controlled concurrency? ✅ Yes
- [GATE 4] Are all required fields still properly validated? ✅ Yes
- [GATE 5] Does the design handle external API changes gracefully with multiple selectors? ✅ Yes

### Post-Implementation Check

- ✅ **Modularity**: Configuration loading is isolated in separate module with clear interfaces
- ✅ **Error Handling**: Proper fallbacks exist when environment variables are missing; retry mechanism implemented
- ✅ **Efficiency**: Asynchronous patterns maintained with configurable concurrency limits
- ✅ **Timeliness**: Date filtering logic updated to use configurable timeframe while maintaining enforcement
- ✅ **Data Integrity**: Content validation with minimum length check (50 characters) implemented
