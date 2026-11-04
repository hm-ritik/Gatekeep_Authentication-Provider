from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import  DeclarativeBase
from app.core.config import settings


class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self , url:str):
        self.engine=create_async_engine(url , pool_pre_ping=True)
        self._sessionmaker=async_sessionmaker(bind=self.engine , expire_on_commit=False,autoflush=False)

    async def get_session(self):
        async with self._sessionmaker() as session:
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()

db=Database(settings.DATABASE_URL)                


 


