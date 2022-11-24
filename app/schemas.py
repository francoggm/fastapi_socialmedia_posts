from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool] = True

class ResponsePost(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

