from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.tenant_schema import TenantCreate
import uuid
from app.models.tenant_model import Tenant
from sqlalchemy import select


class TenantRepository:
    def __init__(self , db:AsyncSession):
        self.db=db

    async def create(self , tenant:TenantCreate):    
        self.db.add(tenant)
        await self.db.flush()
        return tenant
    async def get_by_id(self , tenant_id:uuid.UUID):
        result= await self.db.execute(select(Tenant).where(Tenant.id==tenant_id))
        return result.scalar_one_or_none()
    async def get_by_slug(self , slug:str):
         result= await self.db.execute(select(Tenant).where(Tenant.slug==slug))
         return result.scalar_one_or_none()

