from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "EduImpact API"
    environment: str = "development"
    debug: bool = False
    secret_key: str = "development-only-change-this-secret-key-please"
    database_url: str = "sqlite:///./eduimpact.db"
    cors_origins: str = "http://localhost:5173"
    access_token_minutes: int = 30
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    auto_create_tables: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def cors_origin_list(self):
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

@lru_cache
def get_settings():
    return Settings()
settings = get_settings()
