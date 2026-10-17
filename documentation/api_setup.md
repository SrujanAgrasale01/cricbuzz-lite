# API provider setup

The API client is ready for a provider-specific key and endpoint.

## 1. Copy the environment template

```bash
cp .env.example .env
```

## 2. Fill in the provider values

```env
CRICBUZZ_BASE_URL=https://provider.example/api
CRICBUZZ_API_KEY=your-key
CRICBUZZ_API_AUTH_TYPE=header
CRICBUZZ_API_KEY_HEADER=x-api-key
CRICBUZZ_LIVE_MATCHES_ENDPOINT=matches/live
CRICBUZZ_LIVE_MATCHES_PARAMS={"status":"live"}
```

Supported authentication modes:

- `header`: sends `CRICBUZZ_API_KEY` using `CRICBUZZ_API_KEY_HEADER`.
- `bearer`: sends `Authorization: Bearer <key>`.
- `query`: sends the key using `CRICBUZZ_API_KEY_PARAM`.

## RapidAPI Cricbuzz configuration

For the RapidAPI provider used by this project, the relevant settings are:

```env
CRICBUZZ_BASE_URL=https://cricbuzz-cricket.p.rapidapi.com
CRICBUZZ_API_AUTH_TYPE=header
CRICBUZZ_API_KEY_HEADER=x-rapidapi-key
CRICBUZZ_EXTRA_HEADERS_JSON={"x-rapidapi-host":"cricbuzz-cricket.p.rapidapi.com"}
CRICBUZZ_SCORECARD_ENDPOINT=mcenter/v1/{match_id}/scard
```

The scorecard endpoint is ready in the dashboard. Enter a provider match ID, such as `40381`, on the **Live Matches** page and choose **Fetch scorecard**.

## 3. Verify the connection

```bash
python - <<'PY'
from api_client import CricketAPIClient
client = CricketAPIClient()
print(client.configuration_message)
print(client.normalize_live_matches(client.live_matches()))
PY
```

## 4. Run the dashboard

```bash
streamlit run app.py
```

Open **Live Matches** and click **Refresh from configured API**. The page displays normalized common fields and keeps the raw provider response in an expandable panel for field mapping.

## Provider-specific field mapping

The client recognizes common aliases for IDs, descriptions, statuses, formats, dates, venues, and team names. If the selected provider uses different field names, update `normalize_live_matches()` in `api_client.py`. No Streamlit page changes are required.

## Security

Never commit `.env` or expose the key in logs, screenshots, or Streamlit output. Keep the local seeded data available for analytics because live APIs often do not provide enough historical records for all 25 SQL questions.
