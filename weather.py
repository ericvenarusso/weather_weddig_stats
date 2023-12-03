from datetime import datetime
from typing import List

import requests
from pytz.tzinfo import DstTzInfo

from parameters import DailyParameters
from response import WeatherResponse


class Weather:
    def __init__(self, latitude: float, longitude: float):
        self._url = "https://archive-api.open-meteo.com/v1/archive"
        self.latitude = latitude
        self.longitude = longitude

    def get(
        self,
        start_date: datetime,
        end_date: datetime,
        timezone: DstTzInfo,
        daily_parameters: List[DailyParameters],
    ) -> WeatherResponse:
        response = requests.get(
            self._url,
            params={
                "latitude": self.latitude,
                "longitude": self.longitude,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "timezone": timezone,
                "daily": daily_parameters,
            },
        ).json()
        return WeatherResponse(**response)
