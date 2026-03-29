from typing import Optional
from pydantic import ConfigDict
from sqlalchemy import func
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, timezone
from ..books import models


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
    books: Optional[list["models.Book"]] = Relationship(back_populates="user_accounts",sa_relationship_kwargs={"lazy":"selectin","uselist": True})

    def __repr__(self) -> str:
        return f"<User {self.username}>"