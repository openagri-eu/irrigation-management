from fastapi import APIRouter
from .endpoints import login, user, eto, location, dataset

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(eto.router, prefix="/eto", tags=["eto"])
api_router.include_router(location.router, prefix="/location", tags=["location"])
api_router.include_router(dataset.router, prefix="/dataset", tags=["dataset"])
