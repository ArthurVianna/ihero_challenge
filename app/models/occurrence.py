import datetime
from email.policy import default
from random import randint
import enum

from sqlalchemy import Enum
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.hero import HeroRanks

class OccurrenceRanks(enum.Enum):
    GOD = 1
    DRAGON = 2
    TIGER = 3
    WOLF = 4

    @classmethod
    def getByRankName(cls, rankName :str):
        if rankName == "God":
            return cls.GOD
        if rankName == "Dragon":
            return cls.DRAGON
        if rankName == "Tiger":
            return cls.TIGER
        if rankName == "Wolf":
            return cls.WOLF

    def get_possible_attending_hero_rank(self):
        if self.name == "GOD":
            return [HeroRanks.RANKS,HeroRanks.RANKA,HeroRanks.RANKB,HeroRanks.RANKC]
        if self.name == "DRAGON":
            return [HeroRanks.RANKA,HeroRanks.RANKB,HeroRanks.RANKC]
        if self.name == "TIGER":
            return [HeroRanks.RANKB,HeroRanks.RANKC]
        if self.name == "WOLF":
            return [HeroRanks.RANKC]

class Occurrence(Base):
    __tablename__ = "occurrence"


    id = Column(Integer, primary_key=True, index=True)
    monster_name = Column(String, nullable=False)
    rank = Column(Enum(OccurrenceRanks), nullable=False, default=OccurrenceRanks.WOLF)
    lat = Column(Numeric, nullable=False, default=0)
    long = Column(Numeric, nullable=False, default=0)
    create = Column(DateTime, server_default=func.now())
    start = Column(DateTime, nullable=True)
    finish = Column(DateTime, nullable=True)
    heroes = relationship("Attendance", back_populates="occurrence")

    @staticmethod
    def validate_dict(user_dict):
        return user_dict
    
    def calculate_finish_time(self):
        args = {}
        if self.rank == OccurrenceRanks.GOD:
            args["minutes"] = randint(5,10)
        elif self.rank == OccurrenceRanks.DRAGON:
            args["minutes"] = randint(2,5)
        elif self.rank == OccurrenceRanks.TIGER:
            args["seconds"] = randint(10,20)
        elif self.rank == OccurrenceRanks.WOLF:
            args["seconds"] = randint(1,2)

        return datetime.datetime.now() + datetime.timedelta(**args)


class Attendance(Base):
    __tablename__ = "Attendance"

    hero_id = Column(ForeignKey("hero.id"), primary_key=True)
    occurrence_id = Column(ForeignKey("occurrence.id"), primary_key=True)
    hero = relationship("Hero", back_populates="occurrences")
    occurrence = relationship("Occurrence", back_populates="heroes")  
