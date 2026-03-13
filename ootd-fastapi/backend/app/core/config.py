"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # App Info
    APP_NAME: str = "穿搭AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key"

    # Database
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/ootd_fastapi"

    # JWT
    JWT_SECRET_KEY: str = "your-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080  # 7 days

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # MiniMax AI
    MINIMAX_API_KEY: str = ""
    MINIMAX_GROUP_ID: str = ""

    # Alibaba Cloud OSS
    OSS_REGION: str = ""
    OSS_ACCESS_KEY_ID: str = ""
    OSS_ACCESS_KEY_SECRET: str = ""
    OSS_BUCKET: str = ""

    # Upload
    UPLOAD_DIR: str = "/data/public/uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
