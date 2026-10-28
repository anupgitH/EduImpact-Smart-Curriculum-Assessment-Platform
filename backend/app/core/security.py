from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

_hasher = PasswordHash.recommended()
def hash_password(password: str) -> str:
    return _hasher.hash(password)
def verify_password(password: str, hashed: str) -> bool:
    return _hasher.verify(password, hashed)
def create_access_token(subject: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": subject, "role": role, "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_minutes)},
        settings.secret_key, algorithm="HS256")
