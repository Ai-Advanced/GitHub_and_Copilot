"""
직원 관리 라우트 (보안 적용 완료)
- 인증/인가 적용
- Pydantic 입력 검증
- SQLAlchemy 파라미터 바인딩 (SQL Injection 방지)
- 민감 정보 노출 차단
"""
from flask import Blueprint, request, jsonify, g
from sqlalchemy.orm import Session
from pydantic import ValidationError

from ..auth import login_required, admin_required, hash_password, get_current_user
from ..database import get_db
from ..models import Employee
from ..validators import EmployeeCreateRequest, EmployeeUpdateRequest, SalaryUpdateRequest

employees_bp = Blueprint("employees", __name__, url_prefix="/api/employees")


@employees_bp.route("", methods=["GET"])
@login_required
def list_employees():
    """직원 목록 조회 (인증 필수, 민감 정보 제외)"""
    department = request.args.get("department", "").strip()
    db: Session = next(get_db())
    try:
        query = db.query(Employee)
        if department:
            # 파라미터 바인딩으로 SQL Injection 방지
            query = query.filter(Employee.department == department)

        employees = query.all()

        # 관리자는 급여 정보 포함, 일반 사용자는 제외
        include_sensitive = g.current_user_role == "admin"
        return jsonify([emp.to_dict(include_sensitive=include_sensitive) for emp in employees])
    finally:
        db.close()


@employees_bp.route("/<int:emp_id>", methods=["GET"])
@login_required
def get_employee(emp_id: int):
    """직원 상세 조회"""
    db: Session = next(get_db())
    try:
        employee = db.query(Employee).filter(Employee.id == emp_id).first()
        if not employee:
            return jsonify({"error": "직원을 찾을 수 없습니다"}), 404

        include_sensitive = (
            g.current_user_role == "admin" or g.current_user_id == emp_id
        )
        return jsonify(employee.to_dict(include_sensitive=include_sensitive))
    finally:
        db.close()


@employees_bp.route("", methods=["POST"])
@admin_required
def create_employee():
    """직원 생성 (관리자 전용, role 필드 지정 불가)"""
    try:
        data = EmployeeCreateRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": "입력값 검증 실패", "details": e.errors()}), 422

    db: Session = next(get_db())
    try:
        existing = db.query(Employee).filter(Employee.email == data.email).first()
        if existing:
            return jsonify({"error": "이미 존재하는 이메일입니다"}), 409

        employee = Employee(
            name=data.name,
            email=data.email,
            department=data.department,
            salary=data.salary,
            password_hash=hash_password(data.password),
            role="user",  # Mass Assignment 방지: role은 항상 'user'로 고정
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)

        return jsonify({
            "status": "created",
            "employee": employee.to_dict(),
        }), 201
    except Exception:
        db.rollback()
        return jsonify({"error": "직원 생성에 실패했습니다"}), 500
    finally:
        db.close()


@employees_bp.route("/<int:emp_id>", methods=["PUT"])
@admin_required
def update_employee(emp_id: int):
    """직원 정보 수정 (관리자 전용)"""
    try:
        data = EmployeeUpdateRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": "입력값 검증 실패", "details": e.errors()}), 422

    db: Session = next(get_db())
    try:
        employee = db.query(Employee).filter(Employee.id == emp_id).first()
        if not employee:
            return jsonify({"error": "직원을 찾을 수 없습니다"}), 404

        if data.name is not None:
            employee.name = data.name
        if data.department is not None:
            employee.department = data.department
        if data.salary is not None:
            employee.salary = data.salary

        db.commit()
        return jsonify({"status": "updated", "employee": employee.to_dict(include_sensitive=True)})
    except Exception:
        db.rollback()
        return jsonify({"error": "수정에 실패했습니다"}), 500
    finally:
        db.close()


@employees_bp.route("/<int:emp_id>", methods=["DELETE"])
@admin_required
def delete_employee(emp_id: int):
    """직원 삭제 (관리자 전용, 자기 자신 삭제 불가)"""
    if g.current_user_id == emp_id:
        return jsonify({"error": "자기 자신은 삭제할 수 없습니다"}), 400

    db: Session = next(get_db())
    try:
        employee = db.query(Employee).filter(Employee.id == emp_id).first()
        if not employee:
            return jsonify({"error": "직원을 찾을 수 없습니다"}), 404

        db.delete(employee)
        db.commit()
        return jsonify({"status": "deleted", "id": emp_id})
    except Exception:
        db.rollback()
        return jsonify({"error": "삭제에 실패했습니다"}), 500
    finally:
        db.close()


@employees_bp.route("/salary", methods=["POST"])
@admin_required
def update_salary():
    """급여 업데이트 (관리자 전용)"""
    try:
        data = SalaryUpdateRequest(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": "입력값 검증 실패", "details": e.errors()}), 422

    db: Session = next(get_db())
    try:
        employee = db.query(Employee).filter(Employee.id == data.employee_id).first()
        if not employee:
            return jsonify({"error": "직원을 찾을 수 없습니다"}), 404

        employee.salary = data.salary
        db.commit()
        return jsonify({
            "status": "updated",
            "employee_id": data.employee_id,
            "new_salary": data.salary,
        })
    except Exception:
        db.rollback()
        return jsonify({"error": "급여 수정에 실패했습니다"}), 500
    finally:
        db.close()
