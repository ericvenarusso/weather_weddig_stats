import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Union


@dataclass
class DailyValues:
    time: List[str]
    temperature_2m_max: List[Union[float, None]]
    temperature_2m_min: List[Union[float, None]]
    rain_sum: List[Union[float, None]]
    precipitation_hours: List[Union[float, None]]
    windspeed_10m_max: List[Union[float, None]]


@dataclass
class DailyUnits:
    time: str
    temperature_2m_max: str
    temperature_2m_min: str
    rain_sum: str
    precipitation_hours: str
    windspeed_10m_max: str


@dataclass
class WeatherResponse:
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    daily_units: DailyUnits
    daily: DailyValues

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def save(self, filename) -> None:
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file)
