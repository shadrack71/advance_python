import uuid
from datetime import datetime
from typing import List
from ..books.schemas import UserBook,BookDetailModel
from pydantic import  BaseModel , Field ,ConfigDict

from ..reviews.schemas import ReviewModel


class UserCreateModel(BaseModel):
    username:str = Field(max_length=8)
    email: str = Field(max_length=40)
    first_name: str =Field(max_length=20)
    last_name: str =Field(max_length=20)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uid: uuid.UUID
    username: str
    first_name: str
    last_name: str
    is_verified: bool
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime

class UserBookModel(UserModel):
    books: List[BookDetailModel]
    reviews:List[ReviewModel]


class UserLoginModel(BaseModel):
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str
