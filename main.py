from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.trends import router as trends_router
from app.api.routes.trend_collector import router as collector_router
from app.db.session import engine
from app.db.base import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trend Analyzer API")

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(trends_router, prefix="/api", tags=["Trends"])
app.include_router(collector_router, prefix="/api/collect", tags=["Trend Collector"])

@app.get("/")
def root():
    return {"message": "Trend Analyzer is running!"}
