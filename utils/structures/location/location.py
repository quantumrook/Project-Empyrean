from dataclasses import dataclass
from typing import Any


@dataclass
class Position():
    class Keys():
        lattitude = "lattitude"
        longitude = "longitude"
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
    class Keys():
        lastverified = "lastverified"
        x = "x"
        y = "y"
        station = "station"
    lastverified    : str
    x               : str
    y               : str
    station         : str

    def __init__(self, data: dict[str, str]) -> None:
        self.lastverified = data[API_Grid.Keys.lastverified]
        self.x = data[API_Grid.Keys.x]
        self.y = data[API_Grid.Keys.y]
        self.station = data[API_Grid.Keys.station]

    def to_json(self) -> dict[str, str]:
        return {
            API_Grid.Keys.lastverified  : self.lastverified,
            API_Grid.Keys.x             : self.x,
            API_Grid.Keys.y             : self.y,
            API_Grid.Keys.station       : self.station
        }

@dataclass
class Location():
    class Keys():
        alias = "alias"
        name = "name"
        position = "position"
        api_grid = "api_grid"
        timezone = "timezone"
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
