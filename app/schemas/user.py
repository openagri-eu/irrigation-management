from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    password: str


class UserMe(BaseModel):
    email: str

    model_config = ConfigDict(from_attributes=True)
