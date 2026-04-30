from fastapi import APIRouter, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session
import schemas, models, database

router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)

get_db = database.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Showblog])
def show(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delee(id: int, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'deleted'}

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.blog, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id == id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blogs.update(request.dict(), synchronize_session=False)
    db.commit()
    return 'updated'

@router.get('/{id}', status_code=200, response_model=schemas.Showblog)
def shows(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not available")
    return blog
