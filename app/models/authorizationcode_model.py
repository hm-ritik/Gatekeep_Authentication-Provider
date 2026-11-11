"""Create an AuthorizationCode model with these columns: code (stored hashed, or unique and random), client_id, user_id, tenant_id, redirect_uri, code_challenge, code_challenge_method, expires_at, used flag.
Generate an Alembic migration, read it, then apply it.
Write its repository (create, get by code, mark used)."""
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime , timezone
from sqlalchemy.dialects.postgresql import UUID
def utcnow() -> datetime:
    return datetime.now(timezone.utc)

class AuthorizationCode(Base):
    __tablename__ = "authorization_codes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    code_hash: Mapped[str] = mapped_column(String(64),unique=True,nullable=False,index=True)
    client_id: Mapped[uuid.UUID] = mapped_column( UUID(as_uuid=True) ,ForeignKey("clients.id" , ondelete="CASCADE"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id" , ondelete="CASCADE"),nullable=False )
    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True) ,ForeignKey("tenants.id" , ondelete="CASCADE"),nullable=False )
    redirect_uri: Mapped[str] = mapped_column(String(2048), nullable=False)
    code_challenge: Mapped[str] = mapped_column( String(43), nullable=False)
    code_challenge_method: Mapped[str] = mapped_column(String(10),nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False)
    used: Mapped[bool] = mapped_column(Boolean,default=False,nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow ,nullable=False)



