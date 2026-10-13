from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "AutoPartSmart Backend API"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: str = "sqlite:///./autopartsmart.db"

    # JWT Authentication Security
    SECRET_KEY: str = "autopartsmart-super-secret-key-32chars-for-dev-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI Model Artifacts & Fallback
    MODEL_PATH: str = "models/knn_model.joblib"
    SCALER_PATH: str = "models/scaler.joblib"

    # Security & File Limits
    MAX_FILE_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: List[str] = [".csv", ".png", ".jpg", ".jpeg"]
    ALLOWED_MIME_TYPES: List[str] = [
        "text/csv",
        "text/plain",
        "application/vnd.ms-excel",
        "image/png",
        "image/jpeg",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
