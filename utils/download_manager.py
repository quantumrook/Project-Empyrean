from enum import Enum, auto
from random import randint
from threading import Thread
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import END, ttk
from tkinter import messagebox
from urllib.error import HTTPError

import requests
import time


from utils.json.location import Location

class ForecastType(Enum):
    POINTS      = 'points'
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'

class DownloadStatus(Enum):
    INITIALIZING                    = 1
    BUILDING_REQUEST                = 2
    REQUEST_BUILT                   = 3
    API_TIMEOUT_PROTECTION_STARTED  = 4
    API_TIMEOUT_PROTECTION_COMPLETE = 5
    SENDING_REQUEST                 = 6
    REQUEST_RECIEVED                = 7
    REQUEST_FAILED                  = -1
    REQUEST_SUCCESS                 = 8

class HTMLStatusCode(Enum):
    OK                  = 200
    NOT_FOUND           = 404
    SERVICE_UNAVAILABLE = 503

class ForecastDownload(Thread):

    __time_delay_max = 3
    __api_address = 'https://api.weather.gov'

    location:       Location       = None
    response_json                  = None
    error_message:  list[str]      = [ ]

    def __init__(self, location: Location, forecast_type: ForecastType) -> None:
        super().__init__()

        self.status = DownloadStatus.INITIALIZING

        self.location = location
        self.forecast_type = forecast_type

    def __build_url(self) -> str:
        url = f'{self.__api_address}/'
        match self.forecast_type:
            case ForecastType.POINTS:
                url += f'points/{self.location.position.lattitude},{self.location.position.longitude}/'
            case ForecastType.EXTENDED:
                url += f'gridpoints/{self.location.api_grid.station}/{self.location.api_grid.x},{self.location.api_grid.y}/forecast'
            case ForecastType.HOURLY:
                url += f'gridpoints/{self.location.api_grid.station}/{self.location.api_grid.x},{self.location.api_grid.y}/forecast/hourly'
            case default:
                print(f"{self.forecast_type=} for requesting from {self.__api_address} is not valid.\nLocation Data:{self.location.to_json()}")
                raise ValueError(f"{self.forecast_type=} for requesting from {self.__api_address} is not valid.\nLocation Data:{self.location.to_json()}")
        time.sleep(randint(1, self.__time_delay_max))
        return url

    def __exectute_timeout_safeguard(self) -> None:
        time.sleep(randint(1, self.__time_delay_max))

    def __check_response_code_and_return_json(self, url) -> bool:
        time.sleep(randint(1, self.__time_delay_max))
        self.status.SENDING_REQUEST
        time.sleep(randint(1, self.__time_delay_max))
        try:
            with requests.get(url=url) as request:
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
            return response

    def run(self):

        self.status = DownloadStatus.BUILDING_REQUEST
        url = self.__build_url()
        self.status = DownloadStatus.REQUEST_BUILT
        
        self.status = DownloadStatus.API_TIMEOUT_PROTECTION_STARTED
        self.__exectute_timeout_safeguard()
        self.status = DownloadStatus.API_TIMEOUT_PROTECTION_COMPLETE

        self.response_json = self.__check_response_code_and_return_json(url=url)
        self.status = DownloadStatus.REQUEST_SUCCESS

class ForecastDownloader(tk.Toplevel):
    _open_threads : list[ForecastDownload]

    def __init__(self) -> None:
        super().__init__()
        self.wm_title("Download Status")

        self._open_threads = [ ]

        self.status_text_log = ScrolledText(self)
        self.status_text_log.grid(column=0, row=0)

        self.downloadbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        self.downloadbar.grid(column=0, row=1)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)


    def save_download(self, content):
        print("Tried to save, but we're not there yet!")
        pass

    def start_download(self, location: Location, forecast_request_type: ForecastType):
        print("Download Started.")
        if self._open_threads:
            for thread in self._open_threads:
                if (thread.forecast_type == forecast_request_type) and (thread.location == location):
                    raise Exception(f"Download already exists for: {location.alias} @ {forecast_request_type}")
        self._open_threads.append(ForecastDownload(location, forecast_request_type))
        self._open_threads[-1].start()
        self.monitor_download(self._open_threads[-1])
    
    def end_download(self, download_thread: ForecastDownload):
        if download_thread.status == DownloadStatus.REQUEST_SUCCESS:
            self.save_download(download_thread.response_json)
        else:
            print(f'{download_thread.forecast_type} for {download_thread.location.name} Failed', download_thread.error_message)
            messagebox.showerror(f'{download_thread.forecast_type} for {download_thread.location.name} Failed', download_thread.error_message)
            self._open_threads.remove(download_thread)
            download_thread = None
        
        if len(self._open_threads) == 0:
            self.downloadbar["value"] = 100
            self.closebutton = tk.Button(self, text="Close", command=self.close_manager)
            self.closebutton.grid(column=0, row=2)

    def monitor_download(self, download_thread: ForecastDownload):
        if download_thread.is_alive():
            log_text = f'Thread: {download_thread.location.name}; Type: {download_thread.forecast_type}; Status: {download_thread.status}\n'
            print(log_text)
            self.status_text_log.insert(END, log_text)
            self.after(100, lambda: self.monitor_download(download_thread))
        else:
            self.end_download(download_thread)

        progress_count = 0
        for thread in self._open_threads:
            progress_count += int(thread.status)
        if len(self._open_threads) > 0:
            self.downloadbar["value"] = round(progress_count/len(self._open_threads))

    def close_manager(self) -> None:
        self._open_threads = None
        widgets = self.grid_slaves()
        for l in widgets:
            l.destroy()
        widgets = None
        self.destroy()