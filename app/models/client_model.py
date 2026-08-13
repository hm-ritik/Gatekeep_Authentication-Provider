import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    client_id: Mapped[str] = mapped_column(String(255),unique=True,index=True,nullable=False)
    client_secret_hash: Mapped[str] = mapped_column(String(255),nullable=False)
    client_name: Mapped[str] = mapped_column(String(255),nullable=False)
    redirect_uris: Mapped[list[str]] = mapped_column(ARRAY(String),nullable=False)
    allowed_scopes: Mapped[list[str]] = mapped_column(ARRAY(String),nullable=False,default=list)
    allowed_grant_types: Mapped[list[str]] = mapped_column(ARRAY(String),nullable=False,default=list)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)