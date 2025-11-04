---

description: "Task list for dual-source financial news scraper implementation"
---

# Tasks: Dual Source Financial News Scraper

**Input**: Design documents from `/specs/001-news-scraper/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are REQUIRED - based on testing standards from constitution requiring unit tests for date parsing/filtering, deduplication logic, rate limiting, and integration tests for complete flow.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/ directory
- [X] T002 Initialize Python project with httpx, beautifulsoup4, python-dateutil, pytest dependencies
- [X] T003 [P] Configure project virtual environment and requirements.txt
- [X] T004 [P] Configure linting with flake8 or pylint and formatting with black

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create base NewsArticle model in src/models/article.py
- [X] T006 [P] Create NewsSource model in src/models/source.py 
- [X] T007 [P] Create ScrapeResult model in src/models/result.py
- [X] T008 Create OutputFile model in src/models/output.py
- [X] T009 Configure comprehensive error handling and logging infrastructure in src/utils/helpers.py
- [X] T010 [P] Create utility functions for date/time parsing in src/utils/date_parser.py
- [X] T011 [P] Create rate limiter module in src/utils/rate_limiter.py with 3-5 second delays between requests
- [X] T012 Create deduplication module in src/deduplication.py with title-based duplicate detection

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dual Source News Scraping (Priority: P1) 🎯 MVP

**Goal**: Enable the tool to access CNBC Business (https://www.cnbc.com/business/) and CNN Business (https://www.cnn.com/business) pages to gather the latest financial news articles.

**Independent Test**: The tool can successfully retrieve web pages from both CNBC and CNN business sections and identify news titles with corresponding URLs on each page.

### Tests for User Story 1 (REQUIRED - constitution standards) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T013 [P] [US1] Unit test for CNN article parsing in tests/unit/test_cnn_parser.py
- [X] T014 [P] [US1] Unit test for CNBC article parsing in tests/unit/test_cnbc_parser.py

### Implementation for User Story 1

- [X] T018 [P] [US1] Create CNN parser module in src/cnn_parser.py implementing get_cnn_articles function
- [X] T019 [P] [US1] Create CNBC parser module in src/cnbc_parser.py implementing get_cnbc_articles function  
- [X] T020 [US1] Implement scraper coordinator in src/scraper.py with asyncio for concurrent scraping
- [X] T021 [US1] Add error handling for network connectivity issues in both parsers
- [X] T022 [US1] Add logging for scraping operations in src/scraper.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Date Filtering and Content Extraction (Priority: P2)

**Goal**: Perform strict date checking on articles and extract complete content from articles published within the last 72 hours, to avoid outdated information.

**Independent Test**: The tool correctly identifies articles published within the last 72 hours and retrieves the full text content from those articles' URLs while skipping older articles.

### Tests for User Story 2 (REQUIRED - constitution standards) ⚠️

- [X] T023 [P] [US2] Unit test for date filtering logic in tests/unit/test_date_filter.py
- [X] T024 [P] [US2] Unit test for date parsing function in tests/unit/test_date_filter.py
- [X] T025 [P] [US2] Unit test for deduplication logic in tests/unit/test_deduplication.py
- [X] T026 [P] [US2] Unit test for data integrity validation in tests/unit/test_data_integrity.py

### Implementation for User Story 2

- [X] T027 [P] [US2] Create date filtering module in src/utils/date_parser.py with is_within_72_hours function
- [X] T028 [P] [US2] Implement parse_article_date function in src/utils/date_parser.py for both sources
- [X] T029 [P] [US2] Create CNN content extraction in src/cnn_parser.py with extract_cnn_content function
- [X] T030 [P] [US2] Create CNBC content extraction in src/cnbc_parser.py with extract_cnbc_content function
- [X] T031 [US2] Integrate date filtering with content extraction in scraper logic
- [X] T032 [US2] Add validation to skip articles without publication dates
- [X] T033 [US2] Integrate deduplication logic using title-based detection in scraper workflow

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Structured Output Generation (Priority: P3)

**Goal**: All scraped data to be written to a structured Markdown file with a specific naming convention to ensure consistent access to the information.

**Independent Test**: The tool creates a properly formatted Markdown file following the naming convention (US_News_yyyymmdd-hhmm.md) containing all successfully scraped articles with their source, title, date, URL, and content.

### Tests for User Story 3 (REQUIRED - constitution standards) ⚠️

- [X] T034 [P] [US3] Unit test for output writer in tests/unit/test_output_writer.py
- [X] T035 [P] [US3] Unit test for filename generation in tests/unit/test_output_writer.py
- [X] T036 [P] [US3] Unit test for rate limiter functionality in tests/unit/test_rate_limiter.py

### Implementation for User Story 3

- [X] T037 [P] [US3] Create output writer module in src/output_writer.py with write_to_markdown function
- [X] T038 [US3] Implement generate_filename function in src/output_writer.py for US_News_yyyymmdd-hhmm.md format
- [X] T039 [US3] Format Markdown content with source, title, date, URL, and content per article
- [X] T040 [US3] Add directory creation functionality if output path doesn't exist
- [X] T041 [US3] Implement automatic cleanup of output files after 30 days in output_writer module

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Integration & Validation (REQUIRED - constitution standards)

**Goal**: Complete end-to-end functionality with integration testing as required by constitution standards

### Integration Tests ⚠️

- [X] T042 [P] [INTEGRATION] End-to-end integration test in tests/integration/test_end_to_end.py
- [X] T043 [P] [INTEGRATION] Integration test for rate limiting functionality in tests/integration/test_end_to_end.py
- [X] T044 [P] [INTEGRATION] Integration test for deduplication logic in tests/integration/test_end_to_end.py
- [X] T045 [P] [INTEGRATION] Integration test for data integrity validation in tests/integration/test_end_to_end.py

### Integration Implementation

- [X] T046 [INTEGRATION] Connect all components in scraper.py to implement complete workflow
- [X] T047 [INTEGRATION] Add final validation checks for all data requirements (FR-008)
- [X] T048 [INTEGRATION] Integrate rate limiting between each request to avoid being blocked by websites
- [X] T049 [INTEGRATION] Ensure comprehensive logging at all levels including debug information
- [X] T051 [INTEGRATION] Validate data integrity throughout processing pipeline

**Checkpoint**: Complete system with all user stories working together

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T052 [P] Documentation updates in README.md
- [X] T053 Code cleanup and refactoring following modularity principles
- [X] T054 Add retry mechanisms for HTTP request failures (implemented in safe_request_with_retry function)
- [X] T055 [P] Additional unit tests in tests/unit/
- [X] T056 Rate limiting implementation to respect website terms of service (already implemented in T011, T048)
- [X] T057 Run quickstart.md validation and update as needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Integration (Phase 6)**: Depends on all user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories and integration being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 models and infrastructure
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 and US2 for article data

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
T013 [P] [US1] Unit test for CNN article parsing in tests/unit/test_cnn_parser.py
T014 [P] [US1] Unit test for CNBC article parsing in tests/unit/test_cnbc_parser.py

# Launch all implementation modules for User Story 1 together:
T018 [P] [US1] Create CNN parser module in src/cnn_parser.py
T019 [P] [US1] Create CNBC parser module in src/cnbc_parser.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Complete Integration → Test end-to-end → Deploy
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2  
   - Developer C: User Story 3
3. Integration developer works on Phase 6 after all stories complete
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence