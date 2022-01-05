from fastapi import FastAPI, Depends,HTTPException,status,APIRouter
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
#from fastapi.param_functions import Depends,Depends,
from .. import  models,schemas,auth2 
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from .. import utils


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login",response_model=schemas.Token)
def login(user_credentional: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email==user_credentional.username).first()

    if not user:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credentional.password,user.password):
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = auth2.create_access_token(data = {"user_id": user.id}) #Payload sectin--can also pro vide
    # some extra info, and scope of different endpoint, user previlage

    return {"access_token": access_token, "token_type" : "bearer"}

