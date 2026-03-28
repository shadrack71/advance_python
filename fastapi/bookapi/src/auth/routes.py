from datetime import timedelta

from fastapi import  APIRouter ,Depends,status,HTTPException
from fastapi.responses import JSONResponse

from ..db.main import get_session
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .services import UserService
from .utils import create_access_token,decode_token,password_verify
from sqlmodel.ext.asyncio.session import AsyncSession

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post('/signup', response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def  create_user_account(user_data:UserCreateModel,session:AsyncSession = Depends(get_session)):

    user_email = user_data.email
    user_exist = await user_service.user_exist(user_email,session)
    if user_exist:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user with email exist')

    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post('/signin')
async def user_login(user_login_data:UserLoginModel,session:AsyncSession = Depends(get_session)):
    email = user_login_data.email
    password = user_login_data.password
    user_exist = await user_service.user_exist(email,session)
    if user_exist:
        user_data = await user_service.get_user_email(email,session)
        password_match = password_verify(password,user_data.password_hash)
        if password_match:
            user_payload = {
                'email':user_data.email,
                'user_uid':str(user_data.uid)
            }
            refresh_token = create_access_token(user_payload,refresh=True, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))
            access_token = create_access_token(user_payload)

            return  JSONResponse(
                content={
                    "message":"login Successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user_data.email,
                        "uid":str(user_data.uid)
                    }
                }
            )
        else:
            return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid password and email')
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user not found')

    pass
