from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.trends import router as trends_router
from app.api.routes.trend_collector import router as collector_router

from app.db.session import engine
from app.db.base_class import Base   # ✅ THIS IS THE FIX

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)   # ✅ NOW Base exists

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(trends_router, prefix="/api", tags=["Trends"])
app.include_router(collector_router, prefix="/api/collect", tags=["Collector"])

@app.get("/")
def root():
    return {"message": "API running on Render!"}
