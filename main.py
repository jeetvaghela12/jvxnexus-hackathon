from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import Base, engine
from core.config import settings
from models.user_model import User
from models.clientshield_model import ClientShieldReport
from api.auth_routes import router as auth_router
from api.clientshield_routes import router as clientshield_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.include_router(auth_router)
app.include_router(clientshield_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}