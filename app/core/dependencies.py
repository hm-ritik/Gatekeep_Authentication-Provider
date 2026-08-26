from app.core.database import asyncsessionlocal
from jose import jwt , JWTError
from app.core.config import settings
from datetime import timedelta ,datetime
from app.core.security import PRIVATE_KEY , PUBLIC_KEY
import uuid
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import get_user_by_id

oauth_scheme=OAuth2PasswordBearer(tokenUrl="/token")

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
      "scope":scope,
      "iat":now ,
      "exp":now+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "jti": str(uuid.uuid4()),
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
   except JWTError as e:
      print(e)
      return None

async def get_current_user(token:str=Depends(oauth_scheme) , db:AsyncSession=Depends(get_db)):
     payload=await decode_access_token(token)
     if not payload:
        raise HTTPException(status_code=400 , detail="Authentication Failed")
     current_id=payload.get("sub")
     if not current_id:
         raise HTTPException(status_code=400 , detail="Authentication Failed")
     user=await get_user_by_id(db,current_id)
     if not user:
         raise HTTPException(status_code=400 , detail="Authentication Failed")
     return user
        
     
    
      

