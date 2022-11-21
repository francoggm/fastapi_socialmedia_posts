from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
import os
from dotenv import load_dotenv

app = FastAPI()
tries = 0
load_dotenv()

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

while tries < 3:
    try:
        conn = psycopg2.connect(host=os.getenv('HOST'), database=os.getenv('DATABASE'), user=os.getenv('USER'), 
        password=os.getenv('PASSWORD'), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('DB Connected')
        break
    except Exception as e:
        print('Error connecting DB ->', e, '\nTrying again!')
        sleep(2)
        tries += 1
        if tries == 3:
            print('Exceded tries, error connecting DB')

@app.get('/')
def root():
    return {"message": "welcome to api"}

@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"posts": posts}

@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if post:
        return {"post": post}
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post {id} not found!")

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"post": new_post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if post:
        cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
        deleted = cursor.fetchone()
        if deleted:
            conn.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found!")

@app.put('/posts/{id}')
def update_post(id: int, update_post: UpdatePost):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if post:
        cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (update_post.title, update_post.content, update_post.published, str(id)))
        updated_post = cursor.fetchone()
        if updated_post:
            conn.commit()
            return {"post": updated_post}
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found!")

@app.get('/posts/latest/')
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1 """)
    post = cursor.fetchone()
    if post:
        return {"post": post}
    

