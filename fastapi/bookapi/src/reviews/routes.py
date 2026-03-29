from fastapi import APIRouter, Depends,status
from .schemas import ReviewCreateModel ,ReviewModel
from .services import ReviewService
from ..db.models import User
from  ..auth.dependencies import  get_current_user ,RoleChecker
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session

review_router = APIRouter()

review_service = ReviewService()


@review_router.get('/')
async  def get_all_review():
    pass


@review_router.post('/book/{book_uid}',status_code=status.HTTP_201_CREATED)
async def add_review(book_uid:str,review_data:ReviewCreateModel,
                     current_user:User = Depends(get_current_user),
                     session:AsyncSession = Depends(get_session)):
    user_email = current_user.email
    new_review = await review_service.add_review_to_book(
        user_email=user_email,
        book_uid=book_uid,
        review_data=review_data,
        session=session
    )

    return new_review
