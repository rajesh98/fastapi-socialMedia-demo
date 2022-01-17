#from fastapi import FastAPI, Response, status, HTTPException,Depends
#from fastapi.params import Body
#from psycopg2 import extras
from fastapi import FastAPI


#from pydantic.main import Model


from . import  models
from .database import engine
from .routers import user,post,auth,vote

from .  config import settings

from fastapi.middleware.cors import CORSMiddleware
 








#needed to create database when alembic not used
#models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# @app.get("/sqlalchemy")
# def test_post(db:Session = Depends(get_db)):
# 	data = db.query(models.Post).all()
# 	return {"status": data}

#my_post = []







app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {"Hello": "World-successfully deployed to heroku from CI/CD pipeline"}




















	




    






        



       
        

        
       



		
     



