# Cricbuzz LiveStats

A modular Streamlit cricket analytics dashboard using Python, SQLite, SQL, pandas, and a configurable Cricbuzz-compatible REST API.

## Features

- Live match retrieval through a configurable REST API with local fallback data
- Top batting and bowling statistics
- 25 SQL analytics exercises from beginner to advanced level
- Player CRUD operations with validation and parameterized SQL
- SQLite schema with teams, players, venues, series, matches, innings, batting, bowling, and fielding tables
- Seed data for an immediately runnable demonstration
- Tests for database initialization and CRUD behavior
- Dockerfile for deployment

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. On first launch, the app automatically creates and seeds the demo database when it is empty. Run `python seed.py` manually only when you want to reset the demo data.

## API configuration

Copy `.env.example` to `.env` and configure:

```env
DATABASE_PATH=data/cricket.db
CRICBUZZ_BASE_URL=https://your-provider.example/api
CRICBUZZ_API_KEY=replace-me
CRICBUZZ_API_AUTH_TYPE=header
CRICBUZZ_API_KEY_HEADER=x-api-key
CRICBUZZ_EXTRA_HEADERS_JSON={"x-rapidapi-host":"cricbuzz-cricket.p.rapidapi.com"}
CRICBUZZ_LIVE_MATCHES_ENDPOINT=matches/live
CRICBUZZ_LIVE_MATCHES_PARAMS={"status":"live"}
CRICBUZZ_SCORECARD_ENDPOINT=mcenter/v1/{match_id}/scard
REQUEST_TIMEOUT_SECONDS=15
```

The client supports API keys in a header (`header`), bearer tokens (`bearer`), or query parameters (`query`). Change `CRICBUZZ_LIVE_MATCHES_ENDPOINT` when the provider uses a path such as `matches/live`. The API client also recognizes common response wrappers such as `data`, `matches`, `results`, and `response`, then normalizes common match fields for the dashboard. When no API settings are present, Live Matches uses the seeded local database.

For the RapidAPI Cricbuzz provider, use `x-rapidapi-key` as the key header and add the `x-rapidapi-host` extra header. The scorecard endpoint is ready for match IDs such as `40381`. Only the secret key needs to be kept private; the rest of the request handling is ready: retries, timeouts, JSON validation, authentication formatting, response extraction, normalization, raw-response inspection, and local fallback.

## Project structure

```text
Cricbuzz_LiveStats/
├── app.py                 # Streamlit entry point and dashboard pages
├── config.py              # Environment-backed configuration
├── db.py                  # SQLite connection, schema, CRUD, and query helpers
├── api_client.py          # Configurable REST client with retries and caching
├── analytics.py           # SQL query registry and execution helpers
├── seed.py                # Creates schema and demo data
├── schema.sql             # Normalized relational schema
├── requirements.txt
├── Dockerfile
├── .env.example
├── sql/queries.sql        # All 25 analytics queries
├── data/                  # Runtime database location
├── tests/                 # Automated tests
└── documentation/         # Design and deployment notes
```

## Data model

The schema is normalized around stable IDs. A match references a series and venue; `match_teams` stores both participating teams and the winner; `innings` connects a match to batting and bowling performance rows; performance tables connect back to players. This allows the same player, team, venue, and series to be reused across many matches.

## API and data quality notes

- API responses are external and may change; the API client validates that a JSON object/list was returned.
- Live APIs may not provide enough historical data for every analytical question. Seed or historical ingestion data is therefore retained for the SQL module.
- Secrets are loaded from environment variables and are never written into the repository.
- All database writes use parameterized SQL and transactions.

## Testing

```bash
pytest -q
```

## Docker

```bash
docker build -t cricbuzz-livestats .
docker run --rm -p 8501:8501 cricbuzz-livestats
```

## Learning roadmap

1. Read `documentation/architecture.md`.
2. Run `python seed.py` and inspect the schema.
3. Use the Analytics page and study one query at a time.
4. Configure the API only after understanding the local data flow.
5. Extend the schema or replace SQLite with PostgreSQL behind `db.py`.
