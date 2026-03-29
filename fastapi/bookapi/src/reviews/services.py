from fastapi.exceptions import  HTTPException
from typing import Any
from fastapi import status

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from .schemas import ReviewCreateModel
from ..db.models import Review
from ..books.service import BookService
from ..auth.services import UserService
import  logging

book_service = BookService()
user_service = UserService()
class ReviewService:
    async def add_review_to_book(self,user_email:str,book_uid:str,review_data:ReviewCreateModel,session:AsyncSession):
        try:
            book_detail = await book_service.get_book(book_uid,session)
            user_data = await  user_service.get_user_email(user_email,session)
            if book_detail  is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found"
                )
            if user_data  is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            new_review = Review(
                **review_data.model_dump()
            )
            new_review.books=book_detail
            new_review.user_accounts=user_data
            session.add(new_review)
            await session.commit()
            return  new_review



        except Exception as e:
            logging.exception(e)
            raise  HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ooops Something went wrong try again"
            )