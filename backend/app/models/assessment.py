from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class Assessment(Base):
    __tablename__ = "assessments"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(20), default="draft")
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    questions: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id", ondelete="CASCADE"), index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="in_progress")
    submitted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
