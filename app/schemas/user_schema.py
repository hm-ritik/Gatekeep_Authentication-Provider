from pydantic import BaseModel , Field , EmailStr , ConfigDict
import uuid
from datetime import datetime


class Create(BaseModel):
      model_config=ConfigDict(str_strip_whitespace=True)
      tenant_id:uuid.UUID
      email:EmailStr
      hashed_password:str

class UserResponse(BaseModel):
     id:uuid.UUID
     tenant_id:uuid.UUID
     email:EmailStr
     is_active:bool
     created_at:datetime



            

