from sqlalchemy.ext.asyncio import AsyncSession
from app.models.refresh_tmodel import RefreshToken




async def create_refresh_token(db:AsyncSession , post:RefreshToken):
    db.add(post)
    await db.commit()
    db.refresh(post)
    return post