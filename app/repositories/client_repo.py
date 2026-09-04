from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.client_model import Client

class ClientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, client: Client) -> Client:
        self.db.add(client)
        await self.db.commit()
        await self.db.refresh(client)
        return client

    async def get_by_client_id(self, client_id: str) -> Optional[Client]:
        result = await self.db.execute(
            select(Client).where(Client.client_id == client_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Optional[Client]:
        result = await self.db.execute(
            select(Client).where(Client.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all_active(self) -> List[Client]:
        result = await self.db.execute(
            select(Client).where(Client.is_active == True)
        )
        return result.scalars().all()

    async def update(self, client: Client) -> Client:
        await self.db.commit()
        await self.db.refresh(client)
        return client

    async def delete(self, client: Client) -> None:
        client.is_active = False
        await self.db.commit()