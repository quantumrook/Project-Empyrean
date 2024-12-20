from dataclasses import dataclass
from time import timezone
from typing import Any

@dataclass
class Position():
    lattitude   : str
    longitude   : str

    def __init__(self, data: dict[str, str]) -> None:
        self.lattitude = data["lattitude"]
        self.longitude = data["longitude"]

    def to_json(self) -> dict[str, str]:
        return {
            "lattitude" : self.lattitude,
            "longitude" : self.longitude
        }

@dataclass
class API_Grid():
    lastverified    : str
    x               : str
    y               : str
    station         : str

    def __init__(self, data: dict[str, str]) -> None:
        self.lastverified = data["lastverified"]
        self.x = data["x"]
        self.y = data["y"]
        self.station = data["station"]

    def to_json(self) -> dict[str, str]:
        return {
            "lastverified"  : self.lastverified,
            "x"             : self.x,
            "y"             : self.y,
            "station"       : self.station
        }

@dataclass
class Location():
    alias       : str
    name        : str
    position    : Position
    api_grid    : API_Grid
    timezone    : str

    def __init__(self, location_data: dict[str, Any]) -> None:
        self.alias = location_data["alias"]
        self.name = location_data["name"]
        self.position = Position(location_data["position"])
        self.api_grid = API_Grid(location_data["api_grid"])
        self.timezone = location_data["timezone"]

    def to_json(self):
        return {
            "alias"     : self.alias,
            "name"      : self.name,
            "position"  : self.position.to_json(),
            "api_grid"  : self.api_grid.to_json(),
            "timezone"  : self.timezone
        }
