from pydantic import Field , field_validator
from pydantic_settings import BaseSettings , SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    
    SECRET_KEY: str=Field(..., min_length=32, description="Secret for sessions/cookies")
    PRIVATE_KEY_PATH: str  =Field(..., description="Path to RSA private key")
    PUBLIC_KEY_PATH: str =Field(..., description="Path to RSA public key")
    
    JWT_ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    ID_TOKEN_EXPIRE_MINUTES: int = 5  

    APP_NAME: str = "GateKeep"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings=Settings()    