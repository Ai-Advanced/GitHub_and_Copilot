# 🏢 현업 레거시 Flask API — Custom Agent 테스트 대상 코드
#
# 이 코드는 실제 현업에서 흔히 볼 수 있는 레거시 패턴을 재현합니다.
# 교육 목적으로 의도적으로 보안 취약점과 안티패턴을 포함합니다.
# 절대 프로덕션에서 사용하지 마세요!

import sqlite3
import os
import json
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify, send_file, render_template_string

app = Flask(__name__)
app.secret_key = "super-secret-key-12345"  # 하드코딩된 시크릿

# ========== 데이터베이스 설정 ==========
DB_PATH = "company.db"

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            department TEXT,
            salary REAL,
            password TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            budget REAL,
            owner_id INTEGER,
            status TEXT DEFAULT 'active',
            created_at TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            user_id INTEGER,
            details TEXT,
            timestamp TEXT
        )
    """)
    # 샘플 데이터 삽입
    try:
        db.execute(
            "INSERT INTO employees (name, email, department, salary, password, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("김관리자", "admin@company.com", "IT", 90000, hashlib.md5("admin123".encode()).hexdigest(), "admin", datetime.now().isoformat())
        )
        db.execute(
            "INSERT INTO employees (name, email, department, salary, password, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("이개발자", "dev@company.com", "Engineering", 75000, hashlib.md5("dev456".encode()).hexdigest(), "user", datetime.now().isoformat())
        )
        db.execute(
            "INSERT INTO projects (title, description, budget, owner_id, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("신규 플랫폼", "차세대 플랫폼 개발", 500000, 1, "active", datetime.now().isoformat())
        )
    except:
        pass
    db.commit()
    db.close()


# ========== 인증 관련 ==========

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("email", "")
    password = data.get("password", "")

    db = get_db()
    # SQL Injection 취약점 — 문자열 포맷팅으로 쿼리 생성
    query = f"SELECT * FROM employees WHERE email = '{username}' AND password = '{hashlib.md5(password.encode()).hexdigest()}'"
    user = db.execute(query).fetchone()
    db.close()

    if user:
        return jsonify({
            "status": "success",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "salary": user["salary"]  # 민감 정보 노출
            },
            "token": hashlib.md5(f"{user['id']}:{app.secret_key}".encode()).hexdigest()  # 취약한 토큰 생성
        })
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401


# ========== 직원 관리 ==========

@app.route("/api/employees", methods=["GET"])
def get_employees():
    department = request.args.get("department", "")
    db = get_db()

    if department:
        # SQL Injection — 사용자 입력을 직접 쿼리에 삽입
        query = "SELECT * FROM employees WHERE department = '" + department + "'"
    else:
        query = "SELECT * FROM employees"

    employees = db.execute(query).fetchall()
    db.close()

    result = []
    for emp in employees:
        result.append({
            "id": emp["id"],
            "name": emp["name"],
            "email": emp["email"],
            "department": emp["department"],
            "salary": emp["salary"],      # 모든 사용자에게 급여 노출
            "password": emp["password"],  # 비밀번호 해시 노출!
            "role": emp["role"]
        })
    return jsonify(result)


@app.route("/api/employees", methods=["POST"])
def create_employee():
    data = request.get_json()

    # 입력 검증 없음
    name = data.get("name")
    email = data.get("email")
    department = data.get("department")
    salary = data.get("salary")
    password = data.get("password", "default123")
    role = data.get("role", "user")  # 사용자가 직접 role을 지정할 수 있음 (권한 상승)

    db = get_db()
    try:
        db.execute(
            f"INSERT INTO employees (name, email, department, salary, password, role, created_at) "
            f"VALUES ('{name}', '{email}', '{department}', {salary}, "
            f"'{hashlib.md5(password.encode()).hexdigest()}', '{role}', '{datetime.now().isoformat()}')"
        )
        db.commit()
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500  # 에러 상세 정보 노출

    db.close()
    return jsonify({"status": "created", "name": name}), 201


@app.route("/api/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    # 인증/인가 검증 없음 — 누구나 삭제 가능
    db = get_db()
    db.execute(f"DELETE FROM employees WHERE id = {emp_id}")
    db.commit()
    db.close()
    return jsonify({"status": "deleted"})


# ========== 프로젝트 관리 ==========

@app.route("/api/projects", methods=["GET"])
def get_projects():
    db = get_db()
    projects = db.execute("SELECT * FROM projects").fetchall()
    db.close()

    result = []
    for p in projects:
        result.append({
            "id": p["id"],
            "title": p["title"],
            "description": p["description"],
            "budget": p["budget"],  # 예산 정보 무차별 노출
            "owner_id": p["owner_id"],
            "status": p["status"]
        })
    return jsonify(result)


@app.route("/api/projects/search", methods=["GET"])
def search_projects():
    keyword = request.args.get("q", "")
    db = get_db()
    # SQL Injection
    query = f"SELECT * FROM projects WHERE title LIKE '%{keyword}%' OR description LIKE '%{keyword}%'"
    projects = db.execute(query).fetchall()
    db.close()

    return jsonify([dict(p) for p in projects])


# ========== 보고서 & 파일 ==========

@app.route("/api/report", methods=["GET"])
def generate_report():
    """XSS 취약점 — 사용자 입력을 HTML에 직접 삽입"""
    title = request.args.get("title", "보고서")
    author = request.args.get("author", "시스템")

    html = f"""
    <html>
    <head><title>{title}</title></head>
    <body>
        <h1>{title}</h1>
        <p>작성자: {author}</p>
        <p>생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/api/files/download", methods=["GET"])
def download_file():
    """Path Traversal 취약점 — 경로 검증 없음"""
    filename = request.args.get("name", "")
    filepath = os.path.join("/data/reports", filename)
    try:
        return send_file(filepath)
    except:
        return jsonify({"error": "File not found"}), 404


@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    """파일 업로드 — 확장자/크기 검증 없음"""
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file"}), 400

    # 파일명 그대로 저장 — 경로 조작 가능
    save_path = os.path.join("/data/uploads", file.filename)
    file.save(save_path)
    return jsonify({"status": "uploaded", "path": save_path})


# ========== 관리자 기능 ==========

@app.route("/api/admin/salary-update", methods=["POST"])
def update_salary():
    """IDOR + 인가 미흡 — 관리자 검증 없이 급여 변경"""
    data = request.get_json()
    emp_id = data.get("employee_id")
    new_salary = data.get("salary")

    db = get_db()
    db.execute(f"UPDATE employees SET salary = {new_salary} WHERE id = {emp_id}")
    db.commit()
    db.close()

    return jsonify({"status": "updated", "employee_id": emp_id, "new_salary": new_salary})


@app.route("/api/admin/run-query", methods=["POST"])
def run_raw_query():
    """임의 SQL 실행 — 가장 위험한 엔드포인트"""
    data = request.get_json()
    query = data.get("query", "")

    db = get_db()
    try:
        result = db.execute(query).fetchall()
        db.close()
        return jsonify({"result": [dict(r) for r in result]})
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500


# ========== 유틸리티 ==========

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "debug": app.debug,
        "secret_key_length": len(app.secret_key),  # 보안 정보 노출
        "db_path": DB_PATH,  # 내부 경로 노출
        "python_version": os.sys.version  # 시스템 정보 노출
    })


@app.route("/api/debug/env", methods=["GET"])
def debug_env():
    """환경 변수 전체 노출 — 매우 위험"""
    return jsonify(dict(os.environ))


# ========== 앱 시작 ==========

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)  # debug=True — 프로덕션 위험
