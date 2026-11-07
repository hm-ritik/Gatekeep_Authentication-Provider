import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import (
    TenantNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import password_hasher
from app.models.user_model import User
from app.repositories.tenant_repository import TenantRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import Create


class UserServices:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)
        self.tenants = TenantRepository(db)

    async def create_user(self, data: Create):
        tenant = await self.tenants.get_by_id(data.tenant_id)
        if tenant is None or not tenant.is_active:
            raise TenantNotFoundError(str(data.tenant_id))

        email = data.email.strip().lower()
        if await self.users.get_by_email(data.tenant_id, email):
            raise UserAlreadyExistsError(email)

        user = User(
            tenant_id=data.tenant_id,
            email=email,
            hashed_password=password_hasher.hash_password(data.password),
        )
        try:
            await self.users.create(user)
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise UserAlreadyExistsError(email)
        return user

    async def get_by_id(self, user_id: uuid.UUID):
        user = await self.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(str(user_id))
        return user

    async def get_by_email(self, tenant_id: uuid.UUID, email: str):
        user = await self.users.get_by_email(tenant_id, email.strip().lower())
        if user is None:
            raise UserNotFoundError(email)
        return user