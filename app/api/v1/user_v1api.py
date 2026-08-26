from fastapi import APIRouter , Depends , Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db ,get_current_user
from app.schemas.user_schema import Register,RegisterResponse,Login
from app.services.user_services import registring_user , logging_in
from app.core.limiter import limiter
from app.models.user_model import User


router=APIRouter()

@router.post("/Register/", response_model=RegisterResponse)
@limiter.limit("10/minutes")
async def register_user(request:Request,post:Register,db:AsyncSession=Depends(get_db)):
    return await registring_user(post,db)

@router.post("/login/")
@limiter.limit("10/minutes")
async def login_user(request:Request,post:Login , db:AsyncSession=Depends(get_db)):
    return await logging_in(post ,db) 

@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
    }



