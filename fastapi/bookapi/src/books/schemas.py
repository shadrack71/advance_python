import uuid
from  datetime import  datetime
from typing import List
from ..reviews.schemas import ReviewModel

from pydantic import BaseModel

class GetBook(BaseModel):
    uid:uuid.UUID
    title :str
    author :str
    publisher:str
    published_date:str
    page_count:int
    language:str
    created_at:datetime
    updated_at:datetime
    #add the user relationship
class BookDetailModel(GetBook):
    reviews:List[ReviewModel]

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class UserBook(BaseModel):
    uid:uuid.UUID
    title :str
    author :str
    publisher:str
    published_date:str
    page_count:int
    language:str
    created_at:datetime
    updated_at:datetime
    user_uid:uuid.UUID