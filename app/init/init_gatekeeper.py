import requests
from fastapi import APIRouter

from core.config import settings

from api.api_v1.endpoints import dataset, eto, location

def register_apis_to_gatekeeper():

    at = requests.post(
        url=str(settings.GATEKEEPER_BASE_URL) + "/api/login/",
        headers={"Content-Type": "application/json"},
        json={
            "username": "{}".format(settings.GATEKEEPER_USERNAME),
            "password": "{}".format(settings.GATEKEEPER_PASSWORD)
        }
    )

    temp = at.json()

    access = temp["access"]
    refresh = temp["refresh"]


    # Registration

    apis_to_register = APIRouter()

    apis_to_register.include_router(dataset.router, prefix="/dataset")
    apis_to_register.include_router(eto.router, prefix="/eto")
    apis_to_register.include_router(location.router, prefix="/location")

    for api in apis_to_register.routes:

        requests.post(
            url=str(settings.GATEKEEPER_BASE_URL) + "/api/register_service/",
            headers={"Content-Type": "application/json", "Authorization" : "Bearer {}".format(access)},
            json={
                "base_url": "http://{}:{}/".format(settings.SERVICE_NAME, settings.SERVICE_PORT),
                "service_name": settings.SERVICE_NAME,
                "endpoint": "api/v1/" + api.path.strip("/"),
                "methods": list(api.methods)
            }
        )


    requests.post(
        url=str(settings.GATEKEEPER_BASE_URL) + "/api/logout/",
        headers={"Content-Type": "application/json"},
        json={"refresh": refresh}
    )

    return