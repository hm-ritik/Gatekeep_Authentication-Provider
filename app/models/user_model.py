from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey , DateTime , UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from sqlalchemy.orm import Mapped , mapped_column

class User(Base):
    __tablename__ = "users"
    __table_args__=(UniqueConstraint("tenant_id" , "email" , name="uq_users_tenant_email"),)

    id:Mapped[uuid.UUID]=mapped_column(UUID , primary_key=True , default=uuid.uuid4)
    tenant_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("tenants.id" ,ondelete="CASCADE"))
    email:Mapped[str]=mapped_column(String(256))
    hashed_password:Mapped[str]=mapped_column(String(256))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column( 
     DateTime(timezone=True), default=datetime.utcnow())
    updated_at: Mapped[datetime] = mapped_column( DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

   