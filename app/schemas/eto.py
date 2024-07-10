from pydantic import BaseModel


class InputParams(BaseModel):
    z_msl: int = 500
    lat: float = -43.6
    lon: int = 172
    tz_lon: int = 173
    freq: str = 'D'
