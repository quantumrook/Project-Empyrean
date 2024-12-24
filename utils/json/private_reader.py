import json

from utils.forecast.location import Location

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