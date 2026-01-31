from datetime import datetime

from typing import List

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: List[float]


class TemperatureUpdate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int
