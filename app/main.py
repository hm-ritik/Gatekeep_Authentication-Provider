from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.tenant_v1api import router as tenant_router
from app.api.v1.client_v1api import router as client_router
from app.api.v1.user_v1api import router as user_router
from app.core.config import settings
from app.core.database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db.dispose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(tenant_router)
app.include_router(client_router)
app.include_router(user_router)


@app.get("/home")
async def home():
    return{
        "Message" : "Wait Untill I finish this one"
    }