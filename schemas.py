# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    user_id: int

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str
    status: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class PostWithRelations(Post):
    user: Optional[User]
    comments: Optional[List[Comment]]
    tags: Optional[List[Tag]]

class UserWithRelations(User):
    posts: Optional[List[Post]]
    comments: Optional[List[Comment]]