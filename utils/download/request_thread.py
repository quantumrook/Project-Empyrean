"""Module used to allow multithreading of the program while it
fetches data from the NWS API.

Raises:
    ValueError: Throws an error if the RequestType is invalid.
"""
import random
import time
from threading import Thread
from urllib.error import HTTPError

import requests
from utils.download.download_status import DownloadStatus
from utils.download.html_status import HTMLStatusCode
from utils.download.request_type import RequestType
from utils.structures.forecast.api.forecast import PropertiesData
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable
from utils.writer import save_forecast_data, save_location_data


class RequestThread(Thread):
    """An extension of the Thread class that handles requesting and processing
    of information from the NWS API.

    Raises:
        ValueError: Throws an error if the RequestType is invalid. This means
        a programming error has occured - not I/O.
    """
    __time_delay_max = 3
    __api_address = 'https://api.weather.gov'

    def __init__(self, location: Location, request_type: RequestType, enable_extra_timeout_protection: bool = True) -> None:
        """Spawns a new thread for requesting data from the NWS API.

        Args:
            location (Location): The location to get information about.
            request_type (RequestType): The API request type to perform.
            enable_extra_timeout_protection (bool, optional): Enables extra sleep calls
            to ensure program doesn't send requests to quickly one after the other. 
            Defaults to True.
        """
        super().__init__()

        self.status                         = WatchedVariable()
        self.status.value                   = DownloadStatus.INSTANTIATING

        self.new_location                   = WatchedVariable()
        self.new_location.value             = None

        self.location       : Location      = location
        self.request_type   : RequestType   = request_type

        self.error_message  :  list[str]    = [ ]
        self.response_json                  = None
        self.__extra_timeout_protection_enabled = enable_extra_timeout_protection

    def __build_url(self) -> str:
        url = f'{self.__api_address}/'
        match self.request_type:
            case RequestType.POINTS:
                url += f'points/{self.location.position.latitude},{self.location.position.longitude}/'
            case RequestType.EXTENDED:
                url += f'gridpoints/{self.location.api_grid.station}/{self.location.api_grid.x},{self.location.api_grid.y}/forecast'
            case RequestType.HOURLY:
                url += f'gridpoints/{self.location.api_grid.station}/{self.location.api_grid.x},{self.location.api_grid.y}/forecast/hourly'
            case _:
                raise ValueError(f"{self.request_type=} for requesting from {self.__api_address} is not valid.\nLocation Data:{self.location.to_json()}")
        
        return url

    def __exectute_timeout_safeguard(self) -> None:
        time.sleep(random.randint(1, self.__time_delay_max))

    def __check_response_code_and_return_json(self, url) -> bool:
        response = None
        try:
            with requests.get(url=url) as request:
                # TODO:: add timeout to request
                # TODO:: format request header according to API specs
                self.status.value = DownloadStatus.REQUEST_RECIEVED
                if self.__extra_timeout_protection_enabled:
                    time.sleep(0.5)
                self.status.value = DownloadStatus.CONVERTING_SOURCE_DATA
                response = request.json()
        except HTTPError as http_err:
            match request.status_code:
                case HTMLStatusCode.NOT_FOUND:
                    self.error_message.append("HTTP Error 404: Most likely too many requests for data have been made in too short of a time, please wait 10 minutes before trying again.")
                case HTMLStatusCode.SERVICE_UNAVAILABLE:
                    self.error_message.append("HTTP Error 503: Service is unavailable. Most likely, there is no new valid forecast to fetch at this time, please try again later.")
            self.status.value = DownloadStatus.REQUEST_FAILED
            self.error_message.append(f"Further details:\n\t{http_err}\n")
            print(self.error_message)
        finally:
            if self.__extra_timeout_protection_enabled:
                time.sleep(0.5)
        return response

    def run(self):

        self.status.value = DownloadStatus.BUILDING_REQUEST
        if self.__extra_timeout_protection_enabled:
            time.sleep(0.5)
        url = self.__build_url()
        self.status.value = DownloadStatus.REQUEST_BUILT
        if self.__extra_timeout_protection_enabled:
            time.sleep(0.5)

        self.status.value = DownloadStatus.API_TIMEOUT_PROTECTION_STARTED
        self.__exectute_timeout_safeguard()
        self.status.value = DownloadStatus.API_TIMEOUT_PROTECTION_COMPLETE
        if self.__extra_timeout_protection_enabled:
            time.sleep(0.5)

        self.status.value = DownloadStatus.SENDING_REQUEST
        if self.__extra_timeout_protection_enabled:
            time.sleep(0.5)
        self.response_json = self.__check_response_code_and_return_json(url=url)
        self.status.value = DownloadStatus.REQUEST_SUCCESS
        if self.__extra_timeout_protection_enabled:
            time.sleep(0.5)
        self.status.value = DownloadStatus.SAVING_DATA
        if self.__extra_timeout_protection_enabled:
            time.sleep(0.5)
        self.save()

    def save(self):
        """Handles saving the corresponding requested information. And triggers callback
        to manager with setting of status.
        """
        if self.request_type == RequestType.POINTS:
            self.new_location.value = save_location_data(self.response_json, self.location)
        else:
            api_data = PropertiesData(self.response_json["properties"])
            self.forecast_to_save = EmpyreanForecast.from_API(api_data)
            save_forecast_data(self.location, self.forecast_to_save)
        if self.__extra_timeout_protection_enabled:
            time.sleep(0.5)
        self.status.value = DownloadStatus.SAVE_COMPLETE

    def update_location_with_new_POINTS_data(self, updated_location):
        """Callback used for updating the location data in place for subsequent requests,
        if we're also performing a POINTS update.
        """
        self.location = updated_location.value
