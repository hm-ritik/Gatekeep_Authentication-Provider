from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Tuple
from datetime import datetime
import uuid

from app.models.user import User
from app.models.client import Client
from app.models.token import RefreshToken, AuthorizationCode
from app.repositories import UserRepository, ClientRepository, TokenRepository
from app.core.security import (
    hash_password, verify_password, 
    create_access_token, create_refresh_token,
    verify_refresh_token, generate_token_hash
)
from app.schemas.auth import LoginResponse, TokenResponse

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.client_repo = ClientRepository(db)
        self.token_repo = TokenRepository(db)

    async def register(self, email: str, password: str, full_name: Optional[str] = None) -> User:
        """Register a new user"""
        # Check if user exists
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create user
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            email_verified=False,
            is_active=True
        )
        
        return await self.user_repo.create(user)

    async def login(self, email: str, password: str, client_id: str) -> LoginResponse:
        """Login user and return tokens"""
        # Get user
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        
        if not user.is_active:
            raise ValueError("Account is disabled")
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        # Get client
        client = await self.client_repo.get_by_client_id(client_id)
        if not client or not client.is_active:
            raise ValueError("Invalid client")
        
        # Update last login
        await self.user_repo.update_last_login(user)
        
        # Generate tokens
        return await self._generate_tokens(user, client)

    async def refresh_tokens(self, refresh_token: str, client_id: Optional[str] = None) -> TokenResponse:
        """Refresh access token using refresh token"""
        # Verify refresh token
        token_data = await verify_refresh_token(refresh_token, self.token_repo)
        if not token_data:
            raise ValueError("Invalid or expired refresh token")
        
        # Get user
        user = await self.user_repo.get_by_id(token_data["user_id"])
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        # Get client
        client = await self.client_repo.get_by_client_id(token_data["client_id"])
        if not client or not client.is_active:
            raise ValueError("Invalid client")
        
        # Get old refresh token
        old_token_hash = generate_token_hash(refresh_token)
        old_token = await self.token_repo.get_by_token_hash(old_token_hash)
        
        # Revoke old token (rotation)
        if old_token:
            await self.token_repo.revoke_token(old_token)
        
        # Generate new tokens
        return await self._generate_tokens(user, client, old_family_id=old_token.token_family_id if old_token else None)

    async def revoke_token(self, token: str, token_type_hint: Optional[str] = None) -> None:
        """Revoke a token"""
        if token_type_hint == "refresh_token" or not token_type_hint:
            # Try as refresh token
            token_hash = generate_token_hash(token)
            refresh_token = await self.token_repo.get_by_token_hash(token_hash)
            if refresh_token:
                await self.token_repo.revoke_token(refresh_token)
                return
        
        # If access token, we add to blacklist (handled in TokenService)
        # For now, just pass
        pass

    async def _generate_tokens(self, user: User, client: Client, old_family_id: Optional[str] = None) -> LoginResponse:
        """Generate access and refresh tokens"""
        # Get user roles
        roles = await self.user_repo.get_user_roles(user.id, client.client_id)
        
        # Create access token
        access_token = create_access_token(
            user_id=user.id,
            client_id=client.client_id,
            roles=roles,
            scopes=client.allowed_scopes
        )
        
        # Create refresh token
        refresh_token_str = create_refresh_token()
        token_hash = generate_token_hash(refresh_token_str)
        family_id = old_family_id or str(uuid.uuid4())
        
        refresh_token = RefreshToken(
            token_hash=token_hash,
            token_family_id=family_id,
            user_id=user.id,
            client_id=client.client_id,
            scopes=client.allowed_scopes,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        
        await self.token_repo.create_refresh_token(refresh_token)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token_str
        )