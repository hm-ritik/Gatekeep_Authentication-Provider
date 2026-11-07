from pydantic import BaseModel , field_validator , Field , ConfigDict
import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime


class CreateClient(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    tenant_id:uuid.UUID
    client_id:str
    name:str=Field(min_length=4 , max_length=100)
    redirect_uris:list[str]

class ClientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:uuid.UUID
    tenant_id:uuid.UUID
    client_id:str
    name:str
    redirect_uris:list[str]
    is_confidential:bool
    is_active:bool
    updated_at:datetime
    
      





       
