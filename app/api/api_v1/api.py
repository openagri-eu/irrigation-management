from sys import prefix

from fastapi import APIRouter
from .endpoints import eto, dataset

api_router = APIRouter()
api_router.include_router(eto.router, prefix="/eto", tags=["eto"])
api_router.include_router(dataset.router, prefix="/dataset", tags=["dataset"])
