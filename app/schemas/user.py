from datetime import date
from decimal import Decimal

# pylint might have a problem with this pydantic import
# add this exception in ".pylintrc" so pylint ignores imports from pydantic
# "--extension-pkg-whitelist=pydantic"
from pydantic import BaseModel

class UserBase(BaseModel):
    name : str
    email : str
    password : str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id : int

    class Config:
        orm_mode = True