"""
Pydantic 기반 입력 검증 스키마
모든 API 입력을 엄격하게 검증하여 인젝션 공격 방지
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
import re


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class EmployeeCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., gt=0, le=10_000_000)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not re.match(r"^[가-힣a-zA-Z\s\-\.]+$", v):
            raise ValueError("이름에 허용되지 않는 문자가 포함되어 있습니다")
        return v.strip()

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: str) -> str:
        allowed = {"IT", "HR", "Finance", "Marketing", "Sales", "Engineering", "Operations"}
        if v not in allowed:
            raise ValueError(f"부서는 다음 중 하나여야 합니다: {', '.join(sorted(allowed))}")
        return v


class EmployeeUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    department: str | None = Field(None, min_length=1, max_length=100)
    salary: float | None = Field(None, gt=0, le=10_000_000)

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: str | None) -> str | None:
        if v is None:
            return v
        allowed = {"IT", "HR", "Finance", "Marketing", "Sales", "Engineering", "Operations"}
        if v not in allowed:
            raise ValueError(f"부서는 다음 중 하나여야 합니다: {', '.join(sorted(allowed))}")
        return v


class SalaryUpdateRequest(BaseModel):
    employee_id: int = Field(..., gt=0)
    salary: float = Field(..., gt=0, le=10_000_000)


class ProjectSearchRequest(BaseModel):
    q: str = Field(..., min_length=1, max_length=200)

    @field_validator("q")
    @classmethod
    def sanitize_query(cls, v: str) -> str:
        # SQL 와일드카드 문자 이스케이프
        v = v.replace("%", "\\%").replace("_", "\\_")
        return v.strip()


class ReportRequest(BaseModel):
    title: str = Field(default="보고서", max_length=200)
    author: str = Field(default="시스템", max_length=100)

    @field_validator("title", "author")
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        # HTML/템플릿 인젝션 방지
        dangerous_patterns = ["{{", "}}", "{%", "%}", "<script", "javascript:"]
        for pattern in dangerous_patterns:
            if pattern.lower() in v.lower():
                raise ValueError("허용되지 않는 문자 패턴이 포함되어 있습니다")
        return v.strip()
