from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
app=FastAPI()

models.base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.blog, db:Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',status_code=status.HTTP_200_OK, response_model=List[schemas.Showblog], tags=['blogs'])
def show(db:Session=Depends(get_db)):
    blog=db.query(models.Blog).all()
    return blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
def delee(id: int, db:Session=Depends(get_db)):
    deleted_blog=db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'deleted'}

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request:schemas.blog, db:Session=Depends(get_db)):
    blogs=db.query(models.Blog).filter(models.Blog.id==id)
    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blogs.update(request.dict(), synchronize_session=False)
    db.commit()
    return 'updated'


@app.get('/blog/{id}', status_code=200, response_model=schemas.Showblog, tags=['blogs'])
def shows(id: int, response:Response, db:Session=Depends(get_db)):
    blog1=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog with id {id} is not available")
    #response.status_code=status.HTTP_404_NOT_FOUND --> for using custom not f=default, that is 200 will not be used and 404 will be used
    #return {detail:f"blog with id {id} is not available"}
    return blog1

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

@app.post('/users',status_code=status.HTTP_202_ACCEPTED, tags=['users'])
def create_users(request:schemas.Users, db:Session=Depends(get_db)):
    hashed_password=pwd_cxt.hash(request.password)
    new_user=models.Users(name=request.name,email=request.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/users',status_code=status.HTTP_200_OK,response_model=List[schemas.Showusers], tags=['users'])
def get_users(db:Session=Depends(get_db)):
    users=db.query(models.Users).all()
    return users

@app.get('/users/{id}',status_code=status.HTTP_200_OK,response_model=schemas.Showusers, tags=['users'])
def get_user(id: int, db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user

@app.delete('/users', status_code=status.HTTP_204_NO_CONTENT, tags=['users'])
def delete_all_users(db: Session = Depends(get_db)):
    db.query(models.Users).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'all users deleted'}