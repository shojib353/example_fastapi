from pyexpat import model
import models,schemas,utils,oauth2
from fastapi import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import FastAPI,Response,status,HTTPException,Depends
from database import engine,get_db

route=APIRouter(prefix="",
                 tags=["vote"])

@route.post("/votepost",status_code=status.HTTP_201_CREATED)
async def post_vote(votes:schemas.Vote,db:Session=Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==votes.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()

    
    
    if (votes.dir==1):
        if found_vote:
             raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                  detail=f"user {current_user.id} has already post vote {votes.post_id}") 
        new_vote=models.Vote(post_id=votes.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"sms":"successfully add a vot"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="vote is not exists") 
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"sms":"deleted a vot"}




