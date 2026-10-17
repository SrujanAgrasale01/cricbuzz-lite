# Cricbuzz LiveStats — Phase 1: Project Understanding

## 1. Phase Objective

This phase converts the project brief into a clear technical and business understanding. No production code is written yet. The goal is to understand **what is being built, why it is being built, which technologies are required, and how the major modules fit together**.

The project is titled **Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics**.

The application will combine:

- Live cricket data obtained through a REST API
- A relational SQL database for storing and querying cricket data
- Python services for API integration and business logic
- A Streamlit dashboard for user interaction
- SQL analytics covering beginner, intermediate, and advanced use cases
- CRUD operations for managing player and match-related records

---

## 2. Business Problem

Cricket information is usually distributed across live-score websites, APIs, spreadsheets, and historical databases. A user may be able to see a live score in one place, player statistics in another place, and historical analysis somewhere else.

This project addresses that fragmentation by creating one application that can:

1. Retrieve current cricket information from an API.
2. Store structured match, player, team, venue, and performance data.
3. Allow users to query the data using SQL-driven analytics.
4. Present results through an interactive dashboard.
5. Support controlled data management through CRUD operations.

### Business value

The project is useful for several audiences:

- **Sports media and broadcasting:** Live updates, player comparisons, and historical trends for commentary and pre-match analysis.
- **Fantasy cricket platforms:** Recent player form, head-to-head records, and performance indicators for team selection.
- **Cricket analytics firms:** Player evaluation, format-wise performance, venue analysis, and trend modeling.
- **Educational institutions:** A realistic project for learning Python, SQL, APIs, databases, and Streamlit.
- **Sports prediction and betting analysis:** Historical performance, toss impact, momentum, and venue-specific statistics. Any production use in regulated betting contexts would require additional legal, data-quality, and compliance review.

### Core problem statement

> Build a comprehensive cricket analytics dashboard that integrates live data from the Cricbuzz API with a SQL database to create an interactive web application.

The solution should provide real-time match updates, SQL-based player and match analytics, and full CRUD operations for selected data entities.

---

## 3. Project Objective

The primary objective is to build a **user-friendly, modular, and educational cricket analytics platform** that demonstrates end-to-end data application development.

The application should allow a user to:

- View ongoing and recent cricket matches.
- See scorecards, match status, teams, players, and venue information.
- View top batting and bowling statistics.
- Execute or browse a library of 25 SQL analytics questions.
- Add, view, update, and delete selected player or match records.
- Learn how API data moves into a relational database and becomes dashboard insight.

### Technical objective

The application should demonstrate the following pipeline:

```text
External cricket API
        ↓
API client and validation layer
        ↓
Transformation and service layer
        ↓
Relational SQL database
        ↓
SQL analytics and CRUD services
        ↓
Streamlit user interface
```

### Learning objective

The project is also designed as a guided learning exercise. The learner should understand concepts before implementing them, follow modular design, use PEP 8 conventions, handle errors properly, and build the application incrementally rather than generating one large script.

---

## 4. Expected Deliverables

The project brief expects the following deliverables:

### Application deliverables

- A complete Python application.
- A Streamlit dashboard with the required pages or modules.
- Live match integration using a Cricbuzz-compatible cricket REST API.
- Top player statistics.
- SQL analytics for the 25 specified questions.
- CRUD functionality for relevant player and match data.

### Database deliverables

- Database schema.
- Table definitions and relationships.
- Primary keys, foreign keys, constraints, and indexes where appropriate.
- Sample or seeded data.
- SQL queries for the analytics module.

### Documentation deliverables

- Project setup instructions.
- Installation instructions.
- API key configuration instructions.
- Database configuration instructions.
- Folder structure explanation.
- Usage instructions.
- Future-improvement notes.

### Engineering deliverables

- `requirements.txt` or an equivalent dependency file.
- Secure handling of API keys and database credentials.
- Modular source code.
- Error handling for API and database operations.
- Comments and docstrings for important functions.
- Git-based version control.

### Demonstration deliverables

- A working demonstration of the dashboard.
- A recording video showing the project and its modules.

### Project constraint

The project is expected to be completed and submitted within **14 days from the assignment date**. The detailed schedule should be converted into milestones so that the database and API foundations are completed before the dashboard polish and recording.

---

## 5. Required Technologies

