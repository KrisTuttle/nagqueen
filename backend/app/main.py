from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import Base, engine
from .routers import auth, reminders, admin
from .scheduler import start_scheduler, stop_scheduler

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    # Shutdown
    stop_scheduler()


app = FastAPI(
    title="Nag Queen",
    description="SMS reminder service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(reminders.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Nag Queen API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy"}
