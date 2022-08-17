from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, db_generator
from app.crud import occurrence

router = APIRouter(
    prefix="/occurrence"
)

@router.get("/")
def read_occurrencees(skip: int = 0, limit: int = 100, db = Depends(db_generator), current_user = Depends(get_current_user)):
    db_occurrence = occurrence.get_occurrences(db, skip, limit)
    if db_occurrence is None:
        raise HTTPException(status_code=404, detail="Occurrence not found")
    return db_occurrence

@router.get("/{occurrence_id}")
def read_occurrence(occurrence_id: int, db = Depends(db_generator), current_user = Depends(get_current_user)):
    db_occurrence = occurrence.get_occurrence(db, occurrence_id)
    if db_occurrence is None:
        raise HTTPException(status_code=404, detail="Occurrence not found")
    return db_occurrence
