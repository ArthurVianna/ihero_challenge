from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import null
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, db_generator
from app.core.auth import authenticate, generate_access_token
from app.schemas.user import UserCreate
from app.crud import user

router = APIRouter(
    prefix="/user"
)

@router.get("/")
def read_users(skip: int = 0, limit: int = 100, db = Depends(db_generator), current_user = Depends(get_current_user)):
    db_user = user.get_users(db, skip, limit)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/me")
def read_user(current_user = Depends(get_current_user)):
    return current_user


@router.post("/login/")
# def login(email: str, password: str, db: Session = Depends(db_generator)):
def login(user_dict: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_generator)):
    db_user = authenticate(db, email=user_dict.username, password=user_dict.password)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Incorrect user or password")
    return {
        "access_token": generate_access_token(user_id=db_user.id), 
        "token_type": "bearer",
    }

@router.post("/")
def create_user(new_user: UserCreate, db: Session = Depends(db_generator)):
    return user.create_user(db=db, user=new_user)