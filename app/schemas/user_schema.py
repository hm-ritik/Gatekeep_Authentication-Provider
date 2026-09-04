from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    email_verified: bool
    twofa_enabled: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserInfoResponse(BaseModel):
    sub: str 
    email: str
    email_verified: bool
    name: Optional[str] = None
    roles: List[str] = []
    permissions: List[str] = []

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class ChangeEmailRequest(BaseModel):
    new_email: EmailStr
    password: str  

