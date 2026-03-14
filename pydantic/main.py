from functools import partial
from uuid import uuid4, UUID

from pydantic import BaseModel, ValidationError, Field, SecretStr, field_validator, model_validator, ValidationInfo, \
    EmailStr
from datetime import datetime , UTC
from typing import Optional, NewType, TypedDict, Literal,Annotated



class User(BaseModel):
    uid:UUID =Field(default_factory=uuid4)
    # uid:Annotated[int,Field(default_factory=uuid4)]
    username:Annotated[str,Field(min_length=3 , max_length=20)]
    name :str
    age : Annotated[int,Field(ge =13)]
    password : SecretStr
    bio:str = ""
    verified_at:datetime | None = None
    is_active:bool = True
    firstName:Optional[str] = None
    full_name:str | None = None


    ### Username Validation
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v.lower()


### Model Validator
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def passwords_match(self) -> 'UserRegistration':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self


try:
    registration = UserRegistration(
        email="CoreyMSchafer@gmail.com",
        password="secret123",
        confirm_password="secret123"
    )
except ValidationError as e:
    print(e)

class Blog (BaseModel):
    title:Annotated[str,Field(min_length=3 , max_length=200)]
    content:Annotated[str,Field(min_length=3 )]
    view_count:int = 0
    is_published:bool = False
    tags:list[str] = Field(default_factory=list)
    created_at :datetime = Field(default_factory=partial(datetime.now,tz=UTC))
    author_id:str | int
    status:Literal["draft","published","archived"]
    # slug:Annotated[str,Field(pattern=r"^[a-z0-9-]+$")]


post = Blog(
    title="blog1",
    content="name",
    author_id="122",
    tags= ['atta'],
    status = "draft"
    # slug = "name099 "

)
print(post.model_dump_json(indent=2))


user1 = User(

        username='Shadrack_kin66',
        name='user1',
        age=16,
        password='password',
    )



# user1.bio = "Python dev"
print(user1.validate_username(user1.username))
print(user1.model_dump_json(indent=2))