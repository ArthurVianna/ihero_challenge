
from datetime import datetime
from sqlalchemy import update, delete
from sqlalchemy.orm import Session, joinedload

from app.models.occurrence import Occurrence, OccurrenceRanks, Attendance

def get_occurrence(db: Session, occurrence_id: int):
    return db.query(Occurrence).filter(Occurrence.id == occurrence_id).first()

def create_occurrence(data, db: Session):
    db_occurrence = Occurrence(
        monster_name=data["monsterName"],
        lat=data["location"][0]["lat"],
        long=data["location"][0]["lng"],
        rank=OccurrenceRanks.getByRankName(data["dangerLevel"])
    )
    db.add(db_occurrence)
    db.commit()
    db.refresh(db_occurrence)
    return db_occurrence
    
def get_occurrences(db: Session, skip: int = 0, limit: int = 100): 
    return db.query(Occurrence).\
            options(joinedload(Occurrence.heroes).options(joinedload(Attendance.hero))).\
                offset(skip).limit(limit).all()