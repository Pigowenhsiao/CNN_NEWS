# Feature Specification: Dual Source Financial News Scraper

**Feature Branch**: `001-news-scraper`  
**Created**: 2025-11-03  
**Status**: Draft  
**Input**: User description: "目的 (Goal)： 建立一個高效且穩健的新聞抓取工具，專門用於追蹤和彙整 CNBC 和 CNN 財經版塊的最新報導，以確保資料的即時性和關聯性。 使用者故事 (User Stories)： 作為使用者，我需要工具能夠訪問 CNBC Business (https://www.cnbc.com/business/) 和 CNN Business (https://www.cnn.com/business) 這兩個頁面。 作為使用者，我需要工具能夠識別每個來源頁面上的所有新聞標題和對應的 URL。 作為使用者，我需要工具能夠對每個標題執行嚴格的日期檢查，只處理發布時間在最近三天內的新聞，以避免抓取過時資訊。 作為使用者，對於通過日期檢查的標題，我需要工具能跟蹤其連結，抓取完整的新聞內文。 作為使用者，我需要所有抓取到的資料（包括標題、內文、URL 和準確的發布日期）都能以結構化的格式寫入指定的 Markdown 檔案。 功能性需求 (Functional Requirements)： 來源處理：支援同時處理 CNBC 和 CNN 頁面結構，並針對兩者建立獨立的抓取邏輯。 標題與 URL 提取：成功從兩個來源的首頁列表中提取新聞標題與文章 URL。 時間過濾 (核心約束)： 必須能夠解析兩個網站文章中的發布時間。 僅允許時間戳記（Timestamp）在執行當下72 小時（三天）內的文章被處理。 內容提取：進入文章 URL 後，成功提取文章的完整文字內容（內文）。 輸出格式： 最終輸出必須寫入一個單一的 Markdown 檔案。 檔案命名格式必須為：US_News_yyyymmdd-hhmm.md (例如：US_News_20251102-2023.md)。 每個新聞條目在 Markdown 檔案中應以清晰、結構化的格式呈現，並包含：來源網站、標題、發布日期 (格式為 YYYY-MM-DD HH:MM:SS)、原始連結 (URL) 和 新聞內文 (Content)。"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Dual Source News Scraping (Priority: P1)

