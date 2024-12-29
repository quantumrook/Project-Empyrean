import json
from pathlib import Path

from utils.private.private import directory_paths, user_default_timezone
from utils.structures.datetime import TODAY
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.location.location import API_Grid, Location, Position


def save_forecast_data(location: Location, forecast_data: EmpyreanForecast):
    directories = ['Forecasts', f'{location.name}', f'{forecast_data.frontmatter.forecast_type.name.title()}']
    filename = directory_paths["project"]

    for directory in directories:
        filename += f'\\{directory}'
        path_to_file = Path(filename)

        if path_to_file.exists():
            continue
        else:
            Path.mkdir(path_to_file)
    
    filename += f'\\{forecast_data.frontmatter.generated.date}.json'

    with open(filename, 'w+') as forecast_JSON_file:
        data_as_JSON_Object = json.dumps(forecast_data.to_dict(), indent=4, sort_keys=False)
        # data_as_JSON_Object = json.dumps(forecast_data, indent=4, sort_keys=True)
        forecast_JSON_file.write(data_as_JSON_Object)

def save_location_data(response_json, location_properties) -> Location:
    properties = response_json["properties"]
    points = response_json["id"].split("/")
    lat, lon = points[-1].split(",")

    timezone = user_default_timezone
    if location_properties[Location.Keys.timezone]:
        timezone = location_properties[Location.Keys.timezone]

    location_to_add = Location(
        {
            Location.Keys.alias : location_properties[Location.Keys.alias],
            Location.Keys.name  : location_properties[Location.Keys.name],
            Location.Keys.position : {
                Position.Keys.lattitude : lat,
                Position.Keys.longitude : lon
            },
            Location.Keys.api_grid : {
                API_Grid.Keys.lastverified  : TODAY.date,
                API_Grid.Keys.x             : properties["gridX"],
                API_Grid.Keys.y             : properties["gridY"],
                API_Grid.Keys.station       : properties["cwa"]
            },
            Location.Keys.timezone : timezone
        }
    )

    filename = f'{directory_paths["private"]}\\private.json'

    with open(filename, 'r+') as location_JSON_file:
        data_from_file = json.load(location_JSON_file)

    data_from_file["locations"].append(location_to_add.to_json())
    data_as_JSON_Object = json.dumps(data_from_file, indent=4, sort_keys=False)

    with open(filename, 'w+') as location_JSON_file:
        location_JSON_file.write(data_as_JSON_Object)

    return location_to_add