from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.models.authorizationcode_model import AuthorizationCode
from sqlalchemy import select , update

class AuthorizationCodeRepo:
    def __init__(self, db:AsyncSession):
        self.db=db

    async def create(self , auth_code:AuthorizationCode):
        self.db.add(auth_code)
        self.db.flush()
        return auth_code


    async def get_by_code(self , code_hash:str):
        result=await self.db.execute(select(AuthorizationCode).where(AuthorizationCode.code_hash==code_hash))
        return result.scalar_one_or_none()
        

    async def mark_used(self, auth_code_id: uuid.UUID) -> bool:
        result = await self.db.execute(update(AuthorizationCode).where(
                AuthorizationCode.id == auth_code_id,
                AuthorizationCode.used.is_(False)).values(used=True))
        return result.rowcount == 1
