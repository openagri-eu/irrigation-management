from eto import ETo
from requests import RequestException
from models import Location
from schemas import EToInputData, EtoCreate
from crud import eto

import datetime
import db.session
import requests
import pandas as pd

def get_weather_data():
    session = db.session.SessionLocal()

    locations = session.query(Location).all()

    if len(locations) == 0:
        session.close()
        return

    weather_info = []
    for l in locations:
        try:
            response = requests.get(
                url="https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,"
                    "temperature_2m_mean,relative_humidity_2m_mean,pressure_msl_mean,surface_pressure_mean,"
                    "wind_speed_10m_mean,temperature_2m_min&timezone=auto&past_days=1&forecast_days=1".format(
                    l.latitude,
                    l.longitude),
                timeout=120
            )
        except RequestException:
            continue

        if (response.status_code / 100) != 2:
            continue

        body = response.json()

        # Attempt to extract information
        try:
            weather = EToInputData(
                t_min=body["daily"]["temperature_2m_min"][1],
                t_max=body["daily"]["temperature_2m_max"][1],
                t_mean=body["daily"]["temperature_2m_mean"][1],
                rh_mean=body["daily"]["relative_humidity_2m_mean"][1],
                u_z=body["daily"]["wind_speed_10m_mean"][1],
                p=body["daily"]["surface_pressure_mean"][1] / 10,
                sea_level=int(body["daily"]["pressure_msl_mean"][1])
            )
        except Exception:
            continue

        weather_info.append((weather, l.latitude, l.longitude, l.id, body["elevation"]))

    eto_calculations = []

    for wi in weather_info:
        df_dict = {
            "T_min": [wi[0].t_min],
            "T_max": [wi[0].t_max],
            "T_mean": [wi[0].t_mean],
            "RH_mean": [wi[0].rh_mean],
            "U_z": [wi[0].u_z],
            "P": [wi[0].p]
        }
        df = pd.DataFrame(data=df_dict, index=[datetime.datetime.now()])

        eto_obj = ETo(df=df, lat=wi[1], lon=wi[2], freq="D", z_msl=wi[4], z_u=10)

        eto_calculations.append((wi, eto_obj.eto_fao()))

    eto.batch_create(db=session, obj_in=[EtoCreate(date=datetime.date.today(), value=c[1].iloc[0], location_id=c[0][3]) for c in eto_calculations])

    session.close()
