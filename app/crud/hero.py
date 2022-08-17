
from sqlalchemy import update, delete
from sqlalchemy.orm import Session

from app.models.hero import Hero, HeroRanks
from app.schemas.hero import HeroCreate



def get_hero(db: Session, hero_id: int):
    return db.query(Hero).filter(Hero.id == hero_id).first()
    
def create_hero(db: Session, hero: HeroCreate):
    db_hero = Hero(
        name=hero.name,
        rank=hero.rank,
        lat= hero.lat,
        long= hero.long,
        available= hero.available
    )
    db.add(db_hero)
    db.commit()
    db.refresh(db_hero)
    return db_hero

def put_hero(db: Session, hero: HeroCreate, hero_id: int):
    stmt = update(Hero).where(Hero.id == hero_id).values(
        name=hero.name,
        rank=hero.rank,
        lat=str(hero.lat),
        long=str(hero.long),
        available=hero.available
    ).execution_options(synchronize_session="fetch")

    result = db.execute(stmt)
    db.commit()

    return result.rowcount
    
def delete_hero(db: Session, hero_id: int):
    stmt = delete(Hero).where(Hero.id == hero_id).execution_options(synchronize_session="fetch")
    result = db.execute(stmt)
    db.commit()

    return result.rowcount

def get_heros(db: Session, skip: int = 0, limit: int = 100): 
    return db.query(Hero).offset(skip).limit(limit).all()