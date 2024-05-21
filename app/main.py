import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app import models, schemas, crud, database, email_service
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Ensure the database tables are created
models.Base.metadata.create_all(bind=database.engine)

@app.post("/send-test-email")
def send_test_email(db: Session = Depends(database.get_db)):
    test_email = os.getenv("TEST_EMAIL")
    subject = "Test Email"
    body = "This is a test email from FastAPI."
    email_service.send_email(test_email, subject, body)
    return {"message": f"Test email sent to {test_email}"}

@app.post("/leads", response_model=schemas.Lead)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(database.get_db)):
    logger.info(f"Received lead data: {lead}")
    try:
        db_lead = crud.create_lead(db=db, lead=lead)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    logger.info(f"Created lead in DB: {db_lead}")
    email_service.send_email_to_prospect(lead.email)
    email_service.send_email_to_attorney(lead.email)
    return db_lead

@app.get("/leads", response_model=list[schemas.Lead])
def read_leads(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    leads = crud.get_leads(db, skip=skip, limit=limit)
    logger.info(f"Returning leads: {leads}")
    return leads

@app.put("/leads/{lead_id}/state", response_model=schemas.Lead)
def update_lead_state(lead_id: int, state: schemas.LeadStateUpdate, db: Session = Depends(database.get_db)):
    db_lead = crud.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        logger.warning(f"Lead with ID {lead_id} not found")
        raise HTTPException(status_code=404, detail="Lead not found")
    logger.info(f"Updating lead state: {lead_id} to {state.state}")
    db_lead = crud.update_lead_state(db=db, lead=db_lead, state=state)
    logger.info(f"Updated lead: {db_lead}")
    return db_lead
