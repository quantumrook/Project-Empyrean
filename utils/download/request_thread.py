import random
import time
from threading import Thread
from urllib.error import HTTPError

import requests
from utils.download.download_status import DownloadStatus
from utils.download.html_status import HTMLStatusCode
from utils.download.request_type import RequestType
from utils.forecast.location import Location


class RequestThread(Thread):

    __time_delay_max = 3
    __api_address = 'https://api.weather.gov'

    def __init__(self, location: Location, request_type: RequestType) -> None:
        super().__init__()

        self.status                         = DownloadStatus.INSTANTIATING

        self.location       : Location      = location
        self.request_type   : RequestType   = request_type

        self.error_message  :  list[str]    = [ ]
        self.response_json                  = None

    def __build_url(self) -> str:
        url = f'{self.__api_address}/'
        match self.request_type:
            case RequestType.POINTS:
                url += f'points/{self.location.position.lattitude},{self.location.position.longitude}/'
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
        try:
            with requests.get(url=url) as request:
                self.status = DownloadStatus.REQUEST_RECIEVED
                time.sleep(1)
                self.status = DownloadStatus.CONVERTING_SOURCE_DATA
                response = request.json()
        except HTTPError as http_err:
            match request.status_code:
                case HTMLStatusCode.NOT_FOUND:
                    self.error_message.append("HTTP Error 404: Most likely too many requests for data have been made in too short of a time, please wait 10 minutes before trying again.")
                case HTMLStatusCode.SERVICE_UNAVAILABLE:
                    self.error_message.append("HTTP Error 503: Service is unavailable. Most likely, there is no new valid forecast to fetch at this time, please try again later.")
            self.status = DownloadStatus.REQUEST_FAILED
            self.error_message.append(f"Further details:\n\t{http_err}\n")
            print(self.error_message)
        finally:
            time.sleep(1)
            return response

    def run(self):

        self.status = DownloadStatus.BUILDING_REQUEST
        time.sleep(1)
        url = self.__build_url()
        self.status = DownloadStatus.REQUEST_BUILT
        time.sleep(0.5)

        self.status = DownloadStatus.API_TIMEOUT_PROTECTION_STARTED
        self.__exectute_timeout_safeguard()
        self.status = DownloadStatus.API_TIMEOUT_PROTECTION_COMPLETE
        time.sleep(1)

        self.status = DownloadStatus.SENDING_REQUEST
        time.sleep(0.5)
        self.response_json = self.__check_response_code_and_return_json(url=url)
        self.status = DownloadStatus.REQUEST_SUCCESS
        time.sleep(1)
