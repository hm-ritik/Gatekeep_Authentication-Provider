from fastapi import APIRouter , Depends , Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.schemas.user_schema import Register,RegisterResponse,Login
from app.services.user_services import registring_user , logging_in
from app.core.limiter import limiter


router=APIRouter()

@router.post("/Register/", response_model=RegisterResponse)
@limiter.limit("10/minutes")
async def register_user(request:Request,post:Register,db:AsyncSession=Depends(get_db)):
    return await registring_user(post,db)

@router.post("/login/")
@limiter.limit("3/minutes")
async def login_user(request:Request,post:Login , db:AsyncSession=Depends(get_db)):
    return await logging_in(post ,db) 



