from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter()

@router.get('/')
def root():
    return {"message": "welcome to api"}

@router.get('/posts', response_model = List[schemas.ResponsePost])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()
    return posts

@router.get('/posts/{id}', response_model = schemas.ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
 
    post = db.query(models.Post).filter_by(id = id).first() 
    if post:
        return post
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post {id} not found!")

@router.post('/posts', status_code = status.HTTP_201_CREATED, response_model = schemas.ResponsePost)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.dict(exclude_unset=True))
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter_by(id = id).first() 
    if post:
        # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
        # deleted = cursor.fetchone()
        # conn.commit()

        db.delete(post)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {id} not found!")

@router.put('/posts/{id}', response_model = schemas.ResponsePost)
def update_post(id: int, update_post: schemas.UpdatePost, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    query = db.query(models.Post).filter_by(id = id)
    post = query.first()
    if post:
        # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (update_post.title, update_post.content, update_post.published, str(id)))
        # updated_post = cursor.fetchone()
        # conn.commit()

        query.update(update_post.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return query.first()
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Post not found!")

@router.get('/posts/latest/', response_model = schemas.ResponsePost)
def get_latest_post(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1 """)
    # post = cursor.fetchone()

    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if post:
        return post