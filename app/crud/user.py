
from sqlalchemy.orm import Session

from app.core import auth
from app.models.user import User
from app.schemas.user import UserCreate



def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
    
def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        password=auth.generate_md5(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100): 
    return db.query(User).offset(skip).limit(limit).all()