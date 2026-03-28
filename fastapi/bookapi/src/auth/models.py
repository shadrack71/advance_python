from sqlalchemy import func
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime, timezone


class User(SQLModel, table=True):
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
    is_verified: bool = Field(default=False)
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP),
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"