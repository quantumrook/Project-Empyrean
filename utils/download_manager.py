from enum import Enum
from random import randint
from threading import Thread
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import END, ttk
from tkinter import messagebox
from urllib.error import HTTPError

import requests
import time
from utils.json.forecast import Forecast
from utils.json.private_writer import save_forecast_data


from utils.json.location import Location

class ForecastType(Enum):
    POINTS      = 'points'
    HOURLY      = 'hourly'
    EXTENDED    = 'extended'

    def as_log_str(self):
        return self.name

class DownloadStatus(Enum):
    INSTANTIATING                   = 0
    INITIALIZING                    = 1
    BUILDING_REQUEST                = 2
    REQUEST_BUILT                   = 3
    API_TIMEOUT_PROTECTION_STARTED  = 4
    API_TIMEOUT_PROTECTION_COMPLETE = 5
    SENDING_REQUEST                 = 6
    REQUEST_RECIEVED                = 7
    CONVERTING_SOURCE_DATA          = 8
    REQUEST_FAILED                  = -1
    REQUEST_SUCCESS                 = 9
    SAVING_DATA                     = 10
    SAVE_COMPLETE                   = 11

    def max_value():
        return DownloadStatus.SAVE_COMPLETE.value

    def as_log_str(self):
        return self.name

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

        self.status = DownloadStatus.INSTANTIATING

        self.location = location
        self.forecast_type = forecast_type

        self.response_json = None

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
        
        return url

    def __exectute_timeout_safeguard(self) -> None:
        time.sleep(1)

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

class ForecastDownloader(tk.Toplevel):

    def __init__(self) -> None:
        super().__init__()
        self.wm_title("Download Status")

        self.status_text_log = ScrolledText(self)
        self.status_text_log.grid(column=0, row=0)

        self.downloadbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        self.downloadbar.grid(column=0, row=1)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)


    def save_download(self, download_thread: ForecastDownload):
        download_thread.status = DownloadStatus.SAVING_DATA
        time.sleep(1)
        forecast_to_save = Forecast(download_thread.response_json["properties"])
        save_forecast_data(download_thread.location, download_thread.forecast_type, forecast_to_save)
        time.sleep(1)
        download_thread.status = DownloadStatus.SAVE_COMPLETE
        time.sleep(1)

    def start_download(self, location: Location, forecast_request_type: ForecastType):
        print(f"Download Started for ({location.name}) of type ({forecast_request_type.name}).")
        new_download_thread = ForecastDownload(location, forecast_request_type)
        new_download_thread.name = f'{forecast_request_type}-{location.alias}'
        if threading.active_count() < 3:
            new_download_thread.start()
            self.monitor_download(new_download_thread, DownloadStatus.INSTANTIATING)
        else:
            raise RuntimeError("Oh shit")
    
    def end_download(self, download_thread: ForecastDownload):
        if download_thread.status == DownloadStatus.REQUEST_FAILED:
            print(f'{download_thread.forecast_type.name} for {download_thread.location.name} Failed', download_thread.error_message)
            messagebox.showerror(f'{download_thread.forecast_type} for {download_thread.location.name} Failed', download_thread.error_message)
        
        if threading.active_count() == 1:
            self.downloadbar["value"] = 100
            self.closebutton = tk.Button(self, text="Close", command=self.close_manager)
            self.closebutton.grid(column=0, row=2)

    def monitor_download(self, download_thread: ForecastDownload, previous_status: DownloadStatus):
        progress_count = self.downloadbar["value"]
        for thread in threading.enumerate():
            if isinstance(thread, ForecastDownload):
                progress_count += (thread.status.value * 10) / DownloadStatus.max_value()
        if threading.active_count() > 1:
            self.downloadbar["value"] = round(progress_count / (threading.active_count() - 1))

        if download_thread.is_alive():
            if download_thread.status == DownloadStatus.REQUEST_SUCCESS:
                self.save_download(download_thread)
            log_text = f'({download_thread.location.name}): {download_thread.forecast_type.name} -> {download_thread.status}\n'
            self.status_text_log.insert(END, log_text)
            self.after(1000, lambda: self.monitor_download(download_thread, download_thread.status))
        else:
            self.end_download(download_thread)

    def close_manager(self) -> None:
        widgets = self.grid_slaves()
        for l in widgets:
            l.destroy()
        widgets = None
        self.destroy()