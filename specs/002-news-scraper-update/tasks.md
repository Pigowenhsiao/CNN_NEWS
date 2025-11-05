# Tasks: Dual Source Financial News Scraper Update

**Feature**: Dual Source Financial News Scraper Update  
**Branch**: `002-news-scraper-update` | **Spec**: specs/002-news-scraper-update/spec.md  
**Date**: 2025-11-05

## Dependencies

- **User Story 2**: Depends on User Story 1 (P2 priority)
- **User Story 3**: Depends on User Story 1 and User Story 2 (P3 priority)

## Parallel Execution Examples

- **Per Story**: 
  - US2: T008 [P] [US2] Update content validation in cnn_parser.py, T009 [P] [US2] Update content validation in cnbc_parser.py can run in parallel
  - US3: T015 [P] [US3] Update scraper concurrency control, T016 [P] [US3] Update deduplication logic can run in parallel

## Implementation Strategy

This feature implements an environment configuration system for the dual-source financial news scraper to externalize the URLs and settings. The implementation follows an incremental delivery approach:

1. **MVP (Phase 3)**: Complete dual source scraping with configuration (User Story 1)
2. **Phase 4**: Complete configurable date filtering and content extraction (User Story 2)
3. **Phase 5**: Complete structured output generation and all functional requirements (User Story 3)
4. **Phase 6**: Add advanced features and polish

---

## Phase 1: Setup

**Goal**: Initialize project structure and core dependencies

- [ ] T001 Create config directory structure: src/config/
- [ ] T002 [P] Add python-dotenv dependency to pyproject.toml
- [ ] T003 [P] Add python-dotenv to requirements.txt

## Phase 2: Foundational Components

**Goal**: Create the foundational configuration loading mechanism and base infrastructure

- [ ] T004 Create src/config/__init__.py
- [ ] T005 Create src/config/loader.py with load_config function implementation
- [ ] T006 Create .env file with default configuration values
- [ ] T007 [P] Verify memory usage limits in scraper execution

## Phase 3: User Story 1 - Dual Source News Scraping with Configuration

**Goal**: Implement configurable URLs for CNN and CNBC business sections

**Independent Test**: The tool can successfully retrieve web pages from both CNBC and CNN business sections using configured URLs and identify news titles with corresponding URLs on each page.

- [ ] T008 [P] [US1] Update src/cnn_parser.py to accept configurable URL parameter and use configuration
- [ ] T009 [P] [US1] Update src/cnbc_parser.py to accept configurable URL parameter and use configuration
- [ ] T010 [US1] Update scraper.py to pass configured URLs to parser functions
- [ ] T011 [US1] Test that parser functions work with both default and custom URLs

## Phase 4: User Story 2 - Configurable Date Filtering and Content Extraction

**Goal**: Make date filtering configurable rather than hardcoded to 72 hours and implement content validation

**Independent Test**: The tool correctly identifies articles published within the configured timeframe and retrieves the full text content from those articles' URLs while skipping older articles and validating content meets minimum requirements.

- [ ] T012 [US2] Update src/utils/date_filter.py to support configurable timeframes with is_within_timeframe function
- [ ] T013 [P] [US2] Update date filtering logic in scraper.py to use configurable timeframe
- [ ] T014 [P] [US2] Update cnbc_parser.py to import is_within_timeframe instead of is_within_72_hours
- [ ] T015 [P] [US2] Update content extraction in cnn_parser.py to validate minimum 50 characters
- [ ] T016 [P] [US2] Update content extraction in cnbc_parser.py to validate minimum 50 characters
- [ ] T017 [US2] Implement retry mechanism with 3 attempts in parser modules
- [ ] T018 [US2] Test date filtering and content validation with different configuration values

## Phase 5: User Story 3 - Full Configuration System with Advanced Features

**Goal**: Implement complete configuration system and all functional requirements from spec

**Independent Test**: The tool uses all configurable parameters correctly including rate limiting, retry logic, date filtering, concurrency limits, connection pooling, content caching, and enhanced deduplication while maintaining proper output formatting.

- [ ] T019 [US3] Update scraper.py to implement controlled concurrency (max 3 tasks) to optimize scraping time
- [ ] T020 [P] [US3] Update scraper.py to implement connection pooling for HTTP requests
- [ ] T021 [P] [US3] Implement content caching mechanism to avoid redundant processing
- [ ] T022 [US3] Enhance deduplication algorithm to consider content similarity in addition to title matching
- [ ] T023 [P] [US3] Update output_writer.py to validate minimum content length before writing
- [ ] T024 [P] [US3] Update output_writer.py to implement configurable naming convention
- [ ] T025 [P] [US3] Implement automatic cleanup of output files after 30 days
- [ ] T026 [US3] Validate all scraped data fields and provide default values for missing information
- [ ] T027 [US3] Ensure output formatting includes proper escaping and encoding
- [ ] T028 [US3] Ensure handling of articles with very long content without memory issues
- [ ] T029 [US3] Test complete workflow with various configuration combinations

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Enhance logging, error handling, and perform final testing

- [ ] T030 Implement comprehensive error handling for all network operations, parsing activities, and file operations
- [ ] T031 Update logging system to log all significant events with appropriate severity levels (DEBUG, INFO, WARN, ERROR)
- [ ] T032 Implement graceful recovery from network timeouts, DNS failures, and HTTP error responses
- [ ] T033 Ensure system continues processing when individual articles fail, without affecting overall execution
- [ ] T034 Add data integrity validation to ensure all required fields are properly stored
- [ ] T035 Update pyproject.toml with complete dependencies list
- [ ] T036 Update README.md with complete configuration documentation
- [ ] T037 Verify all configuration validation occurs at startup
- [ ] T038 Test complete end-to-end workflow with configuration
- [ ] T039 Document all environment variables in README.md