| Area | Technology or approach | Purpose |
|---|---|---|
| Programming language | Python | Application logic, API integration, transformations, and services |
| User interface | Streamlit | Interactive multi-page web dashboard |
| Database | PostgreSQL, MySQL, or SQLite | Persistent storage and relational analytics |
| Query language | SQL | Data retrieval, aggregation, reporting, and analytics |
| Data exchange | JSON | Common format for API responses and normalized data transfer |
| External integration | REST API | Fetch live matches, scorecards, players, and series information |
| Data handling | pandas | Tabular transformations and dashboard-friendly data preparation |
| HTTP communication | Python `requests` library | Calling the cricket API |
| Version control | Git | Tracking changes and collaboration |
| Documentation | Markdown and optionally generated project documents | Setup, architecture, usage, and learning notes |

### Recommended initial database choice

For learning and local development, **SQLite** is the easiest starting point because it requires no separate database server. The project brief also expects database-agnostic design, so the code should isolate connection handling and SQL differences behind a small database utility layer.

For deployment or multi-user use, **PostgreSQL** is generally a stronger target because it supports concurrent access, robust constraints, indexes, and production-grade operations. The final database choice should be confirmed before implementation.

---

## 6. Required Python Libraries

The brief explicitly identifies these dependencies:

| Library | Role |
|---|---|
| `streamlit` | Build the dashboard and interactive pages |
| Database connector | Connect Python to SQLite, PostgreSQL, or MySQL |
| `requests` | Call REST API endpoints |
| `pandas` | Transform, filter, aggregate, and display tabular data |

Additional libraries may be selected during later phases, depending on the database and deployment target:

- `python-dotenv` for local environment variables.
- `SQLAlchemy` for database abstraction and connection management.
- A PostgreSQL driver such as `psycopg2-binary` or `asyncpg`, depending on the design.
- A MySQL driver if MySQL is selected.
- `pytest` for testing.
- A retry library such as `tenacity`, or a small custom retry utility.
- A plotting library supported by Streamlit, such as Plotly, for richer visualizations.

These additional dependencies should not be added indiscriminately. Each should have a clear purpose and be documented in the requirements file.

---

## 7. Required APIs

The project requires a **Cricbuzz-compatible cricket REST API**. The API is expected to provide some combination of:

- Current or live matches.
- Match summaries and scorecards.
- Teams and players.
- Series information.
- Venues and match locations.
- Batting and bowling statistics.
- Match status, dates, results, and victory details.

The project brief refers to the “Cricbuzz API” but does not specify a precise provider, subscription plan, base URL, authentication method, endpoint list, or rate-limit policy. These details must be verified during **Phase 5: API Analysis** before implementation.

### Important API design principle

The application should not allow the Streamlit pages to call the external API directly. Instead, API calls should be isolated in an API client or service layer:

```text
Streamlit page → service function → API client → external API
```

This separation makes it easier to:

- Test the application without constantly calling the API.
- Replace the API provider later.
- Add retries, timeouts, caching, and logging.
- Normalize inconsistent JSON responses.
- Protect API keys and headers.

### API concerns to confirm later

- Exact provider and documentation.
- Authentication and API-key format.
- Required headers.
- Available endpoints.
- Response schemas.
- Pagination behavior.
- Rate limits and quotas.
- Licensing and permitted use of the data.
- Whether historical data required by the 25 SQL questions is available.

A major project risk is that live API data alone may not contain enough historical records for all 25 analytical queries. A separate seed dataset or historical data ingestion strategy may therefore be necessary.

---

## 8. Required SQL Knowledge

The project deliberately progresses from basic SQL to advanced analytical SQL.

### Beginner concepts

Questions 1–8 require:

- `SELECT`
- `WHERE`
- `ORDER BY`
- `GROUP BY`
- Aggregate functions such as `COUNT`, `SUM`, `AVG`, and `MAX`
- Basic joins
- Date filtering
- Filtering by country, format, role, or capacity

### Intermediate concepts

Questions 9–16 require:

- Multi-table joins
- Conditional aggregation
- Subqueries
- `CASE` expressions
- Date and time extraction
- Group-level filtering with `HAVING`
- Comparing home and away performance
- Partnership and innings analysis
- Filtering based on minimum participation thresholds

### Advanced concepts

Questions 17–25 require:

- Common table expressions using `WITH`
- Window functions such as `ROW_NUMBER`, `RANK`, `LAG`, and running aggregates
- Standard deviation and other statistical aggregates
- Conditional and weighted scoring
- Percentages and ratios
- Time-series analysis
- Ranking and categorization
- Multiple levels of aggregation
- Query optimization and index awareness

### SQL learning approach

The prompt specifically requires solving **one SQL question at a time**. Each question should be explained through:

1. Business problem.
2. SQL concepts.
3. Tables involved.
4. Relationships.
5. Query logic.
6. Execution or optimization considerations.
7. SQL query.
8. Line-by-line explanation.

The next SQL question should not be started until the learner says **NEXT**.

---

