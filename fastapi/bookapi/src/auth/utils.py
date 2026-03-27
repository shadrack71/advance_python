from passlib.context import CryptContext

passwrd_context = CryptContext(
    schemes=['bcrypt']
)

def generate_password_hash(password:str)->str:
    hash_pwd = passwrd_context.hash(password)
    return hash_pwd
def password_verify(password:str,password_hash:str)->bool:
    return  passwrd_context.verify(password,password_hash)