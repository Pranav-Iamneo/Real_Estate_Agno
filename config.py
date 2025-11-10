"""
Configuration for Real Estate Intelligence System
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Settings(BaseSettings):
    """Real Estate Intelligence System Settings"""

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Agent Configuration
    AGENT_MODEL: str = "gemini-2.0-flash"
    AGENT_TEMPERATURE: float = 0.7
    AGENT_MAX_TOKENS: int = 4096

    # Database
    DB_FILE: str = "real_estate.db"
    DB_TYPE: str = "sqlite"

    # Real Estate Configuration
    CURRENCY: str = "USD"
    PROPERTY_DATABASE_FILE: str = "property_market_data.json"

    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # API Server
    API_HOST: str = os.getenv("API_HOST", "localhost")
    API_PORT: int = int(os.getenv("API_PORT", "8082"))

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
