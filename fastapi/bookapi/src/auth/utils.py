# from passlib.context import CryptContext
#
# # Use bcrypt_sha256 instead of plain bcrypt
# passwrd_context = CryptContext(
#     schemes=['bcrypt_sha256'],
#     deprecated="auto"
# )
# def generate_password_hash(password:str)->str:
#     hash_pwd = passwrd_context.hash(password)
#     return hash_pwd
# def password_verify(password:str,password_hash:str)->bool:
#     return  passwrd_context.verify(password,password_hash)
#
from datetime import timedelta , datetime

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import uuid
import logging


from ..config import Config

# Initialize the hasher once
# Default settings are high-security, but you can tune memory/time if needed
ph = PasswordHasher()
ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    """Hashes a password of any length."""
    return ph.hash(password)

def password_verify(password: str, password_hash: str) -> bool:
    """Verifies a password against an Argon2 hash."""
    try:
        return ph.verify(password_hash, password)
    except VerifyMismatchError:
        return False
def create_access_token(user_data:dict,expiry:timedelta = None , refresh:bool =False):
    payload = {'user': user_data,
               'jti': str(uuid.uuid4()),
               'exp': datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)),
               'refresh':refresh
               }

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return  token
def decode_token(token:str)->dict | None:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]

        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


