from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
from hashing import Hash

def create(request: schemas.Users, db: Session):
    new_user = models.Users(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

def get_all(db: Session):
    users = db.query(models.Users).all()
    return users

def destroy_all(db: Session):
    db.query(models.Users).delete(synchronize_session=False)
    db.commit()
    return 'done'
