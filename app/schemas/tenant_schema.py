
from pydantic import BaseModel , Field , field_validator , ConfigDict
import re
import uuid
from datetime import datetime

class TenantCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=3, max_length=50)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value:str):
        value = value.lower()
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
            raise ValueError(
                "slug may contain only lowercase letters, digits and single hyphens"
            )
        return value
         
class TenantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    slug: str
    is_active: bool
    created_at: datetime
