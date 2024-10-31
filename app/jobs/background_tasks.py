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

    lat_lon_values = []
    for loc in locations:
        if loc.state_code is not None:
            try:
                response = requests.get(
                    url="http://api.openweathermap.org/geo/1.0/direct?q={},{},{}&appid={}".format(loc.city_name,
                                                                                                  loc.state_code,
                                                                                                  loc.country_code,
                                                                                                  settings.OWM_API_KEY)
                )
            except RequestException:
                continue
        else:
            try:
                response = requests.get(
                    url="http://api.openweathermap.org/geo/1.0/direct?q={},{}&appid={}".format(
                        loc.city_name,
                        loc.country_code,
                        settings.OWM_API_KEY
                    )
                )
            except RequestException:
                continue

        if (response.status_code / 100) != 2:
            continue

        body = response.json()

        if len(body) == 0:
            continue

        lat_lon_values.append((loc ,body[0]["lat"], body[0]["lon"]))

    if len(lat_lon_values) == 0:
        session.close()
        return

    weather_info = []
    for ll in lat_lon_values:
        try:
            response = requests.get(
                url="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric".format(
                    ll[1],
                    ll[2],
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

        weather_info.append((ll[0], weather, ll[1], ll[2]))

    eto_calculations = []

    for wi in weather_info:
        df_dict = {
            "T_min": [wi[1].t_min],
            "T_max": [wi[1].t_max],
            "T_mean": [wi[1].t_mean],
            "RH_mean": [wi[1].rh_mean],
            "U_z": [wi[1].u_z],
            "P": [wi[1].p]
        }
        df = pd.DataFrame(data=df_dict, index=[datetime.datetime.now()])

        eto_obj = ETo(df=df, lat=wi[2], lon=wi[3], freq="D", z_msl=wi[1].sea_level)

        eto_calculations.append((wi ,eto_obj.eto_fao()))

    for c in eto_calculations:
        eto.create(
            db=session,
            obj_in=EtoCreate(
                date=datetime.date.today(),
                value=c[1].iloc[0],
                location_id=c[0][0].id,
            )
        )

    session.commit()
    session.close()