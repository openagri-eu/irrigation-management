from fastapi import APIRouter
from eto import ETo, datasets
import pandas as pd
from schemas import InputParams


router = APIRouter()


@router.post("/")
def calculate(
    ip: InputParams
):
    """
    Calculate the Reference evapotranspiration (ETo) according to FAO standards.
    """

    et = ETo()

    # The test data in question
    example = datasets.get_path('example_daily')
    tsdata = pd.read_csv(example, parse_dates=True, infer_datetime_format=True, index_col='date')

    et.param_est(tsdata, ip.freq, ip.z_msl, ip.lat, ip.lon, ip.tz_lon)
    et.ts_param.head()

    eto1 = et.eto_fao()

    return eto1.to_json()
