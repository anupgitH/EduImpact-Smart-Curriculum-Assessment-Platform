from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas import UserCreate, UserLogin, TokenOut, UserOut
router = APIRouter(prefix="/auth", tags=["authentication"])
@router.post("/register", response_model=TokenOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(name=payload.name.strip(), email=email, password_hash=hash_password(payload.password), role=payload.role)
    db.add(user); db.commit(); db.refresh(user)
    return TokenOut(access_token=create_access_token(str(user.id), user.role), user=user)
@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash) or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenOut(access_token=create_access_token(str(user.id), user.role), user=user)
@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
