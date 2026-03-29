from typing import Optional
from pydantic import ConfigDict
from sqlalchemy import func
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, timezone


class User(SQLModel, table=True):
    model_config = ConfigDict(from_attributes=True)

    __tablename__ = "user_accounts"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )
    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    role:str = Field(
        sa_column=Column(pg.VARCHAR,nullable=False , server_default="user")
    )
    is_verified: bool = Field(default=False)
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP),
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )
    books: Optional[list["Book"]] = Relationship(back_populates="user_accounts",sa_relationship_kwargs={"lazy":"selectin","uselist": True})
    reviews: Optional[list["Review"]] = Relationship(back_populates="user_accounts",
                                                 sa_relationship_kwargs={"lazy": "selectin", "uselist": True})

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Book(SQLModel , table=True):
    __tablename__ = "books"

    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language:str
    user_uid:Optional[uuid.UUID] = Field(default=None,foreign_key="user_accounts.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user_accounts:Optional["User"] = Relationship(back_populates="books")
    reviews: Optional[list["Review"]] = Relationship(back_populates="books",
                                                     sa_relationship_kwargs={"lazy": "selectin", "uselist": True})

    def __repr__(self) -> str:
        return f"<Book {self.title}>"

class Review(SQLModel , table=True):
    __tablename__ = "reviews"

    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    rating: int = Field(lt=5)
    review_text:str
    user_uid:Optional[uuid.UUID] = Field(default=None,foreign_key="user_accounts.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user_accounts:Optional["User"] = Relationship(back_populates="reviews")
    books: Optional["Book"] = Relationship(back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review  for book {self.book_uid} by User {self.user_uid}>"