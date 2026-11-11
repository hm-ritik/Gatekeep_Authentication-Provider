from pydantic import BaseModel , field_validator , Field , ConfigDict
import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime

class CreateClient(BaseModel):
    tenant_id: uuid.UUID
    name: str = Field(min_length=1, max_length=100)
    redirect_uris: list[str] = Field(min_length=1)
    is_confidential: bool = True


class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    tenant_id: uuid.UUID
    client_id: str
    name: str
    redirect_uris: list[str]
    is_confidential: bool
    is_active: bool
    created_at: datetime


class ClientCreatedResponse(ClientResponse):
    client_secret: str | None = None