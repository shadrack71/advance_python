from fastapi import APIRouter, Header, status, HTTPException, Depends
from typing import Optional, List

from fastapi.params import Depends

from .schemas import GetBook, BookUpdateModel, BookCreateModel ,BookDetailModel
# from  .data import  books
from ..db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService

from ..auth.dependencies import  AccessTokenBearer ,RoleChecker

book_router = APIRouter()

role_checker = Depends(RoleChecker(['admin','user']))

@book_router.get('/test')
async def index():
    return {'name': 'shadrack'}


@book_router.get('/test/greeting')
async def greeting(age: int, name: Optional[str] = 'shadrack') -> dict:
    return {
        'name': f'Hello {name} , age {age}'
    }


@book_router.post('/test/book')
async def create_book(book_data):
    return {
        'title': book_data.title,
        'author': book_data.author
    }


@book_router.get('/test/get_header', status_code=200)
async def get_header(accept: str = Header(None),
                     content_type: str = Header(None),
                     user_agent: str = Header(None),
                     host: str = Header(None)):
    request_header = {'accept': accept, 'content-type': content_type, 'user_agent': user_agent, 'host': host}

    return request_header

#  Creating Simple CRUD
book_service = BookService()
access_token_bearer = AccessTokenBearer()

@book_router.get('/', response_model=List[BookDetailModel],dependencies=[role_checker])
async def get_all_book(session: AsyncSession = Depends(get_session),user_details=Depends(access_token_bearer)) -> dict:
    # print(user_details)
    books = await book_service.get_all_books(session)
    return books

@book_router.get('/user/{user_id}', response_model=List[BookDetailModel],dependencies=[role_checker])
async def get_user_books(user_id:str,session: AsyncSession = Depends(get_session),user_details=Depends(access_token_bearer)) -> dict:
    books = await book_service.get_users_books(user_id,session)
    return books

@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookCreateModel,dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session),user_details:dict=Depends(access_token_bearer)) -> dict:
    user_id = user_details.get('user')['user_uid']
    new_book = await book_service.create_books(book_data,user_id,session)
    return new_book


@book_router.get('/{book_uid}', response_model=BookDetailModel,dependencies=[role_checker])
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session),user_details=Depends(access_token_bearer)):
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book Not found')

@book_router.patch('/{book_uid}',status_code=status.HTTP_200_OK,response_model=BookUpdateModel,dependencies=[role_checker])
async def update_book(book_uid: str, book_update_data: BookUpdateModel,
                      session: AsyncSession = Depends(get_session),user_details=Depends(access_token_bearer)) -> dict:
    update_book_data = await book_service.update_books(book_uid, book_update_data,session)
    if update_book_data:
        return update_book_data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT,dependencies=[role_checker])
async def delete_all_book(book_uid: str, session: AsyncSession = Depends(get_session),user_details=Depends(access_token_bearer)):
    delete_book = await book_service.delete_books(book_uid, session)
    if delete_book:
        return delete_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
