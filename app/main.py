from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.user_v1api import router as user_router
from app.core.database import async_engine,Base

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield    


app=FastAPI(title="GateKeep" , lifespan=lifespan)
app.include_router(user_router , prefix="/user")

@app.get("/home")
async def health():
    return{
        "Message" : "Checking system"
    }
