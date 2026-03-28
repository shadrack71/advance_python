import redis.asyncio as redis
from ..config import Config

JWT_EXPIRY = 3600

# Create the client (use from_url for easier config)
token_blacklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,
    decode_responses=True # This returns strings instead of bytes!
)

async def add_jwi_to_blocklist(jti: str) -> None:
    await token_blacklist.set(
        name=jti,
        value="true", # Value can't be empty for some Redis versions/configs
        ex=JWT_EXPIRY
    )

async def token_in_blocklist(jti: str) -> bool:
    # Use .get() to check if a key exists
    jti_token = await token_blacklist.get(jti)
    return jti_token is not None