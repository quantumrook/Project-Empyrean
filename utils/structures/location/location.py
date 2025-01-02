"""Module for interfacing between Empyrean and the NWS API"""
from dataclasses import dataclass
from typing import Any


@dataclass
class Position():
    """Helper class for holding latitude and longitude information."""
    class Keys():
        """Helper class for maping dictionary keys to variables."""
        latitude = "latitude"
        longitude = "longitude"
    latitude   : str
    longitude   : str

    def __init__(self, data: dict[str, str]) -> None:
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]

    def to_json(self) -> dict[str, str]:
        """Helper funciton for preparing to convert to JSON"""
        return {
            "latitude" : self.latitude,
            "longitude" : self.longitude
        }

@dataclass
class API_Grid():
    """Helper class for holding API information."""
    class Keys():
        """Helper class for maping dictionary keys to variables."""
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
        """Helper funciton for preparing to convert to JSON"""
        return {
            API_Grid.Keys.lastverified  : self.lastverified,
            API_Grid.Keys.x             : self.x,
            API_Grid.Keys.y             : self.y,
            API_Grid.Keys.station       : self.station
        }

@dataclass
class Location():
    """Helper class for maping API data to Empyrean friendly usage."""
    class Keys():
        """Helper class for maping dictionary keys to variables."""
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
        """Helper funciton for preparing to convert to JSON"""
        return {
            "alias"     : self.alias,
            "name"      : self.name,
            "position"  : self.position.to_json(),
            "api_grid"  : self.api_grid.to_json(),
            "timezone"  : self.timezone
        }
