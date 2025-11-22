from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.trends import router as trends_router
from app.db.base import Base
from app.db.session import engine

# Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trend Collection API",
    version="1.0.0",
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(trends_router, prefix="/api/trends", tags=["Trends"])


@app.get("/")
def home():
    return {"message": "Trend API is running"}
