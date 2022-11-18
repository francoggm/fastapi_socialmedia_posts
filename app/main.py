from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool] = True
    rating: Optional[int] = None

my_posts = [{"title": "post 1", "content": "content post 1", "id": 1}, {"title": "post 2", "content": "content post 2", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post.get('id') == id:
            return post

@app.get('/')
def root():
    return {"message": "welcome to api"}

@app.get('/posts')
def get_posts():
    return {"posts": my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1_000_000)
    my_posts.append(post_dict)
    return {"post": post_dict}

@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[-1]
    return {"post": post}

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post = find_post(id)
    if post:
        return {"post": post}
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post {id} not found!")

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id)
    if post:
        my_posts.remove(post)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found!")

@app.put('/posts/{id}')
def update_post(id: int, update_post: UpdatePost):
    post = find_post(id)
    update_post = update_post.dict()
    if post:
        my_posts.remove(post)
        if update_post.get('title'):
            post['title'] = update_post['title']
        if update_post.get('content'):
            post['content'] = update_post['content']
        if update_post.get('published'):
            post['published'] = update_post['published']
        if update_post.get('rating'):
            post['rating'] = update_post['rating']
        my_posts.append(post)
        return {"post": post}
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found!")
    

