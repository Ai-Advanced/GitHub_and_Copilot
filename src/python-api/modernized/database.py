"""
SQLAlchemy 기반 데이터베이스 레이어
연결 관리, 세션 팩토리, 마이그레이션 지원
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from contextlib import contextmanager
from typing import Generator

from .config import get_settings


class Base(DeclarativeBase):
    pass


_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
        )
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            bind=get_engine(),
            autocommit=False,
            autoflush=False,
        )
    return _SessionLocal


def init_db():
    """테이블 생성 (개발 환경 전용, 프로덕션은 Alembic 사용)"""
    from .models import Employee, Project  # noqa: F401
    Base.metadata.create_all(bind=get_engine())


def get_db() -> Generator[Session, None, None]:
    """Flask 요청 컨텍스트용 DB 세션 제너레이터"""
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """독립적인 DB 세션 컨텍스트 매니저"""
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
