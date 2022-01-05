from fastapi import Depends,HTTPException,status
from jose import jwt 
from datetime import datetime,timedelta
from jose.exceptions import JWTError
from sqlalchemy.orm import Session


from app import models
from . import schemas,database
from fastapi.security import OAuth2PasswordBearer
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




# to get a string like this run:
# openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    #if expires_delta:
       # expire = datetime.now() + expires_delta
    #else:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithim)
    return encoded_jwt



def verify_access_token(token:str, credentials_exception):

   try: 

      payload = jwt.decode(token,settings.secret_key,algorithms=settings.algorithim)
      id:str = payload.get("user_id")

      if id is None:
         raise credentials_exception
      
      token_data = schemas.TokenData(id = id)
   except JWTError:

      raise credentials_exception

   return token_data

   

   

def get_current_user(token:str = Depends(oauth2_scheme), db:Session =  Depends(database.get_db) ):

   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
   detail=f"Count not verify Credentials", headers={"WWW-Authenticate": "Bearer"})

   token = verify_access_token(token,credentials_exception)

   user = db.query(models.User).filter(models.User.id==token.id).first()



   return user


      
















