from random import random
from typing import Optional,NewType,TypedDict
from dataclasses import dataclass

name:str = 'shadrack'
last:str = 'kinsimba'
age:int = 30
height:float = 1.75

RGB = NewType('RGB',tuple[int,int,int])
HSL = NewType('HSL',tuple[int,int,int])

@dataclass
class User:
    name: str
    email:str
    color:RGB |HSL | None
    age:int | None = None
    height:float | None = None

class MyName(TypedDict):
    name: str
    email: str
    color:RGB |HSL | None
    age:int | None = None


# type User = dict[str, str | int | RGB | float | None]
# type RGB = tuple[int, int, int]

# T = TypeVar('T')
def random_number[T](lists:list[T])->T:
    return random.choice(lists)

def create_user(name: str,
                last:str,
                age: Optional[int],
                height: float,
                fav_color:RGB | None  = None) ->User:

    email = f'{name.lower()}.{last.lower()}@hadrastechsolutions.com'


    return User (
        name=name,
        email=email,
        age=age,
        color=fav_color,
        height=height
    )

user = create_user(name, last , age, height)
user2 = create_user(name, last, age, height,fav_color=RGB((105,111,221)))


print(user2)

