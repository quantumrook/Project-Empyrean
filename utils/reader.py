"""Helper functions for loading JSON data into the program.
"""
import json
from pathlib import Path

from utils.structures.location.location import Location


def get_private_data(filename: str) -> list[Location]:
    """Load the location data already saved.

    Args:
        filename (str): The complete filename path to the data.

    Returns:
        list[Location]: A list of the location data as objects.
    """
    with open(filename) as file:
        data = json.load(file)

    if "locations" not in data:
        return [ ]

    locations = [ ]
    for location in data["locations"]:
        location_data = Location(location)
        locations.append(location_data)
    return locations

def get_test_data(filename: str) -> dict:
    """Helper function for loading test JSON data.

    Args:
        filename (str): The complete filename path to the data.

    Returns:
        dict: The test data.
    """
    with open(filename) as file:
        data = json.load(file)
    return data

def get_forecast_data(filename: str) -> dict | None:
    """Helper function for loading forecast JSON data.

    Args:
        filename (str): The complete filename path to the data.
        
    Returns:
        dict: The JSON forecast data
    """
    path_to_file = Path(filename)
    if path_to_file.exists():
        with open(filename) as file:
            data = json.load(file)
        return data
    return None
