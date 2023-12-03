from enum import Enum


class DailyParameters(Enum):
    temperature_2m_max = "temperature_2m_max"
    temperature_2m_min = "temperature_2m_min"
    rain_sum = "rain_sum"
    precipitation_hours = "precipitation_hours"
    windspeed_10m_max = "windspeed_10m_max"

    def __str__(self):
        return str(self.value)
