import json
from pathlib import Path

from utils.private.private import directory_paths
from utils.structures.forecast.forecast import Forecast
from utils.structures.location.location import Location


def save_forecast_data(location: Location, forecast_type, forecast_data: Forecast):
    directories = ['Forecasts', f'{location.name}', f'{forecast_type.name}']
    filename = directory_paths["project"]

    for directory in directories:
        filename += f'\\{directory}'
        path_to_file = Path(filename)

        if path_to_file.exists():
            continue
        else:
            Path.mkdir(path_to_file)
    
    filename += f'\{forecast_data.generatedAt.date}.json'

    with open(filename, 'w+') as forecast_JSON_file:
        data_as_JSON_Object = json.dumps(forecast_data, indent=4, sort_keys=True)
        forecast_JSON_file.write(data_as_JSON_Object)
