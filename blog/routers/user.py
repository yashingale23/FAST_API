from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
import schemas, database, oauth2
from repository import user as user_repo

router = APIRouter(
    prefix="/user",
    tags=['users']
)

get_db = database.get_db

@router.post('/', status_code=status.HTTP_202_ACCEPTED)
def create_users(request: schemas.Users, db: Session = Depends(get_db)):
    return user_repo.create(request, db)

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Showusers])
def get_users(db: Session = Depends(get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    return user_repo.get_all(db)

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Showusers)
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    return user_repo.show(id, db)

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_all_users(db: Session = Depends(get_db), current_user: schemas.Users = Depends(oauth2.get_current_user)):
    return user_repo.destroy_all(db)
