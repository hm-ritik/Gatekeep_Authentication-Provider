from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schema import Register , RegisterResponse
from sqlalchemy import select
from app.models.user_model import User



async def register(db:AsyncSession , post:Register):
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

async def check_email(db:AsyncSession , email:str):
    email= await db.execute(select(User).where(User.email==email))
    return email.scalar_one_or_none()



