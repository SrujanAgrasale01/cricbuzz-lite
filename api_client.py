"""Provider-agnostic cricket REST API client.

Configure the provider through environment variables. The client supports API keys
in headers or query parameters, bearer tokens, extra provider headers such as the
RapidAPI host header, retries, timeouts, scorecards, and common JSON wrappers.
"""
from typing import Any
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import settings

class CricketAPIError(RuntimeError):
    """Raised when the configured cricket API cannot return valid data."""

class CricketAPIClient:
    def __init__(self):
        self.session = requests.Session()
        retry = Retry(total=2, backoff_factor=0.4, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=("GET",), respect_retry_after_header=True)
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    @property
    def configured(self) -> bool:
        return bool(settings.base_url)

    @property
    def configuration_message(self) -> str:
        if not settings.base_url:
            return "Set CRICBUZZ_BASE_URL in .env."
        if not settings.api_key:
            return "Set CRICBUZZ_API_KEY in .env."
        return "API configuration is present."

    def _headers_and_params(self, params: dict[str, Any] | None):
        headers = {"Accept": "application/json"}
        request_params = dict(params or {})
        if settings.extra_headers_json.strip():
            try:
                extra = json.loads(settings.extra_headers_json)
                if not isinstance(extra, dict):
                    raise ValueError("CRICBUZZ_EXTRA_HEADERS_JSON must be a JSON object")
                headers.update({str(key): str(value) for key, value in extra.items()})
            except json.JSONDecodeError as exc:
                raise CricketAPIError("CRICBUZZ_EXTRA_HEADERS_JSON is not valid JSON") from exc
        if settings.api_auth_type == "bearer" and settings.api_key:
            headers["Authorization"] = f"{settings.bearer_prefix} {settings.api_key}"
        elif settings.api_auth_type == "header" and settings.api_key:
            headers[settings.api_key_header] = settings.api_key
        elif settings.api_auth_type == "query" and settings.api_key:
            request_params[settings.api_key_param] = settings.api_key
        return headers, request_params

    def _configured_params(self) -> dict[str, str]:
        if not settings.live_matches_params.strip():
            return {}
        try:
            value = json.loads(settings.live_matches_params)
            if not isinstance(value, dict):
                raise ValueError("CRICBUZZ_LIVE_MATCHES_PARAMS must be a JSON object")
            return {str(key): str(item) for key, item in value.items()}
        except json.JSONDecodeError as exc:
            raise CricketAPIError("CRICBUZZ_LIVE_MATCHES_PARAMS is not valid JSON") from exc

    def get(self, path: str = "", params: dict[str, Any] | None = None) -> Any:
        if not self.configured:
            raise CricketAPIError("CRICBUZZ_BASE_URL is not configured")
        headers, request_params = self._headers_and_params(params)
        url = f"{settings.base_url}/{path.lstrip('/')}"
        try:
            response = self.session.get(url, params=request_params, headers=headers, timeout=settings.timeout_seconds)
            response.raise_for_status()
            payload = response.json()
        except requests.HTTPError as exc:
            detail = exc.response.text[:300] if exc.response is not None else str(exc)
            raise CricketAPIError(f"HTTP request failed: {detail}") from exc
        except (requests.RequestException, ValueError) as exc:
            raise CricketAPIError(str(exc)) from exc
        if not isinstance(payload, (dict, list)):
            raise CricketAPIError("API returned an unexpected JSON shape")
        return payload

    def live_matches(self) -> Any:
        return self.get(settings.live_matches_endpoint, self._configured_params())

    def scorecard(self, match_id: str | int) -> Any:
        """Fetch a scorecard using the provider's match ID."""
        endpoint = settings.scorecard_endpoint.format(match_id=str(match_id))
        return self.get(endpoint)

    @staticmethod
    def extract_match_items(payload: Any) -> list[dict[str, Any]]:
        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict):
            items = None
            for key in ("matches", "data", "results", "response", "items"):
                candidate = payload.get(key)
                if isinstance(candidate, list):
                    items = candidate
                    break
                if isinstance(candidate, dict):
                    for nested_key in ("matches", "data", "results", "items"):
                        nested = candidate.get(nested_key)
                        if isinstance(nested, list):
                            items = nested
                            break
                    if items is not None:
                        break
            if items is None and all(key in payload for key in ("id", "status")):
                items = [payload]
            items = items or []
        else:
            items = []
        return [item for item in items if isinstance(item, dict)]

    @classmethod
    def normalize_live_matches(cls, payload: Any) -> list[dict[str, Any]]:
        normalized = []
        for item in cls.extract_match_items(payload):
            teams = item.get("teams") or item.get("teamInfo") or []
            if isinstance(teams, dict):
                teams = list(teams.values())
            normalized.append({
                "external_match_id": item.get("id") or item.get("matchId") or item.get("match_id"),
                "match_description": item.get("name") or item.get("description") or item.get("matchDescription"),
                "status": item.get("status") or item.get("matchStatus") or item.get("state"),
                "format": item.get("format") or item.get("matchType") or item.get("type"),
                "match_date": item.get("date") or item.get("matchDate") or item.get("startTime"),
                "venue": item.get("venue") or item.get("venueName") or item.get("ground"),
                "team_1": item.get("team1") or (teams[0].get("name") if len(teams) > 0 and isinstance(teams[0], dict) else None),
                "team_2": item.get("team2") or (teams[1].get("name") if len(teams) > 1 and isinstance(teams[1], dict) else None),
            })
        return normalized
