from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.models.course import Course
from app.models.assessment import Assessment, Attempt
from app.models.user import User
router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("/overview")
def overview(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    courses = db.scalar(select(func.count(Course.id))) or 0
    assessments = db.scalar(select(func.count(Assessment.id))) or 0
    if user.role == "student":
        attempts = list(db.scalars(select(Attempt).where(Attempt.student_id == user.id)).all())
        scores = [a.score for a in attempts if a.score is not None]
        return {"courses": courses, "assessments": assessments, "attempts": len(attempts),
                "average_score": round(sum(scores)/len(scores),1) if scores else 0}
    return {"courses": courses, "assessments": assessments, "users": db.scalar(select(func.count(User.id))) or 0,
            "submitted_attempts": db.scalar(select(func.count(Attempt.id)).where(Attempt.status=="submitted")) or 0}
