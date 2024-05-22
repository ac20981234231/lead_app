from sqlalchemy.orm import Session
from . import models, schemas

def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()

def get_lead_by_email(db: Session, email: str):
    return db.query(models.Lead).filter(models.Lead.email == email).first()

def get_leads(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Lead).offset(skip).limit(limit).all()

def create_lead(db: Session, lead: schemas.LeadCreate, resume_path: str):
    db_lead = models.Lead(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        resume_path=resume_path,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def update_lead_state(db: Session, lead: models.Lead, lead_update: schemas.LeadUpdate):
    lead.state = lead_update.state
    db.commit()
    db.refresh(lead)
    return lead
