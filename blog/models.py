from operator import index
from sqlalchemy import Column, Integer,String, ForeignKey
from database import base
from sqlalchemy.orm import relationship

class Blog(base):
    __tablename__='blogs'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    body=Column(String)
    user_id=Column(Integer,ForeignKey('users.id'))
    creator=relationship("Users",back_populates="blogs")

class Users(base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    password=Column(String)
    email=Column(String)
    blogs=relationship("Blog",back_populates="creator")