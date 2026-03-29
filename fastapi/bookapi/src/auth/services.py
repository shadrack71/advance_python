from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreateModel
from sqlmodel import select, desc
from .models import  User
from .utils import generate_password_hash,password_verify


class UserService:
    async  def get_user_email(self,email:str,session:AsyncSession):
        statement = select(User).where(User.email == email)
        result = await  session.exec(statement)
        user = result.first()
        return user

    async def user_exist(self,email:str,session:AsyncSession):
        user = await self.get_user_email(email,session)
        return True if user is not None else False


    async def create_user(self,user_data:UserCreateModel,session:AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict
        )
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        new_user.role = "user"

        session.add(new_user)
        await session.commit()
        return new_user