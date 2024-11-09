
import oauth2
import models,schemas,utils
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import FastAPI,Response,status,HTTPException,Depends
from database import engine,get_db



route=APIRouter(prefix="",tags=['user'])




@route.post('/user',response_model=schemas.Getuser)
def post_create(user:schemas.User_create,db:Session=Depends(get_db)):
    
    
    
    email=db.query(models.User).filter(models.User.email==user.email).first()
    
    if email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email and pass aleady exits")
       
    
    
    
    hash_pwd = utils.hash(user.password)
    user.password = hash_pwd
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user