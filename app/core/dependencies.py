from jose import jwt , JWTError
from app.core.config import settings
from datetime import timedelta ,datetime
from app.core.security import PRIVATE_KEY , PUBLIC_KEY
import uuid
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


oauth_scheme=OAuth2PasswordBearer(tokenUrl="/token")

class TokenManager:
    def __init__(self):
        pass

    async def create_access_token(self, subject: str, client_id: str, scope: str = ""):
        self.now = datetime.utcnow()
        payload = {
            "sub": subject,
            "iss": settings.APP_NAME,
            "aud": client_id,
            "scope": scope,
            "iat": self.now,
            "exp": self.now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "jti": str(uuid.uuid4()),
            "token_type": "access",
        }

        token = jwt.encode(payload, PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)
        return {
            "jwt": token,
            "token_type": "bearer",
        }

    async def decode_access_token(self, token: str):
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM], issuer=settings.APP_NAME)
            return payload
        except JWTError as e:
            print(e)
            return None




        
     
    
      

