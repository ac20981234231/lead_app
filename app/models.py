from sqlalchemy import Column, Integer, String, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class LeadState(enum.Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    resume_path = Column(String)
    state = Column(Enum(LeadState), default=LeadState.PENDING)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
