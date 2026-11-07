from fastapi import APIRouter , HTTPException , status,Depends
from app.schemas.client_schema  import CreateClient , ClientResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import db
from app.core.exception import ClientAlreadyExistsError
from app.services.client_services import ClientServices
import uuid






router=APIRouter()

@router.post("/client" , response_model=ClientResponse, status_code=201)
async def create_client(data:CreateClient , session:AsyncSession=Depends(db.get_session)):
    client=ClientServices(session)
    try:
       return await client.create_client(data)
    except ClientAlreadyExistsError as exe:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail=str(exe))


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

        
    

    







