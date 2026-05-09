"""
안전한 파일 업로드/다운로드 라우트
- Path Traversal 방지
- 파일 확장자/크기 제한
- 안전한 파일명 처리
"""
import os
import uuid
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

from ..auth import login_required
from ..config import get_settings

files_bp = Blueprint("files", __name__, url_prefix="/api/files")


def _allowed_file(filename: str) -> bool:
    """허용된 확장자인지 확인"""
    settings = get_settings()
    return "." in filename and filename.rsplit(".", 1)[1].lower() in settings.ALLOWED_EXTENSIONS


def _safe_path(base_dir: str, filename: str) -> str | None:
    """Path Traversal 방지: 최종 경로가 base_dir 내부인지 검증"""
    safe_name = secure_filename(filename)
    if not safe_name:
        return None
    full_path = os.path.realpath(os.path.join(base_dir, safe_name))
    if not full_path.startswith(os.path.realpath(base_dir)):
        return None
    return full_path


@files_bp.route("/download", methods=["GET"])
@login_required
def download_file():
    """안전한 파일 다운로드"""
    filename = request.args.get("name", "").strip()
    if not filename:
        return jsonify({"error": "파일명을 지정해주세요"}), 400

    settings = get_settings()
    safe_path = _safe_path(settings.REPORT_DIR, filename)
    if safe_path is None:
        return jsonify({"error": "유효하지 않은 파일명입니다"}), 400

    if not os.path.isfile(safe_path):
        return jsonify({"error": "파일을 찾을 수 없습니다"}), 404

    return send_from_directory(
        settings.REPORT_DIR,
        secure_filename(filename),
        as_attachment=True,
    )


@files_bp.route("/upload", methods=["POST"])
@login_required
def upload_file():
    """안전한 파일 업로드"""
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "파일이 필요합니다"}), 400

    if not _allowed_file(file.filename):
        settings = get_settings()
        return jsonify({
            "error": f"허용되지 않는 파일 형식입니다. 허용 형식: {', '.join(sorted(settings.ALLOWED_EXTENSIONS))}"
        }), 400

    settings = get_settings()

    # 파일 크기 제한 검사
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        return jsonify({"error": f"파일 크기는 {settings.MAX_UPLOAD_SIZE_MB}MB를 초과할 수 없습니다"}), 400

    # 고유한 파일명 생성 (원본 확장자 유지)
    ext = secure_filename(file.filename).rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    file.save(save_path)

    return jsonify({
        "status": "uploaded",
        "filename": unique_name,
    }), 201
