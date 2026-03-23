from typing import Optional

from fastapi import  FastAPI,Header
from pydantic import BaseModel

app = FastAPI()



@app.get('/')
async def index():
    return  { 'name':'shadrack'}

@app.get('/greeting')
async def greeting(age:int,name:Optional[str] = 'shadrack')->dict:
    return  {
        'name':f'Hello {name} , age {age}'
    }

class BookModel(BaseModel):
    title:str
    author:str
@app.post('/book')
async  def create_book(book_data:BookModel):
    return {
        'title':book_data.title,
        'author':book_data.author
    }

@app.get('/get_header',status_code=200)
async  def get_header(accept:str = Header(None),
                      content_type:str = Header(None),
                      user_agent:str=Header(None),
                      host:str = Header(None)):
    request_header = {'accept':accept,'content-type':content_type,'user_agent':user_agent,'host':host}

    return request_header
