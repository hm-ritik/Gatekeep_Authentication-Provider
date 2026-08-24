from pwdlib import PasswordHash
from pathlib import Path
from app.core.config import settings

pwd=PasswordHash.recommended()

def hash_password(password:str):
    return pwd.hash(password)

def verify_password(plain_password:str , hashed_password:str):
    return pwd.verify(plain_password , hashed_password)

PRIVATE_KEY = Path(settings.PRIVATE_KEY_PATH).read_text()
PUBLIC_KEY = Path(settings.PUBLIC_KEY_PATH).read_text()