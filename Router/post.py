

from typing import List, Optional
from Router import vote
import oauth2
import models,schemas,utils
from fastapi import APIRouter
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func
from fastapi import FastAPI,Response,status,HTTPException,Depends
from database import engine,get_db



route=APIRouter(prefix="",tags=['posts'])




@route.post('/post',response_model=schemas.Getpost)
def post_create(post:schemas.Posts,db:Session=Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    
    
    
    title=db.query(models.Post).filter(models.Post.title==post.title).first()
    
    if title:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post aleady exits")
       
    
#     print(current_user.email)
    

    new_user=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user











@route.get('/post/item',response_model=List[schemas.Getpost2])
# @route.get('/post/item')
def post_show(db:Session=Depends(get_db),
                current_user=Depends(oauth2.get_current_user),limit:int=None,skip:int=None,search:Optional[str]=""):
    
    posts_votes=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    
    user_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    if not user_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found for this user")
    
    return posts_votes
     

















# @route.delete('/post2/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def post_delete(
#     id: int,
#     db: Session = Depends(get_db),
#     current_user = Depends(oauth2.get_current_user)
# ):
#     # Fetch the specific post to delete
#     post_to_delete = db.query(models.Post).filter(models.Post.id == id).first()
    
#     # Check if the post exists
#     if not post_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    
#     # Check if the current user is the owner of the post
#     if post_to_delete.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    
#     # Delete the post
#     db.delete(post_to_delete)
#     db.commit()
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



@route.delete('/post/{id}',status_code=status.HTTP_204_NO_CONTENT)
def post_delete(id:int,db:Session=Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    
    
    
    d_posts = db.query(models.Post).filter(models.Post.id == id)

    e_post=d_posts.first()
    
    if not d_posts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found for this user")
    if e_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    
    d_posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

















@route.put('/post/{id}', response_model=schemas.Getpost)
def update_post(
    id: int,
    updated_post: schemas.UpdatePost,  # Using the schema for updating
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)
):
    # Fetch the post to update
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # Check if the post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Check if the current user is the owner of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    
    # Update only the provided fields
    update_data = updated_post.dict(exclude_unset=True)  # Exclude fields not set by the user
    post_query.update(update_data, synchronize_session=False)
    db.commit()
    
    # Refresh and return the updated post
    db.refresh(post)
    return post