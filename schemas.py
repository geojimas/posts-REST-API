from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from models import Post


#------------------------------
### Post Schemas
#------------------------------


# Properties to receive on Posts creation & Post edit
class PostCreation(BaseModel):
    title: Optional[str]
    content: Optional[str]



# Properties to receive on Posts reading
class Post(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True





#------------------------------
### User Schemas
#------------------------------


# Properties to receive on User creation
class UserCreation(BaseModel):
    password: str
    email: str


# Properties to receive on User reading
class User(BaseModel):
    id: int
    email: str
    password: str
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    posts: list[Post] = []
    
    class Config:
        orm_mode = True
