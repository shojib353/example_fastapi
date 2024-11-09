from ast import Str
from datetime import datetime
from operator import le
from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from typing_extensions import Annotated

# class Post(BaseModel):
#     title:str
#     content:str
#     punlishec:bool=False
#     rat: Optional[int]=None

class Posts(BaseModel):
    title:str
    content:str


class User_out(BaseModel):
    id:int
    email:str
    password:str
    created_at:datetime 

    class Config:
        from_attributes  = True


class Getpost(BaseModel):
    title:str
    content:str
    created_at:datetime
    id:int
    owner_id:int
    owner:User_out

    class Config:
        from_attributes  = True









class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None









class Getuser(BaseModel):
    
    email:EmailStr
    password:str
   

    class Config:
        from_attributes  = True

class User_create(BaseModel):
    
    email:EmailStr
    password:str

class User_login(BaseModel):
    
    email:str
    password:str




class Token(BaseModel):
    Token:str
    Token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None



class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, Field(strict=True, le=1)]


class Getpost2(BaseModel):
        Post:Getpost
        votes:int


        class Config:
             from_attributes  = True

    

    
