import enum

from sqlalchemy import Enum
from sqlalchemy import Boolean, Column, Integer, String, Numeric
from sqlalchemy.orm import relationship


from app.core.database import Base

class HeroRanks(enum.Enum):
    RANKS = 1
    RANKA = 2
    RANKB = 3
    RANKC = 4

class Hero(Base):
    __tablename__ = "hero"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rank = Column(Enum(HeroRanks), nullable=False, default=HeroRanks.RANKC)
    lat = Column(Numeric, nullable=False, default=0)
    long = Column(Numeric, nullable=False, default=0)
    available = Column(Boolean, nullable=False, default=True)
    occurrences = relationship("Attendance", back_populates="hero")

    @staticmethod
    def validate_dict(user_dict):
        return user_dict