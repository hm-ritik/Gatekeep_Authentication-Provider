from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.user_schema import Register,RegisterResponse,Login
from app.services.user_services import registring_user , logging_in


router=APIRouter()

@router.post("/Register/", response_model=RegisterResponse)
async def register_user(post:Register,db:AsyncSession=Depends(get_db)):
    return registring_user(post,db)

@router.post("/login/")
async def login_user(post:Login , db:AsyncSession=Depends(get_db)):
    return logging_in(post ,db) 



