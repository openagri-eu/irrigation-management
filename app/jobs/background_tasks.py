from eto import ETo
from requests import RequestException
from core import settings
from models import Location
from schemas import EToInputData, EtoCreate
from crud import eto

import datetime
import db.session
import requests
import pandas as pd

def get_owm_data():
    session = db.session.SessionLocal()

    locations = session.query(Location).all()

    if len(locations) == 0:
        session.close()
        return

    weather_info = []
    for l in locations:
        try:
            response = requests.get(
                url="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(
                    l.latitude,
                    l.longitude,
                    settings.OWM_API_KEY
                )
            )
        except RequestException:
            continue

        if (response.status_code / 100) != 2:
            continue

        body = response.json()

        weather = EToInputData(
            t_min=body["main"]["temp_min"],
            t_max=body["main"]["temp_max"],
            t_mean=body["main"]["temp"],
            rh_mean=body["main"]["humidity"],
            u_z=body["wind"]["speed"],
            p=body["main"]["pressure"],
            sea_level=body["main"]["sea_level"]
        )

        weather_info.append((weather, l.latitude, l.longitude, l.id))

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

        eto_obj = ETo(df=df, lat=wi[1], lon=wi[2], freq="D", z_msl=wi[0].sea_level)

        eto_calculations.append((wi ,eto_obj.eto_fao()))

    eto.batch_create(db=session, obj_in=[EtoCreate(date=datetime.date.today(), value=c[1].iloc[0], location_id=c[0][3]) for c in eto_calculations])

    session.close()