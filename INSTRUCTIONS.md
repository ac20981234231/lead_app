## Prerequisites
Python 3.9+
Virtual Env (recommended)

## Installation
git clone <repo-url>
cd lead_app

## Create Virtual Env
python3 -m venv venv
source venv/bin/activate

## Install Dependencies
pip3 install -r requirements.txt

## Configure .env File:
Create a .env file in the root directory of the project with the following content:\
EMAIL_HOST=smtp.gmail.com\
EMAIL_PORT=587\
EMAIL_HOST_USER=your-email@gmail.com\
EMAIL_HOST_PASSWORD=your-app-password  # Use an App Password if MFA is enabled\
EMAIL_FROM=your-email@gmail.com\
ATTORNEY_EMAIL=attorney@example.com
SECRET_KEY=your_secret_key

## Running the Application
uvicorn app.main:app --reload

## Accessing the Application
Open browser and go to 'http://127.0.0.1:8000'


## TESTING
---------------------------------------------------------------------------

## CREATING A USER
curl -X POST "http://127.0.0.1:8000/users/" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "testpassword"}'

## GETTING A TOKEN
curl -X POST "http://127.0.0.1:8000/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser&password=testpassword"

## CREATING A LEAD
curl -X POST "http://127.0.0.1:8000/leads" \
    -H "Authorization: Bearer <your_generated_token>" \
    -F "first_name=Daniel" \
    -F "last_name=Smith" \
    -F "email=Daniel.Smith@example.com" \
    -F "resume=@resume.txt"

(assuming resume.txt is in same working directory)

## GETTING LEADS
curl -X GET "http://127.0.0.1:8000/leads" \
    -H "Authorization: Bearer <your_generated_token>"


## TESTING EMAIL SENDING ENDPOINT
curl -X POST "http://127.0.0.1:8000/send-test-email" 

## UPDATE LEAD STATE
curl -X PUT "http://127.0.0.1:8000/leads/1/state" \
    -H "Authorization: Bearer <your_generated_token>" \
    -H "Content-Type: application/json" \
    -d '{"state": "REACHED_OUT"}'


Alternatively, use http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc to test interactively with UI

------------------------------------------------

## Verifying Emails
Ensure SMTP settings are correct. The app attempts to send emails to the provided emails. If encountering issues with sending emails due to security settings, consider generating an App Password for your email account.

## Known Issues
Gmail Authentication Error:
If you encounter an error like (535, b'5.7.8 Username and Password not accepted'), it means the SMTP server rejected the provided credentials. This is likely due to Gmail's security settings.

Solution: Use an App Password if MFA is enabled or allow less secure apps (not recommended).

## NOTES
Submission focuses on core functionalities. Unit tests weren't included to meet the submission deadline.
