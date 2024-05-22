from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import shutil
from datetime import timedelta
from fastapi.responses import FileResponse

from . import crud, models, schemas, database, email_service, auth

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/leads", response_model=schemas.Lead)
def create_lead(
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    email: str = Form(...), 
    resume: UploadFile = File(...), 
    db: Session = Depends(database.get_db), 
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_lead = crud.get_lead_by_email(db, email=email)
    if db_lead:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Save resume file in the current working directory
    file_location = resume.filename
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    
    lead_in = schemas.LeadCreate(first_name=first_name, last_name=last_name, email=email)
    db_lead = crud.create_lead(db=db, lead=lead_in, resume_path=file_location)
    return db_lead

@app.get("/leads", response_model=List[schemas.Lead])
def read_leads(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    leads = crud.get_leads(db, skip=skip, limit=limit)
    return leads

@app.put("/leads/{lead_id}/state", response_model=schemas.Lead)
def update_lead_state(lead_id: int, lead: schemas.LeadUpdate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    db_lead = crud.get_lead(db, lead_id=lead_id)
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return crud.update_lead_state(db=db, lead=db_lead, lead_update=lead)

@app.post("/send-test-email")
def send_test_email():
    email_service.send_email_to_prospect("test@example.com")
    email_service.send_email_to_attorney("test@example.com")
    return {"message": "Test emails sent"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/resumes/{filename}", response_class=FileResponse)
def get_resume(filename: str):
    file_path = f"./{filename}"
    return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)


