from fastapi import FastAPI
from app.api.v1.routers import api_router
from fastapi.middleware.cors import CORSMiddleware

from core.config import SERVER_PORT, DB_PORT

app = FastAPI(
    title="SSAG MUSIC",
    description="SSAGSSAG",
    version="1.0.0",
)

# 260123 김광원 
# CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:8081",
    f"http://localhost:{SERVER_PORT}",
    f"http://localhost:{DB_PORT}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")