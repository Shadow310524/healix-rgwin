from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pharma Platform API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    # SECURITY FIX: Reduced from 1440 (24h) to 60 minutes.
    # Short-lived tokens limit the blast radius of token theft.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Debug mode controls whether /docs and /redoc are exposed
    DEBUG_MODE: bool = False

    # CORS — list every origin that is allowed to call this API.
    # Add your actual Vercel frontend URL to your .env file like this:
    # ALLOWED_ORIGINS=["https://your-app.vercel.app","http://localhost:5173"]
    # The defaults below cover local development so the app works out of the box.
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    DATABASE_URL: str

    CLOUDINARY_CLOUD_NAME: Optional[str] = None
    CLOUDINARY_API_KEY: Optional[str] = None
    CLOUDINARY_API_SECRET: Optional[str] = None

    GEMINI_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
