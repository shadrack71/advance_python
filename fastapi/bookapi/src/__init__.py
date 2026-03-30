from fastapi import FastAPI

from .books.routes import book_router
from .auth.routes import auth_router
from .reviews.routes import review_router

from .db.main import initdb

from contextlib import asynccontextmanager

from .errors import (InvalidToken ,RevokedToken,AccessTokenRequired,
                     RefreshTokenRequired,
                      UserAlreadyExists,InvalidCredentials,InsufficientPermission,
                      BookNotFound,TagNotFound,TagAlreadyExists,UserNotFound,
                     create_exception_handler,register_error_handlers
                     )

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting")
    await initdb()

    yield

    print(f"server is stoping")

version = 'v1'
app = FastAPI(
    title='bookly',
    description='A RESTful API for a book review web service',
    version=version
    # lifespan=life_span
)
register_error_handlers(app)

app.include_router(book_router,prefix=f"/api/{version}/books",tags=['books'])
app.include_router(auth_router,prefix=f"/api/{version}/auth",tags=['auth'])
app.include_router(review_router,prefix=f"/api/{version}/reviews",tags=['review'])