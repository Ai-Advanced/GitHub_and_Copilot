"""
인증/인가, 에러 핸들링, Rate Limiting 미들웨어
"""
import logging
from flask import Flask, jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask):
    """전역 에러 핸들러 등록"""

    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return jsonify({
            "error": "입력값 검증 실패",
            "details": e.errors(),
        }), 422

    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({"error": "잘못된 요청입니다"}), 400

    @app.errorhandler(401)
    def handle_unauthorized(e):
        return jsonify({"error": "인증이 필요합니다"}), 401

    @app.errorhandler(403)
    def handle_forbidden(e):
        return jsonify({"error": "권한이 없습니다"}), 403

    @app.errorhandler(404)
    def handle_not_found(e):
        return jsonify({"error": "리소스를 찾을 수 없습니다"}), 404

    @app.errorhandler(429)
    def handle_rate_limit(e):
        return jsonify({"error": "요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."}), 429

    @app.errorhandler(500)
    def handle_internal_error(e):
        logger.error(f"Internal Server Error: {e}", exc_info=True)
        # 내부 오류 상세 정보를 클라이언트에 노출하지 않음
        return jsonify({"error": "서버 내부 오류가 발생했습니다"}), 500

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify({"error": "예상치 못한 오류가 발생했습니다"}), 500


def register_request_hooks(app: Flask):
    """요청/응답 훅 등록"""

    @app.before_request
    def log_request():
        logger.info(f"{request.method} {request.path} - {request.remote_addr}")

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Cache-Control"] = "no-store"
        return response
