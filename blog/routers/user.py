from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, models, database
import hashing
Hash = hashing.Hash

router = APIRouter(
    prefix="/user",
    tags=['users']
)

get_db = database.get_db

@router.post('/', status_code=status.HTTP_202_ACCEPTED)
def create_users(request: schemas.Users, db: Session = Depends(get_db)):
    new_user = models.Users(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.Showusers])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.Showusers)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_all_users(db: Session = Depends(get_db)):
    db.query(models.Users).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'all users deleted'}
