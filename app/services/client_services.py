from app.repositories.client_repository import ClientRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.client_schema import CreateClient
from app.models.client_model import Client
from fastapi import HTTPException
import uuid
from app.repositories.tenant_repository import TenantRepository
from app.utils.client_utils import helper
from app.core.exception import TenantNotFoundError

"""Update create_client in the service:
Generate the client_id on the server.
If the client is confidential, generate a secret, store only its hash, and return the plain secret once.
Public clients get no secret."""

from dataclasses import dataclass

from app.models.client_model import Client


@dataclass(frozen=True)
class CreatedClient:
    client: Client
    client_secret: str | None


class ClientServices:
    def __init__(self , db:AsyncSession):
        self.db=db
        self.client=ClientRepository(db)
        self.tenants=TenantRepository(db)

    async def create_client(self, data: CreateClient) -> tuple[Client, str | None]:
        tenant = await self.tenants.get_by_id(data.tenant_id)
        if tenant is None or not tenant.is_active:
            raise TenantNotFoundError(str(data.tenant_id))

        secret: str | None = None
        hashed_secret: str | None = None
        if data.is_confidential:
            secret = helper.generate_client_secret()
            hashed_secret = helper.hash_token(secret)

        client = Client(
            tenant_id=data.tenant_id,
            client_id=helper.generate_clientid(),
            client_secret_hash=hashed_secret,
            name=data.name,
            redirect_uris=data.redirect_uris,
            is_confidential=data.is_confidential,
        )
        await self.client.create(client)
        await self.db.commit()
        return CreatedClient(client=client, client_secret=secret)

    
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






                       
            
                      
            




    


       