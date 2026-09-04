from pydantic import BaseModel, Field
from typing import Optional

# ============ AUTHORIZATION ============
class AuthorizeRequest(BaseModel):
    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: Optional[str] = None
    state: Optional[str] = None
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = "S256"

class AuthorizeResponse(BaseModel):
    code: str
    state: Optional[str] = None

# ============ TOKEN EXCHANGE ============
class TokenRequest(BaseModel):
    grant_type: str 
    client_id: str
    client_secret: Optional[str] = None
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    code_verifier: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

class TokenExchangeResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None