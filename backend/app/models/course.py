from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(180), index=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
