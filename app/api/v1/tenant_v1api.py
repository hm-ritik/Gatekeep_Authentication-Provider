from fastapi import APIRouter , Depends  , HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.core.exception import TenantAlreadyExistsError , TenantNotFoundError
from app.schemas.tenant_schema import TenantCreate , TenantResponse
from app.services.tenant_services import TenantService
from app.core.database import db
import uuid


router=APIRouter()






@router.post("/tenants", response_model=TenantResponse, status_code=201)
async def create_tenant(data: TenantCreate, session: AsyncSession = Depends(db.get_session),):
    service=TenantService(session)
    try:
        return await service.create_tenant(data)
    except TenantAlreadyExistsError as exe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exe))

@router.get("/gettenant" , response_model=TenantResponse)
async def gettenant_by_id(tenant_id:uuid.UUID , session:AsyncSession=Depends(db.get_session),):
    service=TenantService(session)
    try:
         return await service.get_by_id(tenant_id)
    except TenantNotFoundError as exe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=str(exe))

@router.get("/gettenantbyslug" ,response_model=TenantResponse)
async def gettenant_byslug(slug:str , session:AsyncSession=Depends(db.get_session),):
    service=TenantService(session)
    try:
        return await service.get_byslug(slug)
    except TenantNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=str(TenantNotFoundError))


   
    