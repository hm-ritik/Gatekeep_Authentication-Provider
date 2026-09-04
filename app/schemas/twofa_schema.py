from pydantic import BaseModel, Field
from typing import Optional, List


class TOTPEnrollResponse(BaseModel):
    secret: str
    qr_code: str  
    backup_codes: List[str]

class TOTPVerifyRequest(BaseModel):
    totp_code: str = Field(..., min_length=6, max_length=6)
    secret: Optional[str] = None

class TOTPVerifyResponse(BaseModel):
    success: bool
    message: str

class TOTPLoginRequest(BaseModel):
    mfa_token: str
    totp_code: str = Field(..., min_length=6, max_length=6)

class TOTPBackupLoginRequest(BaseModel):
    mfa_token: str
    backup_code: str = Field(..., min_length=8, max_length=8)


class TOTPDisableRequest(BaseModel):
    password: str


class TOTPStatusResponse(BaseModel):
    enabled: bool
    backup_codes_remaining: Optional[int] = None