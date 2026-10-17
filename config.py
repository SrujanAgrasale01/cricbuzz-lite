"""Application configuration loaded from environment variables."""
from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    database_path: str = os.getenv("DATABASE_PATH", "data/cricket.db")
    base_url: str = os.getenv("CRICBUZZ_BASE_URL", "").rstrip("/")
    api_key: str = os.getenv("CRICBUZZ_API_KEY", "")
    api_auth_type: str = os.getenv("CRICBUZZ_API_AUTH_TYPE", "header").lower()
    api_key_header: str = os.getenv("CRICBUZZ_API_KEY_HEADER", "x-api-key")
    api_key_param: str = os.getenv("CRICBUZZ_API_KEY_PARAM", "apikey")
    bearer_prefix: str = os.getenv("CRICBUZZ_BEARER_PREFIX", "Bearer")
    extra_headers_json: str = os.getenv("CRICBUZZ_EXTRA_HEADERS_JSON", "")
    live_matches_endpoint: str = os.getenv("CRICBUZZ_LIVE_MATCHES_ENDPOINT", "matches")
    live_matches_params: str = os.getenv("CRICBUZZ_LIVE_MATCHES_PARAMS", "")
    scorecard_endpoint: str = os.getenv("CRICBUZZ_SCORECARD_ENDPOINT", "mcenter/v1/{match_id}/scard")
    timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "15"))
    auto_seed_demo_data: bool = os.getenv("AUTO_SEED_DEMO_DATA", "true").lower() in {"1", "true", "yes"}

    def ensure_data_dir(self) -> None:
        Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)

settings = Settings()
