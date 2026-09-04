from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PermissionAssign(BaseModel):
    user_id: int
    role_id: int
    client_id: str

class PermissionCheck(BaseModel):
    user_id: int
    permission: str  
    client_id: Optional[str] = None

class PermissionCheckResponse(BaseModel):
    has_permission: bool
    reason: Optional[str] = None


class UserRoleResponse(BaseModel):
    user_id: int
    role_id: int
    role_name: str
    client_id: str
    granted_at: datetime
    
    class Config:
        from_attributes = True