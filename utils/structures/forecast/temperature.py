from dataclasses import dataclass
from typing import Any


@dataclass
class Temperature():
    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.value : int    = forecast_data["temperature"]
        self.unit  : str    = forecast_data["temperatureUnit"]
        self.trend : str    = forecast_data["temperatureTrend"]
