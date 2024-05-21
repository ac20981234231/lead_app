from sqlalchemy.orm import Session
from app import models, schemas

def create_lead(db: Session, lead: schemas.LeadCreate):
    existing_lead = db.query(models.Lead).filter(models.Lead.email == lead.email).first()
    if existing_lead:
        raise ValueError("A lead with this email already exists")
    
    db_lead = models.Lead(
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        resume=lead.resume
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_leads(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Lead).offset(skip).limit(limit).all()

def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()

def update_lead_state(db: Session, lead: models.Lead, state: schemas.LeadStateUpdate):
    lead.state = state.state
    db.commit()
    db.refresh(lead)
    return lead
