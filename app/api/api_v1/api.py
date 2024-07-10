from fastapi import APIRouter
from .endpoints import eto

api_router = APIRouter()
api_router.include_router(eto.router, prefix="/eto", tags=["eto"])
