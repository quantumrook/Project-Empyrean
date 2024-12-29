import threading
import time
import tkinter as tk
from tkinter import END, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from utils.download.download_status import DownloadStatus
from utils.download.request_thread import RequestThread
from utils.download.request_type import RequestType
from utils.structures.forecast.api.forecast import PropertiesData
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.location.location import Location
from utils.writer import save_forecast_data, save_location_data


class RequestThreadManager_Window(tk.Toplevel):

    max_thread_count = 5    
    queue: list[RequestThread] = [ ]

    stepsize: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.wm_title("Download Status")

        self.forecast_to_save:   EmpyreanForecast = None
        self.request_type:       RequestType = RequestType.POINTS
        self.download_status:    DownloadStatus = DownloadStatus.INSTANTIATING
        self.location_properties = { 
            Location.Keys.alias : "",
            Location.Keys.name : "",
            Location.Keys.timezone : ""
        }

        self.new_location: Location = None
        self.status_text_log = ScrolledText(self)
        self.status_text_log.grid(column=0, row=0)

        self.downloadbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        self.downloadbar.grid(column=0, row=1)

        self.stepsize = round(100 / DownloadStatus.max_value())

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.number_of_requests = 0

    def save_download(self, download_thread: RequestThread):
        download_thread.status = DownloadStatus.SAVING_DATA
        time.sleep(1)
        if (download_thread.request_type == RequestType.POINTS):
            self.new_location = save_location_data(download_thread.response_json, self.location_properties)
        else:
            api_data = PropertiesData(download_thread.response_json["properties"])
            self.forecast_to_save = EmpyreanForecast.from_API(api_data)
            save_forecast_data(download_thread.location, self.forecast_to_save)
        time.sleep(1)
        download_thread.status = DownloadStatus.SAVE_COMPLETE

    def enqueue_download(self, location: Location, forecast_request_type: RequestType):
        self.request_type = forecast_request_type
        print(f"Download Started for ({location.name}) of type ({forecast_request_type.value}).")
        new_download_thread = RequestThread(location, forecast_request_type)
        new_download_thread.name = f'{forecast_request_type}-{location.alias}'

        if self.location_properties[Location.Keys.alias] == "":
                self.location_properties[Location.Keys.alias] = location.alias
                self.location_properties[Location.Keys.name] = location.name
                self.location_properties[Location.Keys.timezone] = location.timezone
        self.number_of_requests += 1
        self.queue.append(new_download_thread)
    
    def end_download(self, download_thread: RequestThread):
        if download_thread.status == DownloadStatus.REQUEST_FAILED:
            print(f'{download_thread.request_type.name} for {download_thread.location.name} Failed', download_thread.error_message)
            messagebox.showerror(f'{download_thread.request_type} for {download_thread.location.name} Failed', download_thread.error_message)

    def monitor_queue(self):

        current_thread_count = 0
        still_have_active_thread = False
        currently_updating_location = False

        for thread in threading.enumerate():
            if isinstance(thread, RequestThread):
                if thread.is_alive() == True:
                    still_have_active_thread = True
                else:
                    current_thread_count -= 1
                if thread.request_type == RequestType.POINTS:
                    currently_updating_location = True
                current_thread_count += 1
        if current_thread_count > self.number_of_requests:
            raise RuntimeError("Forcing Exception - too many threads tried to execute.")

        #TODO :: Allow Hourly and Extended to download simultaneously?

        if currently_updating_location == False and still_have_active_thread == False and len(self.queue) > 0:
            new_download_thread = self.queue.pop(0)
            if self.new_location is not None:
                if new_download_thread.location.alias == self.new_location.alias:
                    new_download_thread.location = self.new_location
            new_download_thread.start()
            self.monitor_download(new_download_thread)
            still_have_active_thread = True

        if still_have_active_thread == False:
            self.download_status = DownloadStatus.SAVE_COMPLETE
            self.downloadbar["value"] = 100
            self.closebutton = tk.Button(self, text="Close", command=self.close_manager)
            self.closebutton.grid(column=0, row=2)

    def monitor_download(self, download_thread: RequestThread):

        progress_count = self.downloadbar["value"]
        for thread in threading.enumerate():
            if isinstance(thread, RequestThread):
                progress_count += round(self.stepsize / self.number_of_requests )
        if threading.active_count() > 1:
            if progress_count > self.downloadbar["value"]:
                self.downloadbar["value"] = progress_count

        if download_thread.is_alive():
            if download_thread.status == DownloadStatus.REQUEST_SUCCESS:
                self.save_download(download_thread)
            log_text = f'({download_thread.location.name}): {download_thread.request_type.name} -> {download_thread.status}\n'
            self.status_text_log.insert(END, log_text)
            self.after(1000, lambda: self.monitor_download(download_thread))
            if download_thread.status == DownloadStatus.SAVE_COMPLETE:
                self.monitor_queue()
        else:
            self.end_download(download_thread)

    def close_manager(self) -> None:
        widgets = self.grid_slaves()
        for l in widgets:
            l.destroy()
        widgets = None
        self.destroy()
