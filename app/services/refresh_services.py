from sqlalchemy.ext.asyncio import AsyncSession
from app.models.token_model import RefreshToken
from datetime import datetime ,timedelta , timezone
import uuid
from app.repositories.refresh_repository import create_refresh_token


from app.utils.token_utils import generate_refresh_token , hash_token

REFRESH_TOKEN_TTL_DAYS=15
async def refresh_token(db:AsyncSession , user_id:int , client_id:int , token_family_id:int):
    token=generate_refresh_token()
    if token_family_id is None:
        token_family_id=uuid.uuid4()
    r_token=RefreshToken(
          token_hash=hash_token(token),
        user_id=user_id,
        client_id=client_id,
        token_family_id=token_family_id,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=REFRESH_TOKEN_TTL_DAYS),
    )   
    result=await create_refresh_token(db , r_token) 
    return result
