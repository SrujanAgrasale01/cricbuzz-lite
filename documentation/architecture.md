# Architecture and implementation notes

## Layers

- **UI:** `app.py` renders Home, Live Matches, Top Player Stats, SQL Analytics, and Player CRUD.
- **API:** `api_client.py` handles HTTP, headers, timeout, retries, JSON validation, and provider configuration.
- **Persistence:** `db.py` owns connections, transactions, schema setup, parameterized CRUD, and DataFrame queries.
- **Analytics:** `sql/queries.sql` contains 25 numbered exercises; `analytics.py` loads and executes them.
- **Configuration:** `config.py` reads `.env` values without embedding secrets.
- **Data:** `seed.py` supplies deterministic demo data so the project is useful without external credentials.

## Data flow

```text
Streamlit page
  → service/helper function
    → API client or parameterized SQL
      → normalized database
        → pandas DataFrame
          → table/chart in Streamlit
```

## Production improvements

- Add authentication and role-based access for CRUD.
- Add an ingestion job that upserts API data rather than duplicating rows.
- Add PostgreSQL support through SQLAlchemy or a repository interface.
- Add structured logging and metrics.
- Add API response contract tests using recorded fixtures.
- Add data freshness timestamps and cache invalidation.
- Add migrations with Alembic for schema changes.
