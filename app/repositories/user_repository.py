import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import LoginRequest
from app.models.user_model import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def create(self, user: User):
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, tenant_id: uuid.UUID, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.tenant_id == tenant_id, User.email == email))
        return result.scalar_one_or_none()

    async def login(self , hashed_password:str):
        result=await self.db.execute((select(User).where(User.hashed_password==hashed_password)))
        return result.scalar_one_or_none()
    



       


        






