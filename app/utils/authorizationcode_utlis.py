import secrets
import hashlib


class AuthorizationCode_Helper:
    @staticmethod
    def generate_token():
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_token(raw_token:str):
        return hashlib.sha256(raw_token.encode()).hexdigest()