from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_roles
from app.models.assessment import Assessment, Attempt
from app.models.course import Course
from app.models.user import User
from app.schemas import AssessmentCreate, AssessmentOut, AttemptSubmit
router = APIRouter(tags=["assessments"])
@router.get("/assessments", response_model=list[AssessmentOut])
def list_assessments(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = select(Assessment).where(Assessment.status == "published") if user.role == "student" else select(Assessment)
    return list(db.scalars(query.order_by(Assessment.id.desc())).all())
@router.post("/assessments", response_model=AssessmentOut, status_code=201)
def create_assessment(payload: AssessmentCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("teacher"))):
    course = db.get(Course, payload.course_id)
    if not course: raise HTTPException(status_code=404, detail="Course not found")
    if course.teacher_id != user.id: raise HTTPException(status_code=403, detail="You do not own this course")
    item = Assessment(title=payload.title.strip(), course_id=course.id, created_by=user.id, duration_minutes=payload.duration_minutes, questions=payload.questions)
    db.add(item); db.commit(); db.refresh(item)
    return item
@router.post("/assessments/{assessment_id}/publish", response_model=AssessmentOut)
def publish(assessment_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("teacher"))):
    item = db.get(Assessment, assessment_id)
    if not item: raise HTTPException(status_code=404, detail="Assessment not found")
    course = db.get(Course, item.course_id)
    if item.created_by != user.id or not course or course.teacher_id != user.id:
        raise HTTPException(status_code=403, detail="You do not own this assessment")
    if not item.questions: raise HTTPException(status_code=400, detail="Add at least one question before publishing")
    item.status = "published"; db.commit(); db.refresh(item)
    return item
@router.post("/assessments/{assessment_id}/attempts", status_code=201)
def start_attempt(assessment_id: int, db: Session = Depends(get_db), user: User = Depends(require_roles("student"))):
    item = db.get(Assessment, assessment_id)
    if not item or item.status != "published": raise HTTPException(status_code=404, detail="Published assessment not found")
    attempt = Attempt(assessment_id=item.id, student_id=user.id, answers={}, status="in_progress")
    db.add(attempt); db.commit(); db.refresh(attempt)
    return {"id": attempt.id, "assessment_id": item.id, "status": attempt.status}
@router.post("/attempts/{attempt_id}/submit")
def submit(attempt_id: int, payload: AttemptSubmit, db: Session = Depends(get_db), user: User = Depends(require_roles("student"))):
    attempt = db.get(Attempt, attempt_id)
    if not attempt or attempt.student_id != user.id: raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status != "in_progress": raise HTTPException(status_code=409, detail="Attempt has already been submitted")
    item = db.get(Assessment, attempt.assessment_id); score = 0
    for idx, q in enumerate(item.questions or []):
        answer = q.get("answer")
        if answer is not None and str(payload.answers.get(str(idx), "")).strip().lower() == str(answer).strip().lower():
            score += int(q.get("marks", 1))
    attempt.answers = payload.answers; attempt.score = score; attempt.status = "submitted"
    attempt.submitted_at = datetime.now(timezone.utc); db.commit()
    return {"id": attempt.id, "status": attempt.status, "score": score}
