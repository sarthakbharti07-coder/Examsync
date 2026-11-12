from functools import lru_cache

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_DEFAULT_KEY = "change-me-to-a-random-string-of-at-least-32-characters"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    # App
    app_env: str = "development"
    app_name: str = "ExamPattern AI"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"

    # Authentication / JWT
    secret_key: str = _INSECURE_DEFAULT_KEY
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Database
    database_url: str = (
        "postgresql+psycopg://exampattern:exampattern@localhost:5432/exampattern"
    )

    # Gemini AI
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.1-flash-lite"

    # Supabase Storage
    supabase_url: str = ""
    supabase_secret_key: str = ""
    supabase_storage_bucket: str = "question-papers"

    # File Uploads
    storage_backend: str = "supabase"
    local_storage_path: str = "./storage"
    max_upload_mb: int = 20

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Rate Limiting
    rate_limit_enabled: bool = True
    auth_rate_limit: str = "10/minute"
    default_rate_limit: str = "120/minute"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, v):
        if isinstance(v, str) and not v.strip().startswith("["):
            return [o.strip() for o in v.split(",") if o.strip()]
        return v

    @model_validator(mode="after")
    def _check_settings(self):
        if self.app_env == "production":
            if self.secret_key == _INSECURE_DEFAULT_KEY or len(self.secret_key) < 32:
                raise ValueError(
                    "SECRET_KEY must be a random value of 32+ characters in production"
                )

        if self.storage_backend not in ("local", "supabase"):
            raise ValueError("STORAGE_BACKEND must be either 'local' or 'supabase'")

        if self.max_upload_mb < 1:
            raise ValueError("MAX_UPLOAD_MB must be at least 1")

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
