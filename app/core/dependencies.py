from app.core.database import asyncsessionlocal
from jose import jwt
from app.core.config import settings
from datetime import timedelta ,datetime

async def get_db():
    async with asyncsessionlocal() as session:
      try:
        yield session
      finally:
        await session.close()  

async def create_access_token(data:dict):
   to_encode=data.copy()
   to_expire=datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({"expiry_time":to_expire})
   token=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
   return{
      "jwt":token ,
      "token_type": "bearer"
   }

async def get_current_user():
   pass

