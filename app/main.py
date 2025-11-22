from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.trends import router as trends_router

app = FastAPI(title="Trend Collection System")

# Allow frontend or testing tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(trends_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API is running"}
