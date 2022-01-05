from fastapi import Depends,HTTPException,status,APIRouter
#from fastapi.param_functions import Depends,Depends,
from .. import  models,schemas,auth2
from ..database import get_db

from sqlalchemy.orm import Session

from app import database



router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db:Session = Depends(database.get_db), current_user:int = Depends(auth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {vote.post_id} not found.")
    

    #Found if the current user has voted for the specific post
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if(vote.direction==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Success":"voted"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can not found vote")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Success":"Vote deleted"}
        



