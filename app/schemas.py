from pydantic import BaseModel
from typing import Optional
from enum import Enum

class LeadState(str, Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    state: LeadState

class Lead(LeadBase):
    id: int
    resume_path: Optional[str]
    state: LeadState

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
