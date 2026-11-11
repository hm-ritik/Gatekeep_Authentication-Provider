from fastapi import APIRouter , HTTPException , status,Depends
from app.schemas.client_schema  import CreateClient , ClientResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.core.exception import ClientAlreadyExistsError
from app.services.client_services import ClientServices
import uuid
from app.core.exception import TenantNotFoundError 
from app.schemas.client_schema import ClientCreatedResponse





router=APIRouter()

@router.post("/client", response_model=ClientCreatedResponse, status_code=201)
async def create_client(data: CreateClient, session: AsyncSession = Depends(db.get_session)):
    service = ClientServices(session)
    try:
         created = await service.create_client(data)
    except TenantNotFoundError as exc:
         raise HTTPException(status_code=404, detail=str(exc))

    response = ClientCreatedResponse.model_validate(created.client)
    response.client_secret = created.client_secret
    return response

@router.get("/getbyid" , response_model=ClientResponse , status_code=200)
async def get_by_id(id:uuid.UUID , session:AsyncSession=Depends(db.get_session)):
        client=ClientServices(session)
        try:
            return await client.get_by_id(id)
        except ClientAlreadyExistsError as exe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=str(exe))

@router.get("/getbyclientid" , response_model=ClientResponse , status_code=200)
async def get_by_client_id(client_id:str, session:AsyncSession=Depends(db.get_session)):
        client=ClientServices(session)
        try:
            return await client.get_by_clientid(client_id)
        except ClientAlreadyExistsError as exe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=str(exe))

        
    

    







