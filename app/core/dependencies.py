from app.core.database import asyncsessionlocal
from jose import jwt , JWTError
from app.core.config import settings
from datetime import timedelta ,datetime
from app.core.security import PRIVATE_KEY , PUBLIC_KEY


async def get_db():
    async with asyncsessionlocal() as session:
      try:
        yield session
      finally:
        await session.close()  

async def create_access_token(subject:str ,client_id:str,scope:str=""):
   now=datetime.utcnow()
   payload={
      "sub":subject,
      "iss":settings.APP_NAME,
      "aud":client_id,
      "iat":now ,
      "exp":now+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
      "token_type": "access"
   }


  
   token=jwt.encode(payload,PRIVATE_KEY,algorithm=settings.JWT_ALGORITHM)
   return{
      "jwt":token ,
      "token_type": "bearer"
   }

async def decode_access_token(token:str):
   try:
       payload=jwt.decode(token,PUBLIC_KEY ,algorithms=[settings.JWT_ALGORITHM],issuer=settings.APP_NAME)
       return payload
   except JWTError:
      return None

async def get_current_user():
    pass   

