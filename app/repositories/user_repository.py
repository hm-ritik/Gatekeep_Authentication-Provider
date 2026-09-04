from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.user_model import User
from app.models.role_model import UserRole, Role

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_last_login(self, user: User) -> None:
        user.last_login = func.now()
        await self.db.commit()

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()

    async def get_user_roles(self, user_id: int, client_id: Optional[str] = None) -> List[str]:
        query = select(Role.name).join(UserRole).where(UserRole.user_id == user_id)
        if client_id:
            query = query.where(UserRole.client_id == client_id)
        
        result = await self.db.execute(query)
        return [row[0] for row in result.all()]
