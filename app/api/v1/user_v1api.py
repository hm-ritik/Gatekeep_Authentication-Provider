import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db
from app.core.exception import (
    TenantNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidCrentials
)
from app.schemas.user_schema import Create, UserResponse , LoginRequest
from app.services.user_services import UserServices

router = APIRouter()


@router.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: Create,session: AsyncSession = Depends(db.get_session),):
    service = UserServices(session)
    try:
        return await service.create_user(data)
    except TenantNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/user/getbyid", response_model=UserResponse)
async def get_user_by_id(id: uuid.UUID, session: AsyncSession = Depends(db.get_session),):
    service = UserServices(session)
    try:
        return await service.get_by_id(id)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/user/getbyemail", response_model=UserResponse)
async def get_user_by_email(tenant_id: uuid.UUID,email: str,session: AsyncSession = Depends(db.get_session)):
    service = UserServices(session)
    try:
        return await service.get_by_email(tenant_id, email)
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.post("/login")
async def login(data:LoginRequest , db:AsyncSession=Depends(db.get_session)):
    service=UserServices(db)
    try:
        return await service.login_user(data)
    except InvalidCrentials as exe:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Some error occured")
    

   