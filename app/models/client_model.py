from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String(100), unique=True, index=True, nullable=False)
    client_secret_hash = Column(String(255), nullable=False)
    client_name = Column(String(100), nullable=False)
    client_type = Column(String(20), default="confidential") 
    
    redirect_uris = Column(ARRAY(String), default=[])
    allowed_scopes = Column(ARRAY(String), default=["openid", "email", "profile"])
    allowed_grant_types = Column(ARRAY(String), default=["authorization_code", "refresh_token"])
    
    is_active = Column(Boolean, default=True)
    require_pkce = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    authorization_codes = relationship("AuthorizationCode", back_populates="client")
    user_roles = relationship("UserRole", back_populates="client")

    def __repr__(self):
        return f"<Client {self.client_id}>"