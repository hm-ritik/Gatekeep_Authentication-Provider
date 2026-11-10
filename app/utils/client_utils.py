import hashlib
import secrets
import hmac

def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)

def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()


class ClientHelper:
   
    @staticmethod
    def generate_clientid(self):
        return self.secrets.token_urlsafe(16)
    @staticmethod
    def generate_client_secret() -> str:
         return secrets.token_urlsafe(32)
    @staticmethod
    def hash_token(raw_token:str):
            return hashlib.sha256(raw_token.encode()).hexdigest()
    @staticmethod
    def verify_client_secret(plain_secret: str, hashed_secret: str) -> bool:
        generated_hash = hashlib.sha256(plain_secret.encode()).hexdigest()

        return hmac.compare_digest(generated_hash, hashed_secret)


helper=ClientHelper()
        

    