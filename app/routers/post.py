from fastapi import  Depends,HTTPException,status,APIRouter,Response
from sqlalchemy.sql.functions import func
#from fastapi.param_functions import Depends,Depends,
from .. import  models,schemas,auth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(
    prefix = "/posts",
    tags = ['posts']
)





@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user:int = Depends(auth2.get_current_user),
limit:int = 10, skip:int = 0, search:Optional[str] = ""):
	# cursor.execute("""SELECT * FROM posts  """)
	# posts = cursor.fetchall()

	#print(limit)
	#posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
	#print(posts)
	
	posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
		models.Vote,models.Post.id == models.Vote.post_id, isouter = True).group_by(
			models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
	

	return posts

 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db:Session = Depends(get_db), 
 current_user:int = Depends(auth2.get_current_user)):   

	# cursor.execute("""INSERT INTO posts (title,content,is_published) VALUES (%s, %s,%s) RETURNING * """,
	# (post.title,post.content,post.published))    
	# new_post = cursor.fetchone()
	# conn.commit()

	#new_post = models.Post(title = post.title, content = post.content, published = post.published)
	
	#print(current_user.email)
	new_post = models.Post(owner_id =current_user.id ,**post.dict())
	db.add(new_post)
	db.commit()
	db.refresh(new_post)
	return new_post 




@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db:Session = Depends(get_db),current_user:int = Depends(auth2.get_current_user)):
	# print(id)
	# cursor.execute("""SELECT * from posts WHERE id = %s """ ,(str(id),))
	# post = cursor.fetchone()
	# print(post)
	#post = db.query(models.Post).filter(models.Post.id == id).first()
	post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
		models.Vote,models.Post.id == models.Vote.post_id, isouter = True).group_by(
			models.Post.id).filter(models.Post.id == id).first()
	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
		detail="No Post found") 
	return post






@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user:int = Depends(auth2.get_current_user)):
	# cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id),))
	# post = cursor.fetchone()
	# conn.commit()
	post_query = db.query(models.Post).filter(models.Post.id == id)

	post = post_query.first()

	if not post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
		"No Post found") 

	if post.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT Authorized to perform requested operation")

	post_query.delete(synchronize_session=False)
	db.commit()
	return Response(status_code=status.HTTP_204_NO_CONTENT)




@router.put("/{id}",response_model=schemas.Post)
def update_post(id : int , post:schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(auth2.get_current_user)):
	# cursor.execute(""" UPDATE posts SET title = %s, content = %s,
	# is_published = %s WHERE id = %s RETURNING * """,
	# (post.title,post.content,post.published, str(id),))
	# post = cursor.fetchone()
	# conn.commit()
	post_query = db.query(models.Post).filter(models.Post.id == id)
	updated_post = post_query.first()

	if not updated_post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
		"No Post Found ") 

	if updated_post.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOT Authorized to perform requested operation")

	post_query.update(post.dict(),synchronize_session=False)
	db.commit()

	return post_query.first()