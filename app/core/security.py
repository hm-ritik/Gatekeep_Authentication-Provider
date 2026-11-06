from pwdlib import PasswordHash
from pathlib import Path
from app.core.config import settings



class PasswordHasher:
    def __init__(self):
         self._hasher=PasswordHash.recommended()


    def hash_password(self ,password:str):
          return self._hasher.hash(password)

    def verify_password(self ,plain_password:str , hashed_password:str):
          return self._hasher.verify(plain_password , hashed_password)

password_hasher=PasswordHasher()    

PRIVATE_KEY = Path(settings.PRIVATE_KEY_PATH).read_text()
PUBLIC_KEY = Path(settings.PUBLIC_KEY_PATH).read_text()