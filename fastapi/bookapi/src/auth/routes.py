from datetime import timedelta, datetime

from argon2 import hash_password
from fastapi import  APIRouter ,Depends,status,HTTPException
from fastapi.responses import JSONResponse

from ..config import Config
from ..db.main import get_session
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserBookModel,EmailModel,PasswordResetModel,PasswordResetConfirmModel
from .services import UserService
from .utils import create_access_token,decode_token,password_verify ,create_url_safe_token,decode_url_safe_token,generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from  .dependencies import RefreshTokenBearer , get_current_user ,RoleChecker
from ..db.redis import add_jwi_to_blocklist
from ..errors import (InvalidToken ,RevokedToken,AccessTokenRequired,RefreshTokenRequired,
                      UserAlreadyExists,InvalidCredentials,InsufficientPermission,
                      BookNotFound,TagNotFound,TagAlreadyExists,UserNotFound ,PasswordMismatch)

from ..mail import mail,create_email

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin','user'])

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post('/send_email')
async def send_email(emails:EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the bookly app</h1>"
    msg = create_email(recipients=emails,subject="welcome",body=html)
    await mail.send_message(msg)
    return {"message":"email sent successfully"}

@auth_router.post('/signup', response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def  create_user_account(user_data:UserCreateModel,session:AsyncSession = Depends(get_session)):

    user_email = user_data.email
    user_exist = await user_service.user_exist(user_email,session)
    if user_exist:
        raise UserAlreadyExists()
        # return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user with email exist')

    new_user = await user_service.create_user(user_data, session)
    token = create_url_safe_token({"email": user_email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html_message = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
        """

    message = create_email(
        recipients=[user_email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    return {
        "message": "Account Created! Check email to verify your account",
        "user": new_user,
    }
    # return new_user

@auth_router.get('/verify/{token}')
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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
                'user_uid':str(user_data.uid),
                'role':user_data.role
            }
            refresh_token_ = create_access_token(user_payload,refresh=True, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))
            access_token = create_access_token(user_payload)

            return  JSONResponse(
                content={
                    "message":"login Successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token_,
                    "user":{
                        "email":user_data.email,
                        "uid":str(user_data.uid)
                    }
                }
            )
        else:
            raise InvalidCredentials()
            # return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid password and email')
    else:
        raise UserNotFound()
        # return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user not found')

@auth_router.get('/refresh_token')
async  def refresh_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])
        return  JSONResponse(content={"access_token":new_access_token})
    raise InvalidToken()
    # raise HTTPException(
    #     status_code=status.HTTP_400_BAD_REQUEST , detail="Invalid Or expired token"
    # )

@auth_router.get('/me',response_model=UserBookModel)
async  def get_current_user(user = Depends(get_current_user),_:bool = Depends(role_checker)):
    return user

@auth_router.get('/logout')
async def revoke_token(token_details:dict = Depends(RefreshTokenBearer())):
    jti =token_details['jti']
    # await add_jwi_to_blocklist(jti)
    return  JSONResponse(
        content={
            "message":"Logged Out Successfully "
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post('/password-reset')
async def password_reset(email_data:PasswordResetModel , session:AsyncSession = Depends(get_session)):
    user_email = email_data.email
    user_exist = await user_service.user_exist(user_email, session)
    if not user_exist:
        raise UserNotFound()
        # return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user with email exist')
    token = create_url_safe_token({"email": user_email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
            <h1>Verify your Email</h1>
            <p>Please click this <a href="{link}">link</a>  reset your password</p>
            """

    message = create_email(
        recipients=[user_email], subject="Reset your password", body=html_message
    )

    await mail.send_message(message)

    return  JSONResponse(
        content={"message":"Please check your email for instruction to reset your password"},status_code=status.HTTP_200_OK
    )

@auth_router.get('/password-reset-confirm/{token}')
async def password_reset_confirm(token:str,update_data:PasswordResetConfirmModel,session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)
    updated_data = update_data.model_dump()

    user_email = token_data.get("email")

    if user_email:
        user = await user_service.get_user_email(user_email, session)

        if not user:
            raise UserNotFound()

        if updated_data['new_password'] != updated_data['confirm_password']:
            raise PasswordMismatch()
        hash_new_password = generate_password_hash(updated_data['new_password'])

        await user_service.update_user(user, {"password_hash":hash_new_password}, session)

        return JSONResponse(
            content={"message": "Password reset successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


