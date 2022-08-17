from enum import unique
import re
from decimal import Decimal
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, Numeric, Date
from sqlalchemy.sql.expression import null


from app.core.database import Base
# from app.utils.exceptions import ValidationError

class User(Base):
    __tablename__ = "user"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    @staticmethod
    def validate_dict(user_dict):
        return user_dict

    @staticmethod
    def _numeric_str_cleaner(string: str):
        # Using regex to delete everything that isnt numeric
        return re.sub("[^0-9]", "" ,string)
   