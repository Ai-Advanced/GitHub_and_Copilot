"""
애플리케이션 설정 모듈 (12-Factor App 원칙 적용)
환경변수 기반 설정 관리 - pydantic-settings 활용
"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # 애플리케이션 기본 설정
    APP_NAME: str = "Company API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 5000

    # 보안 설정
    SECRET_KEY: str = Field(..., description="JWT 서명용 비밀 키 (반드시 환경변수로 설정)")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24
    BCRYPT_ROUNDS: int = 12

    # 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///company.db"

    # 파일 업로드 설정
    UPLOAD_DIR: str = os.path.join(os.path.dirname(__file__), "uploads")
    REPORT_DIR: str = os.path.join(os.path.dirname(__file__), "reports")
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: set = {"pdf", "xlsx", "csv", "docx", "png", "jpg"}

    # Rate Limiting 설정
    RATE_LIMIT_DEFAULT: str = "100/hour"
    RATE_LIMIT_LOGIN: str = "10/minute"

    # CORS 설정
    CORS_ORIGINS: list = ["http://localhost:3000"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


def get_settings() -> Settings:
    return Settings()
