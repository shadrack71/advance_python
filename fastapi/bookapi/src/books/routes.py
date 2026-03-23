
from fastapi import  APIRouter,Header,status ,HTTPException
from typing import Optional, List
from .schemas import  GetBook,BookUpdateModel
from  .data import  books

book_router = APIRouter()

@book_router.get('/test')
async def index():
    return  { 'name':'shadrack'}

@book_router.get('/test/greeting')
async def greeting(age:int,name:Optional[str] = 'shadrack')->dict:
    return  {
        'name':f'Hello {name} , age {age}'
    }

@book_router.post('/test/book')
async  def create_book(book_data):
    return {
        'title':book_data.title,
        'author':book_data.author
    }

@book_router.get('/test/get_header',status_code=200)
async  def get_header(accept:str = Header(None),
                      content_type:str = Header(None),
                      user_agent:str=Header(None),
                      host:str = Header(None)):
    request_header = {'accept':accept,'content-type':content_type,'user_agent':user_agent,'host':host}

    return request_header

#  Creating Simple CRUD


@book_router.get('/',response_model=List[GetBook])
async  def get_all_book()->list:
    return  books

@book_router.post('/', status_code=status.HTTP_201_CREATED)
async  def create_book(book_data:GetBook)->dict:
    new_books = book_data.model_dump()
    books.append(new_books)
    return  new_books


@book_router.get('/{book_id}')
async  def get_all_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            return  book
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Not found')

@book_router.patch('/{book_id}')
async  def update_all_book(book_id:int , book_update_data:BookUpdateModel)->dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.delete('/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async  def delete_all_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return  {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
