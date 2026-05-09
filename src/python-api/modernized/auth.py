"""
인증/인가 모듈
- bcrypt 기반 비밀번호 해싱
- JWT 토큰 발급/검증
- 역할 기반 접근 제어 (RBAC)
"""
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from functools import wraps
from flask import request, jsonify, g
from sqlalchemy.orm import Session

from .config import get_settings
from .models import Employee


def hash_password(password: str) -> str:
    """bcrypt로 비밀번호 해싱"""
    settings = get_settings()
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """bcrypt 해시 검증"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(employee: Employee) -> str:
    """JWT 액세스 토큰 생성"""
    settings = get_settings()
    payload = {
        "sub": employee.id,
        "email": employee.email,
        "role": employee.role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    """JWT 토큰 디코딩 및 검증"""
    settings = get_settings()
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


def login_required(f):
    """인증 필수 데코레이터"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "인증 토큰이 필요합니다"}), 401

        token = auth_header.split("Bearer ")[-1]
        try:
            payload = decode_token(token)
            g.current_user_id = payload["sub"]
            g.current_user_role = payload["role"]
            g.current_user_email = payload["email"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "토큰이 만료되었습니다"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "유효하지 않은 토큰입니다"}), 401

        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """관리자 권한 필수 데코레이터"""
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if g.current_user_role != "admin":
            return jsonify({"error": "관리자 권한이 필요합니다"}), 403
        return f(*args, **kwargs)
    return decorated


def get_current_user(db: Session) -> Employee | None:
    """현재 인증된 사용자 조회"""
    user_id = getattr(g, "current_user_id", None)
    if user_id is None:
        return None
    return db.query(Employee).filter(Employee.id == user_id).first()