## 9. Required Streamlit Components

The expected dashboard contains the following application areas:

### Home page

Purpose:

- Explain the project.
- Describe tools and technologies.
- Provide navigation guidance.
- Link to documentation and folder structure information.

Likely components:

- Title and project summary.
- Metric cards.
- Instructions.
- Navigation links or sidebar navigation.
- Project status information.

### Live Match page

Purpose:

- Show ongoing matches from the cricket API.
- Display scores, match status, teams, players, and venues.

Likely components:

- Match selector.
- Refresh control.
- Status badges or text.
- Scorecard tables.
- Team and venue sections.
- Expanders for innings or detailed player information.

### Top Player Stats page

Purpose:

- Display top batting and bowling statistics.
- Support categories such as runs, highest score, wickets, and related metrics.

Likely components:

- Format selector.
- Statistic category selector.
- Data tables.
- Bar charts or ranking cards.
- Filters by team, date, or competition where data permits.

### SQL Queries & Analytics page

Purpose:

- Expose the 25 SQL practice questions.
- Display query outputs in an understandable format.

Likely components:

- Query dropdown or numbered question selector.
- Explanation panel.
- Results table.
- Optional chart based on the result.
- Clear error message when data is insufficient.

### CRUD Operations page

Purpose:

- Allow authorized users or learners to manage selected player and match records.

Likely components:

- Create form.
- Read/search table.
- Update form.
- Delete selector with a safety warning.
- Validation messages.
- Success and failure notifications.

### Settings page

The mentoring prompt includes a Settings page even though the original project brief emphasizes four main modules. This page can be treated as a useful extension for:

- Database status.
- API configuration status without exposing secrets.
- Cache clearing.
- Display preferences.
- Environment information.

Authentication is not explicitly required in the project brief. If CRUD operations are exposed publicly, authentication and authorization become important future or production requirements.

---

## 10. Database Requirements

The application needs a relational database capable of representing cricket entities and performance data.

Likely entities include:

- Players
- Teams
- Venues
- Series
- Matches
- Match teams or match participants
- Innings
- Batting performances
- Bowling performances
- Fielding performances
- Player roles and formats, either as attributes or normalized reference tables

The final schema will be designed in Phase 4. At this stage, the key requirements are:

- Use stable primary keys.
- Define foreign-key relationships.
- Avoid unnecessary duplication through normalization.
- Add constraints for valid dates, scores, roles, and formats.
- Add indexes to fields frequently used in filtering and joins.
- Keep database connection logic centralized.
- Use parameterized SQL to avoid injection vulnerabilities.
- Use transactions for create, update, and delete operations.
- Handle missing or incomplete API fields safely.

The project brief specifically mentions a centralized connection utility such as:

```text
utils/db_connection.py
```

The exact filename may be refined when the final folder structure is created.

---

## 11. Why Each Module Exists

### API integration module

This module obtains live or historical cricket data from the external provider. It isolates external communication from the rest of the application.

### Data transformation or ingestion module

API JSON is usually nested and may not match the database schema directly. This module validates, cleans, maps, and transforms API responses before persistence.

### Database module

This module manages connections, transactions, schema access, and database-specific behavior. Centralization prevents every page from implementing its own connection logic.

### Models or schema module

This module represents entities and their relationships. It makes the data structure easier to understand and reduces inconsistent field naming.

### Services module

This module contains business rules, such as retrieving live matches, calculating top players, or applying CRUD validation. Streamlit pages should call services instead of containing all business logic.

### SQL analytics module

This module stores and executes the 25 analytical queries. Keeping queries separate makes them easier to explain, test, optimize, and maintain.

### CRUD module

This module supports controlled creation, reading, updating, and deletion of records. It demonstrates database manipulation and transaction handling.

### Streamlit pages module

This module contains the user-facing pages. Each page should focus on layout and interaction while delegating data operations to services.

### Configuration module

This module loads environment-specific values such as API keys, database URLs, timeouts, and feature flags without hardcoding secrets.

### Utility module

This module contains reusable helpers such as formatting, logging, validation, date conversion, and error display preparation.

### Testing module

Tests protect the project from regressions and demonstrate professional engineering practices. Unit, integration, API, database, and UI-level testing can be introduced progressively.

### Documentation module

Documentation allows another person to install, understand, run, demonstrate, and extend the project.

---

## 12. High-Level Development Roadmap

The project should be built in the following order:

