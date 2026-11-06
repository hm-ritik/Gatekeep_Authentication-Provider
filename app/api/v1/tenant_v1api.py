from fastapi import APIRouter , Depends  , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.core.exception import TenantAlreadyExistsError
from app.schemas.tenant_schema import TenantCreate , TenantResponse


router=APIRouter()

@router.post("/tenantregister", response_model=TenantResponse)
async def create_tenant(tenant:TenantCreate ,  db:AsyncSession=Depends(db)):
    pass