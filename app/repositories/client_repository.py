from app.schemas.client_schema import ClientResponse,CreateClient
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models.client_model import Client
from sqlalchemy import select
import uuid



class  ClientRepository:
    def __init__(self , session:AsyncSession):
        self.db=session

    async def create(self ,client:CreateClient):
        self.db.add(client)
        await self.db.flush()
        return client

    async def get_by_id(self , data_id:uuid.UUID):
            result=await self.db.execute(select(Client).where(data_id==Client.id))    
            return result.scalar_one_or_none()

    async def get_by_clientid(self , client_id:str):
        result=await self.db.execute(select(Client).where(client_id==Client.client_id))    
        return result.scalar_one_or_none()
    
