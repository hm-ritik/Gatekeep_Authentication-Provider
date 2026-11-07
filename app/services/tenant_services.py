from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.core.exception import TenantAlreadyExistsError
from app.models import Tenant
from app.repositories.tenant_repository import TenantRepository
from app.schemas.tenant_schema import TenantCreate
from fastapi import HTTPException


class TenantService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.tenants = TenantRepository(session)
    async def create_tenant(self, data: TenantCreate):
        slug = data.slug.strip().lower()
        if await self.tenants.get_by_slug(slug):
            raise TenantAlreadyExistsError(slug)

        tenant = Tenant(name=data.name.strip(), slug=slug)
        await self.tenants.create(tenant)
        await self.session.commit()
        return tenant

    async def get_by_id(self , tenant_id:uuid.UUID):
        result=await self.tenants.get_by_id(tenant_id)
        if result is None:
            raise HTTPException(status_code=404 , detail="some error occured")
        return result

    async def get_byslug(self , data:str):
        result=await self.tenants.get_by_slug(data)
        if result is None:
            raise HTTPException(status_code=404 , detail="some error occured")
        return result

    