As a user, I need the tool to access CNBC Business (https://www.cnbc.com/business/) and CNN Business (https://www.cnn.com/business) pages to gather the latest financial news articles.

**Why this priority**: This is the foundational functionality that enables all other features. Without the ability to access both sources, the tool cannot fulfill its primary purpose.

**Independent Test**: The tool can successfully retrieve web pages from both CNBC and CNN business sections and identify news titles with corresponding URLs on each page.

**Acceptance Scenarios**:

1. **Given** a configured news scraper tool, **When** I run the scraping function targeting both CNBC and CNN business sections, **Then** the tool successfully accesses both pages and returns a list of news titles and URLs from each source.
2. **Given** the tool is running, **When** there are network connectivity issues with one of the sources, **Then** the tool continues to process the available source and logs the issue with the unavailable source.

---

### User Story 2 - Date Filtering and Content Extraction (Priority: P2)

As a user, I need the tool to perform strict date checking on articles and extract complete content from articles published within the last 72 hours, to avoid outdated information.

**Why this priority**: This ensures data quality and relevance, which is critical for financial news where timeliness is essential.

**Independent Test**: The tool correctly identifies articles published within the last 72 hours and retrieves the full text content from those articles' URLs while skipping older articles.

**Acceptance Scenarios**:

1. **Given** a list of news articles with publication dates, **When** the tool processes these articles, **Then** it only processes articles published within the last 72 hours and skips all others.
2. **Given** a valid article URL that passes the date check, **When** the tool follows the URL, **Then** it extracts the complete article content including text, title, and publication date.

---

### User Story 3 - Structured Output Generation (Priority: P3)

As a user, I need all scraped data to be written to a structured Markdown file with a specific naming convention to ensure consistent access to the information.

**Why this priority**: This provides the final output in a usable format that meets the user's requirements for accessing and organizing the news data.

**Independent Test**: The tool creates a properly formatted Markdown file following the naming convention (US_News_yyyymmdd-hhmm.md) containing all successfully scraped articles with their source, title, date, URL, and content.

**Acceptance Scenarios**:

1. **Given** a collection of scraped articles that passed the date filter, **When** the output function is executed, **Then** a Markdown file is created with the correct naming convention and properly structured entries for each article.
2. **Given** the output process is initiated, **When** the output directory doesn't exist, **Then** the tool creates the necessary directories before writing the file.

### Edge Cases

- What happens when one of the source websites changes its HTML structure?
- How does the system handle articles without publication dates?
- What if the tool encounters a malformed URL or broken link?
- How does the system handle network timeouts or rate limiting from the news websites?
- What if the same article appears on both sources? (resolved: deduplication by title)
- How does the system handle geolocation-based content? (resolved: ignore geolocation issues)

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST be able to access both CNBC Business (https://www.cnbc.com/business/) and CNN Business (https://www.cnn.com/business) pages to retrieve news listings
- **FR-002**: System MUST identify all news titles and their corresponding URLs from both source pages
- **FR-003**: System MUST parse publication timestamps from individual news articles
- **FR-004**: System MUST filter articles to only process those published within 72 hours of execution time
- **FR-005**: System MUST follow valid article URLs to extract complete article content (full text)
- **FR-006**: System MUST write all successfully processed articles to a single Markdown file
- **FR-007**: Output file MUST follow the naming convention: US_News_yyyymmdd-hhmm.md (e.g., US_News_20251102-2023.md)
- **FR-008**: Each article entry in the output file MUST include: source website, title, publication date (formatted as YYYY-MM-DD HH:MM:SS), URL, and article content
- **FR-009**: System MUST handle both CNBC and CNN page structures with independent scraping logic for each source
- **FR-010**: System MUST implement rate limiting by waiting 3-5 seconds between each request to avoid being blocked by websites
- **FR-011**: System MUST implement deduplication by article title to prevent duplicate entries in output
- **FR-012**: System MUST log all levels including debug information for troubleshooting purposes
- **FR-013**: System MUST automatically clean up output files after 30 days to prevent unbounded storage growth

### Key Entities *(include if feature involves data)*

- **News Article**: Represents an individual news piece with id, title, content, URL, publication date, and source website
- **News Source**: Represents the origin of news articles (CNBC Business or CNN Business), with specific parsing logic for each
- **Scraping Result**: Contains the collected data from the scraping process, including successfully processed articles and any errors encountered
- **Output File**: The structured Markdown document containing all processed articles with required metadata

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: The system successfully accesses both CNBC and CNN business pages at least 95% of the time under normal network conditions
- **SC-002**: At least 80% of identified article links result in successful content extraction within 30 seconds per article
- **SC-003**: The system correctly filters articles to only include those published within 72 hours, with 99% accuracy in date parsing
- **SC-004**: The output Markdown file is generated within 5 minutes of execution with all required fields (source, title, date, URL, content) properly formatted for each article
- **SC-005**: Users can reliably find and access timely financial news from both sources in a single organized Markdown file

## Clarifications

### Session 2025-11-03

- Q: 應採用哪種速率限制策略？ → A: 每隔 3-5 秒發送一個請求
- Q: 應如何處理地理定位問題？ → A: 完全忽略地理定位問題
- Q: 應採用哪種重複檢測策略？ → A: 僅基於標題進行重複檢測
- Q: 應採用哪種日誌記錄策略？ → A: 記錄所有級別的日誌（包括調試）
- Q: 應採用哪種數據保留策略？ → A: 保留輸出文件 30 天後自動清理