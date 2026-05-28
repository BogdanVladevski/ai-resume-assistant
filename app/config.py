from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-4o"
    temperature: float = 0.3
    max_tokens: int = 2048
    app_name: str = "AI Resume Assistant"
    version: str = "1.0.0"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
