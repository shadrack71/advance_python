from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from ..books.models import  Book
from  sqlmodel.ext.asyncio.session import AsyncSession
from  sqlalchemy.orm import  sessionmaker

from ..config import Config


engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    connect_args={"ssl": True}
)


async def initdb():
    """Test database connection"""

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()->AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False

    )
    async with Session() as session:
        yield session
