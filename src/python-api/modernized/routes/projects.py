"""
프로젝트 관리 라우트 (보안 적용 완료)
"""
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from pydantic import ValidationError

from ..auth import login_required
from ..database import get_db
from ..models import Project
from ..validators import ProjectSearchRequest

projects_bp = Blueprint("projects", __name__, url_prefix="/api/projects")


@projects_bp.route("", methods=["GET"])
@login_required
def list_projects():
    """프로젝트 목록 조회"""
    db: Session = next(get_db())
    try:
        projects = db.query(Project).all()
        return jsonify([p.to_dict() for p in projects])
    finally:
        db.close()


@projects_bp.route("/<int:project_id>", methods=["GET"])
@login_required
def get_project(project_id: int):
    """프로젝트 상세 조회"""
    db: Session = next(get_db())
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return jsonify({"error": "프로젝트를 찾을 수 없습니다"}), 404
        return jsonify(project.to_dict())
    finally:
        db.close()


@projects_bp.route("/search", methods=["GET"])
@login_required
def search_projects():
    """프로젝트 검색 (SQL Injection 방지)"""
    try:
        params = ProjectSearchRequest(q=request.args.get("q", ""))
    except ValidationError as e:
        return jsonify({"error": "검색어 검증 실패", "details": e.errors()}), 422

    db: Session = next(get_db())
    try:
        search_term = f"%{params.q}%"
        # SQLAlchemy LIKE + 파라미터 바인딩으로 안전하게 검색
        projects = (
            db.query(Project)
            .filter(
                Project.title.like(search_term) | Project.description.like(search_term)
            )
            .all()
        )
        return jsonify([p.to_dict() for p in projects])
    finally:
        db.close()
