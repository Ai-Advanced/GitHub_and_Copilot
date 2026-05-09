"""
Flask 애플리케이션 팩토리
- 블루프린트 등록
- 미들웨어 적용
- 로깅 설정
"""
import logging
import os
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pydantic import ValidationError

from .config import get_settings
from .database import init_db, get_db
from .auth import verify_password, create_token, hash_password
from .models import Employee
from .validators import LoginRequest
from .middleware import register_error_handlers, register_request_hooks


def create_app() -> Flask:
    settings = get_settings()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    # 로깅 설정
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Rate Limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[settings.RATE_LIMIT_DEFAULT],
        storage_uri="memory://",
    )

    # 미들웨어 등록
    register_error_handlers(app)
    register_request_hooks(app)

    # ── 인증 라우트 (블루프린트 밖에서 직접 정의) ──

    @app.route("/api/login", methods=["POST"])
    @limiter.limit(settings.RATE_LIMIT_LOGIN)
    def login():
        try:
            data = LoginRequest(**request.get_json())
        except ValidationError as e:
            return jsonify({"error": "입력값 검증 실패", "details": e.errors()}), 422

        from sqlalchemy.orm import Session
        db: Session = next(get_db())
        try:
            user = db.query(Employee).filter(Employee.email == data.email).first()
            if not user or not verify_password(data.password, user.password_hash):
                return jsonify({"error": "이메일 또는 비밀번호가 올바르지 않습니다"}), 401

            token = create_token(user)
            return jsonify({
                "status": "success",
                "user": user.to_dict(),
                "token": token,
            })
        finally:
            db.close()

    @app.route("/api/health", methods=["GET"])
    def health():
        """헬스체크 (민감 정보 노출 없음)"""
        return jsonify({
            "status": "ok",
            "version": settings.APP_VERSION,
        })

    # ── 블루프린트 등록 ──
    from .routes.employees import employees_bp
    from .routes.projects import projects_bp
    from .routes.files import files_bp

    app.register_blueprint(employees_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(files_bp)

    return app


def seed_admin():
    """초기 관리자 계정 생성 (CLI 명령어로만 실행)"""
    from .database import db_session
    with db_session() as db:
        existing = db.query(Employee).filter(Employee.email == "admin@company.com").first()
        if not existing:
            admin = Employee(
                name="관리자",
                email="admin@company.com",
                department="IT",
                salary=90000,
                password_hash=hash_password(os.environ.get("ADMIN_PASSWORD", "ChangeMe!Str0ng")),
                role="admin",
            )
            db.add(admin)
            logging.getLogger(__name__).info("관리자 계정이 생성되었습니다.")


if __name__ == "__main__":
    settings = get_settings()
    init_db()
    seed_admin()
    app = create_app()
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
