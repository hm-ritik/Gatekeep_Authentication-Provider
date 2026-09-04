from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text , ARRAY
from sqlalchemy.orm import relationship
from app.core.database import Base

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(100), unique=True, index=True, nullable=False)  # JWT ID
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    client_id = Column(String(100), nullable=False)
    revoked_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    user = relationship("User")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String(255), unique=True, index=True, nullable=False)
    token_family_id = Column(String(100), index=True, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    client_id = Column(String(100), nullable=False)
    
 
    scopes = Column(ARRAY(String), default=[])
    
    is_revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
   
    user = relationship("User", back_populates="refresh_tokens")

class AuthorizationCode(Base):
    __tablename__ = "authorization_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, index=True, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    client_id = Column(String(100), ForeignKey("clients.client_id", ondelete="CASCADE"), nullable=False)
    
    redirect_uri = Column(String(500), nullable=False)
    scope = Column(String(500))
    
   
    code_challenge = Column(String(100))
    code_challenge_method = Column(String(10))  # S256 or plain
    
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
   
    user = relationship("User")
    client = relationship("Client", back_populates="authorization_codes")