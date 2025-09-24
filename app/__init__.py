from . import models
from fastapi import FastAPI
from .database import engine
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

fastapi_app = FastAPI()

# Add the CORS middleware before you define your routes
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           
    allow_credentials=True,           
    allow_methods=["*"],              
    allow_headers=["*"],              
)

# Include routes
fastapi_app.include_router(router)

# Create tables at startup
@fastapi_app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)




