from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    cors_regex: str

    db_dsn: str

    access_token_sign_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    secret_key: str


__settings_cache: _Settings | None = None


def get_settings() -> _Settings:
    global __settings_cache
    if __settings_cache is None:
        __settings_cache = _Settings()  # pyright: ignore[reportGeneralTypeIssues]
    return __settings_cache
