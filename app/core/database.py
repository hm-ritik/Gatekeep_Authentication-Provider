from sqlalchemy.ext.asyncio import create_async_engine , async_sessionmaker , AsyncSession
from sqlalchemy.orm import  DeclarativeBase
from app.core.config import settings


async_engine=create_async_engine(settings.DATABASE_URL ,  connect_args={"statement_cache_size": 0}, echo=True ,pool_size=5 ,   max_overflow=10,  pool_pre_ping=True,  pool_recycle=300)
#,pool_size=5 ,   max_overflow=10,  pool_pre_ping=True,  pool_recycle=300

asyncsessionlocal=async_sessionmaker(async_engine , class_=AsyncSession , expire_on_commit=False)

class Base(DeclarativeBase):
    pass

 


