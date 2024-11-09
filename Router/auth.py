
import models,schemas,utils,oauth2
from fastapi import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import FastAPI,Response,status,HTTPException,Depends
from database import engine,get_db



route=APIRouter(prefix="",tags=['Auth'])




@route.post('/login')
def get_login(user:schemas.User_login,db:Session=Depends(get_db)):
    
    
    
    user_detail=db.query(models.User).filter(models.User.email==user.email).first()
    
    if not user_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credintials")
    
    if not utils.verify(user.password,user_detail.password) :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="password not match") 
    
    access_token =oauth2.create_access_token(data={"user_id":user_detail.id})

    #create token
    return {"token":access_token,"tokenItype":"bearer"}



#2nd wey useing oauth2 user class

@route.post('/login2',response_model=schemas.Token)
def get_login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    
    
    
    user_detail=db.query(models.User).filter(models.User.email==user.username).first()
    
    if not user_detail:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credintials")
    
    if not utils.verify(user.password,user_detail.password) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="password not match") 
    
    access_token =oauth2.create_access_token(data={"user_id":user_detail.id})

    #create token
    return {"Token":access_token,"Token_type":"Bearer"}