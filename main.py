from fastapi import FastAPI,Response,status,HTTPException,Depends

from database import engine,get_db
import models,schemas
from sqlalchemy.orm import Session
from typing import List
from Router import auth, post, user, vote



# models.Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user.route)
app.include_router(auth.route)
app.include_router(post.route)
app.include_router(vote.route)


