"""
SQLAlchemy ORM 모델 정의
"""
from datetime import datetime, timezone
from sqlalchemy import String, Float, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    department: Mapped[str] = mapped_column(String(100), nullable=True)
    salary: Mapped[float] = mapped_column(Float, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    projects: Mapped[list["Project"]] = relationship("Project", back_populates="owner")

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """직렬화 (비밀번호/급여 등 민감 정보 제어)"""
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_sensitive:
            data["salary"] = self.salary
        return data


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    owner_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("employees.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    owner: Mapped[Employee | None] = relationship("Employee", back_populates="projects")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "budget": self.budget,
            "owner_id": self.owner_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
