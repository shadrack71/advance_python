from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from ..config import Config


engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
    connect_args={"ssl": True}
)


async def initdb():
    """Test database connection"""

    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT 'Hello World'"))

        print(result.scalar())  # prints: Hello World