"""
Configuration module for the Ecommerce Chatbot API.

Loads environment variables and provides typed settings via Pydantic BaseSettings.
Use this to centralize feature flags and external integration settings.

Ocean Professional note:
- Keep settings clear and discoverable; avoid hardcoding values in services.
"""
from functools import lru_cache
from typing import List, Optional

# Pydantic v2 migration note:
# BaseSettings moved to the separate package pydantic-settings.
from pydantic_settings import BaseSettings
from pydantic import Field, AnyHttpUrl
from dotenv import load_dotenv

# Load .env if present (non-fatal if missing)
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    APP_NAME: str = Field(default="Ecommerce Chatbot API", description="Application name for OpenAPI and logs.")
    ENV: str = Field(default="development", description="Runtime environment: development|staging|production")
    DEBUG: bool = Field(default=True, description="Enable debug features for development.")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level.")
    CORS_ALLOW_ORIGINS: List[str] = Field(default=["*"], description="CORS allowed origins list.")

    # LLM / Chat provider mock toggle
    LLM_PROVIDER: str = Field(default="mock", description="LLM provider identifier (mock|openai|vertex|...)")
    LLM_MODEL: str = Field(default="mock-chat-001", description="LLM model to use.")
    # Example external keys (not required in mock)
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key if using openai provider.")

    # Product provider mock toggle
    PRODUCT_PROVIDER: str = Field(default="mock", description="Product data source (mock|shopify|magento|custom)")
    PRODUCT_SOURCE_URL: Optional[AnyHttpUrl] = Field(default=None, description="Base URL for product provider API.")

    # Recommendation settings
    RECOMMENDER_PROVIDER: str = Field(default="builtin", description="Recommendation engine provider.")
    MAX_RECOMMENDATIONS: int = Field(default=6, description="Default max recommendations returned.")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings."""
    return Settings()
