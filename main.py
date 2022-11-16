from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get('/')
def root():
    return {"message": "welcome to api"}

@app.get('/posts')
def get_posts():
    return {"data": "One post"}

@app.post('/createposts')
def create_post(post: Post):
    print(post)
    return {"data": post}