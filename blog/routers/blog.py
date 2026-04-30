from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session
import schemas, database
from repository import blog as blog_repo

router = APIRouter(
    prefix="/blog",
    tags=['blogs']
)

get_db = database.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.blog, db: Session = Depends(get_db)):
    return blog_repo.create(request, db)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Showblog])
def show(db: Session = Depends(get_db)):
    return blog_repo.get_all(db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delee(id: int, db: Session = Depends(get_db)):
    return blog_repo.destroy(id, db)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.blog, db: Session = Depends(get_db)):
    return blog_repo.update(id, request, db)

@router.get('/{id}', status_code=200, response_model=schemas.Showblog)
def shows(id: int, db: Session = Depends(get_db)):
    return blog_repo.show(id, db)
