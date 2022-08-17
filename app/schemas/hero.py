from datetime import date
from decimal import Decimal

from pydantic import BaseModel
from app.models.hero import Hero, HeroRanks

class HeroBase(BaseModel):
    name : str
    rank : HeroRanks
    lat : Decimal
    long : Decimal
    available : bool

class HeroCreate(HeroBase):
    pass

class Hero(HeroBase):
    id : int

    class Config:
        orm_mode = True