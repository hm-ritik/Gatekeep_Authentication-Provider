from app.core.security import hash_password , verify_password
from app.schemas.user_schema import Register , Login
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import register , check_email
from fastapi import HTTPException
from app.models.user_model import User
from app.core.dependencies import create_access_token




async def  registring_user(post:Register , db:AsyncSession):
    mail=await check_email(db,post.email)
    if mail:
        raise HTTPException(status_code=409 , detail="Email Already Exists ")
    secure_password=hash_password(post.password)
    user=User(
        email=post.email,
        hashed_password=secure_password

    )
    result=await register(db,user)
    return result

async def logging_in(post: Login, db: AsyncSession):
    existing = await check_email(db, post.email)

    if not existing:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    if not verify_password(post.password, existing.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    if not existing.is_active:
        raise HTTPException(status_code=403,detail="User is inactive")
    token = await create_access_token(
        subject=str(existing.id),
        client_id="test-client",
        scope=""
    )
    return token
   
        




