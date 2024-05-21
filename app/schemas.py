from pydantic import BaseModel, EmailStr

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    resume: str

class LeadCreate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    state: str

    class Config:
        orm_mode = True

class LeadStateUpdate(BaseModel):
    state: str

    class Config:
        orm_mode = True
