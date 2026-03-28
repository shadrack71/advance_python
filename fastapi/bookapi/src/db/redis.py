from ..config import Config
import  aioredis

JWT_EXPIRY = 3600
token_blacklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0
)

async  def add_jwi_to_blocklist(jti:str)->None:
    await  token_blacklist.set(
        name=jti,
        value="",
        ex=JWT_EXPIRY
    )
async  def token_in_blocklist(jti:str)->bool:
    jti_token = await token_blacklist.set(jti)
    return jti_token is not None
