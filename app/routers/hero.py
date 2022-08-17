from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, db_generator
from app.schemas.hero import HeroCreate
from app.crud import hero

router = APIRouter(
    prefix="/hero"
)

@router.get("/")
def read_heroes(skip: int = 0, limit: int = 100, db = Depends(db_generator), current_user = Depends(get_current_user)):
    db_hero = hero.get_heros(db, skip, limit)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero

@router.get("/{hero_id}")
def read_hero(hero_id: int, db = Depends(db_generator), current_user = Depends(get_current_user)):
    db_hero = hero.get_hero(db, hero_id)
    if db_hero is None:
        raise HTTPException(status_code=404, detail="Hero not found")
    return db_hero

@router.post("/")
def create_hero(new_hero: HeroCreate, db: Session = Depends(db_generator), current_user = Depends(get_current_user)):
    return hero.create_hero(db=db, hero=new_hero)

@router.put("/{hero_id}")
def update_hero(hero_id: int, updated_hero: HeroCreate, db: Session = Depends(db_generator), current_user = Depends(get_current_user)):
    return hero.put_hero(db=db, hero=updated_hero, hero_id=hero_id)

@router.delete("/{hero_id}")
def delete_hero(hero_id: int, db: Session = Depends(db_generator), current_user = Depends(get_current_user)):
    return hero.delete_hero(db=db, hero_id=hero_id)