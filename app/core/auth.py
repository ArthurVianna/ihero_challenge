import hashlib
from datetime import timedelta, datetime

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from app.core.settings import get_settings
from app.models.user import User

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def generate_md5(password: str):
    return hashlib.md5(password.encode()).hexdigest()

def authenticate(db: Session, email: str, password: str):
    user =  db.query(User).filter(
        User.email == email
    ).first()
    if not user:
        return None
    if user.password != generate_md5(password):
        return None
    return user

def generate_access_token(*, user_id: str):
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=user_id,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)