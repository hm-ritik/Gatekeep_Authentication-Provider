from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime
from app.models.token_model import Token, RefreshToken, AuthorizationCode

class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

   
    async def create_blacklisted_token(self, token: Token) -> Token:
        """Add access token to blacklist"""
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token

    async def get_blacklisted_token(self, jti: str) -> Optional[Token]:
        """Get blacklisted token by JTI"""
        result = await self.db.execute(
            select(Token).where(Token.jti == jti)
        )
        return result.scalar_one_or_none()

 
    async def create_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        """Create a new refresh token"""
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token

    async def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Get refresh token by hash"""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    async def get_by_family_id(self, token_family_id: str) -> List[RefreshToken]:
        """Get all tokens in a family"""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_family_id == token_family_id)
        )
        return result.scalars().all()

    async def revoke_token(self, refresh_token: RefreshToken) -> None:
        """Revoke a single refresh token"""
        refresh_token.is_revoked = True
        await self.db.commit()

    async def revoke_family(self, refresh_tokens: List[RefreshToken]) -> None:
        """Revoke entire token family"""
        for token in refresh_tokens:
            token.is_revoked = True
        await self.db.commit()

    async def delete_expired_tokens(self) -> int:
        """Delete expired refresh tokens"""
        result = await self.db.execute(
            delete(RefreshToken).where(RefreshToken.expires_at < datetime.utcnow())
        )
        await self.db.commit()
        return result.rowcount

   
    async def create_authorization_code(self, auth_code: AuthorizationCode) -> AuthorizationCode:
        """Create authorization code"""
        self.db.add(auth_code)
        await self.db.commit()
        await self.db.refresh(auth_code)
        return auth_code

    async def get_authorization_code(self, code: str) -> Optional[AuthorizationCode]:
        """Get authorization code by code string"""
        result = await self.db.execute(
            select(AuthorizationCode).where(AuthorizationCode.code == code)
        )
        return result.scalar_one_or_none()

    async def mark_code_as_used(self, auth_code: AuthorizationCode) -> None:
        """Mark authorization code as used"""
        auth_code.is_used = True
        await self.db.commit()