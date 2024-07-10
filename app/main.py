from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.api_v1.api import api_router

app = FastAPI(
    title="Irrigation Management", openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
