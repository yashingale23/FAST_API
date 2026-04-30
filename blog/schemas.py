from typing import List
from pydantic import BaseModel
from typing import Optional

class blog(BaseModel):
    title:str
    body:str
    class Config():
        from_attributes=True



class Users(BaseModel):
    name:str
    password:str
    email:str

class Showusers(BaseModel):
    name:str
    email:str
    blogs:List[blog]=[]
    class Config():
        from_attributes=True

class Showblog(BaseModel):
    title:str
    body:str
    creator:Optional[Showusers]
    class Config():
        from_attributes=True