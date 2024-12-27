import json
from pathlib import Path

from utils.structures.location.location import Location


def get_private_data(filename: str):
    with open(filename) as file:
        data = json.load(file)

    locations = [ ]
    for location in data["locations"]:
        location_data = Location(location)
        locations.append(location_data)
    return locations

def get_test_data(filename: str):
    with open(filename) as file:
        data = json.load(file)
    return data

def get_forecast_data(filename: str):

    path_to_file = Path(filename)
    if path_to_file.exists():
        with open(filename) as file:
            data = json.load(file)
        return data
    return None