1. **Understand and finalize requirements.**
2. **Set up the Python and Streamlit environment.**
3. **Choose the database and design the schema.**
4. **Create tables, constraints, indexes, and seed data.**
5. **Verify the cricket API and build a safe API client.**
6. **Ingest and normalize API data into the database.**
7. **Build CRUD operations and validation.**
8. **Implement the SQL analytics queries one by one.**
9. **Build Streamlit pages around tested services.**
10. **Add visualizations, caching, and usability improvements.**
11. **Test the complete application.**
12. **Document, deploy, record, and prepare the presentation or demo.**

This order is intentional. Building the user interface first would create unstable screens because the API response structure and database schema would not yet be settled.

---

## 13. Proposed 14-Day Timeline

| Days | Focus | Expected result |
|---|---|---|
| 1 | Requirements and environment setup | Confirm scope, create repository, install dependencies |
| 2 | Database design | Draft ER model, tables, keys, and relationships |
| 3 | Database implementation | Create schema, indexes, constraints, and seed data |
| 4 | API research and client foundation | Confirm provider, endpoints, authentication, timeouts, and error handling |
| 5 | API ingestion | Fetch, validate, transform, and persist representative data |
| 6 | CRUD operations | Implement create, read, update, delete, validation, and transactions |
| 7 | SQL analytics: beginner | Implement and test questions 1–8 |
| 8 | SQL analytics: intermediate | Implement and test questions 9–16 |
| 9 | SQL analytics: advanced | Implement and test questions 17–25 |
| 10 | Home and Live Match pages | Build core dashboard navigation and live match view |
| 11 | Top Stats and Analytics pages | Add rankings, query selection, tables, and visualizations |
| 12 | CRUD, Settings, and error states | Complete management screens and improve resilience |
| 13 | Testing, documentation, and deployment preparation | Test critical paths, finalize README, prepare deployment |
| 14 | Demo and recording | Run the complete workflow, capture screenshots/video, and package submission |

The timeline is a target rather than a reason to skip validation. If the API or historical data is difficult to obtain, the project should preserve a reliable local sample dataset so that the SQL and dashboard modules remain demonstrable.

---

## 14. Key Assumptions and Risks

### Assumptions

- The application is primarily educational but should follow professional structure.
- The selected API provides enough current cricket information for the Live Match page.
- A local or seeded dataset can support historical SQL exercises where the API does not provide sufficient history.
- The first implementation can use SQLite, with a path to PostgreSQL.
- Streamlit is the primary interface rather than a separate JavaScript frontend.

### Risks

1. **API ambiguity:** The exact Cricbuzz API provider is not named.
2. **Historical data shortage:** Live APIs may not provide the historical depth needed for 25 queries.
3. **Schema mismatch:** Nested API JSON may not map directly to normalized tables.
4. **Data quality:** Missing player roles, venues, dates, scores, or bowling statistics may affect analytics.
5. **Rate limits:** Frequent dashboard refreshes could exhaust API quotas.
6. **Scope expansion:** Authentication, deployment, visual polish, and 25 advanced queries can exceed a 14-day schedule if not prioritized.
7. **Destructive CRUD actions:** Delete functionality needs validation, transactions, and an appropriate access-control strategy.

### Recommended scope boundary

The minimum viable project should prioritize:

- Reliable database schema.
- Working API integration for representative live data.
- Four primary modules: Live Match, Top Player Stats, SQL Analytics, and CRUD.
- All 25 query definitions, with documented data requirements.
- Clear documentation and a working demonstration.

Advanced authentication, automated data pipelines, predictive models, and production-scale deployment should be treated as future improvements unless the core system is already stable.

---

## 15. Phase 1 Completion Summary

### What we completed

- Defined the business problem.
- Explained the project objective.
- Identified expected deliverables.
- Listed the required technologies and likely Python libraries.
- Clarified the role of the Cricbuzz-compatible API.
- Mapped the SQL knowledge progression.
- Identified the required Streamlit pages and components.
- Explained why each major module exists.
- Created a high-level development roadmap.
- Proposed a 14-day execution timeline.
- Documented assumptions and risks.

### Files created

- `Cricbuzz_Phase_1_Project_Understanding.md`

### Concepts learned

- Business requirements versus technical requirements.
- Separation of API, service, database, analytics, and UI layers.
- Why database schema design must precede dashboard implementation.
- How SQL complexity grows from aggregation to window functions and time-series analysis.
- Why live API data and historical analytics may require different ingestion strategies.
- How to prioritize a minimum viable project within a fixed timeline.

## Next Phase Preview: Phase 2 — Requirement Analysis

Phase 2 will extract every requirement from the project brief and classify it into:

- Mandatory features
- Optional features
- Bonus features
- Future improvements

It will also create a requirement checklist with completion status and clarify the minimum viable scope for the 14-day timeline.

Per the project instructions, implementation should not begin until the requirements have been analyzed and the scope is clear.
