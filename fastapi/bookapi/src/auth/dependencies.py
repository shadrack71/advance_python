from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException,status
from .utils import  decode_token

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error =True):
        super().__init__(auto_error=auto_error)
    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token=creds.credentials
        token_data = decode_token(token)
        if  not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid or Expired token')

        if token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Provide Valid token')

        return  token_data


    def token_valid(self,token)->bool:
        token_data = decode_token(token)
        return True if token_data is not None else False