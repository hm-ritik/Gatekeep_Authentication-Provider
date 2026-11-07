from app.repositories.client_repository import ClientRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.client_schema import CreateClient
from app.models.client_model import Client
from fastapi import HTTPException
import uuid
from app.repositories.tenant_repository import TenantRepository





class ClientServices:
    def __init__(self , db:AsyncSession):
        self.db=db
        self.client=ClientRepository(db)
        self.tenet=TenantRepository(db)

    async def create_client(self,data:CreateClient):
        result=await self.client.get_by_clientid(data.client_id)
        ten=await self.tenet.get_by_id(data.tenant_id)
        if result is None and ten is not None:
            cli=Client(tenant_id=data.tenant_id , client_id=data.client_id , name=data.name , redirect_uris=data.redirect_uris)
            await self.client.create(cli)
            await self.db.commit()
            return cli

        raise HTTPException(status_code=404 , detail="Some Error Occured")

    async def get_by_id(self , id:uuid.UUID):
         result=await self.client.get_by_id(id)
         if result is None:
             raise HTTPException(status_code=404 , detail="Some Error Occured")
         return result

    async def get_by_clientid(self , client_id:str):
                 result=await self.client.get_by_clientid(client_id)
                 if result is None:
                     raise HTTPException(status_code=404 , detail="Some Error Occured")
                 return result






                       
            
                      
            




    


       