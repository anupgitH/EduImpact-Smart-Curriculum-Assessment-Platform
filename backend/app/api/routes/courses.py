from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, require_roles
from app.models.course import Course
from app.models.user import User
from app.schemas import CourseCreate, CourseOut
router = APIRouter(prefix="/courses", tags=["courses"])
@router.get("", response_model=list[CourseOut])
def list_courses(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return list(db.scalars(select(Course).order_by(Course.id.desc())).all())
@router.post("", response_model=CourseOut, status_code=201)
def create_course(payload: CourseCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("teacher"))):
    code = payload.code.strip().upper()
    if db.scalar(select(Course).where(Course.code == code)):
        raise HTTPException(status_code=409, detail="Course code already exists")
    course = Course(title=payload.title.strip(), code=code, description=payload.description.strip(), teacher_id=user.id)
    db.add(course); db.commit(); db.refresh(course)
    return course
