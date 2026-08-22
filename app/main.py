from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.user_v1api import router as user_router
from app.core.database import async_engine,Base
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler 
from slowapi.errors import RateLimitExceeded

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
     pass

    yield    


app=FastAPI(title="GateKeep" , lifespan=lifespan)
app.include_router(user_router , prefix="/user")


#ratelimiting
app.state.limiter = limiter
app.add_exception_handler( RateLimitExceeded,_rate_limit_exceeded_handler)

@app.get("/home")
async def health():
    return{
        "Message" : "Checking system"
    }
