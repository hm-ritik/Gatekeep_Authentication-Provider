from app.core.database import asyncsessionlocal

async def get_db():
    async with asyncsessionlocal() as session:
      try:
        yield session
      finally:
        await session.close()  