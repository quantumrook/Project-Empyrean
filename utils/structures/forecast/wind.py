from dataclasses import dataclass
from typing import Any


@dataclass
class Wind():
    def __init__(self, forecast_data: dict[str, Any]) -> None:
        self.value       : int
        self.unit        : str
        self.direction   : str
        self.rawvalue    : str

        self.rawvalue = forecast_data["windSpeed"]
        if len(self.rawvalue.split(' ')) > 2:
            low_speed, to, highspeed, self.unit = self.rawvalue.split(' ')
            self.value = round((int(highspeed) + int(low_speed))/2)
        else:
            self.value, self.unit = forecast_data["windSpeed"].split(' ')
        
        self.direction = forecast_data["windDirection"]
