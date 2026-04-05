from typing import List, Any

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status, Depends
from .utils import  decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session
from ..db.models import  User

# from ..db.redis import add_jwi_to_blocklist ,token_in_blocklist
from .services import  UserService

from ..errors import (InvalidToken ,RevokedToken,AccessTokenRequired,RefreshTokenRequired,
                      UserAlreadyExists,InvalidCredentials,InsufficientPermission,
                      BookNotFound,TagNotFound,TagAlreadyExists,UserNotFound,AccountNotVerified)

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error =True):
        super().__init__(auto_error=auto_error)
    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token=creds.credentials
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise InvalidToken()
            # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid or Expired token')

        # if await token_in_blocklist(token_data['jti']):
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error":"Invalid or Revoked token",
        #                                                                        "resolution":"Please get new token"})

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self,token)->bool:
        token_data = decode_token(token)
        return True if token_data is not None else False

    def verify_token_data(self,token_data):
        raise NotImplemented("Please Override this call in child class ")
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()
            # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Provide Access Valid token')

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict) -> None:
        if token_data and not token_data['refresh']:
            raise RefreshTokenRequired()
            # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Provide Refresh Valid token')


async def get_current_user(session:AsyncSession = Depends(get_session),token_details:dict = Depends(AccessTokenBearer())):
    user_email = token_details['user']['email']
    user_data = await user_service.get_user_email(user_email,session)
    return user_data

class RoleChecker:
    def __init__(self,allowed_roles:List[str])->None:
        self.allowed_roles = allowed_roles

    async  def __call__(self, current_user:User = Depends(get_current_user))->Any:
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()
        # raise HTTPException(
        #     status_code=status.HTTP_403_FORBIDDEN,
        #     detail="You do not have the permission to perform the action"
        # )
