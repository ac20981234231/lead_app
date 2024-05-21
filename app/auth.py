from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str

def get_current_user(token: str = Depends(oauth2_scheme)):
    # For simplicity, simply returns a dummy user for all requests.
    # In "real life" would verify token + fetch user from DB.
    return User(username="dummy_user")
