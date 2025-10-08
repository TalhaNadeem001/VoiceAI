from fastapi import FastAPI
from models.auth import Base
from database import engine, DATABASE_URL
from routes import auth, agent_management
from contextlib import asynccontextmanager
from scheduler import create_scheduler

# Create APScheduler with Postgres persistence
scheduler = create_scheduler(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if not scheduler.running:
        scheduler.start()
    print("Scheduler started")

    yield  # <-- FastAPI runs while this is active

    # Shutdown
    scheduler.shutdown(wait=False)
    print("Scheduler stopped")

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(lifespan=lifespan)

# Include auth routes
app.include_router(auth.router)
app.include_router(agent_management.router)