import threading
import time
import tkinter as tk
from tkinter import END, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from utils.download.download_status import DownloadStatus
from utils.download.request_thread import RequestThread
from utils.download.request_type import RequestType
from utils.structures.forecast.forecast import Forecast
from utils.structures.location.location import Location
from utils.writer import save_forecast_data


class RequestThreadManager_Window(tk.Toplevel):

    max_thread_count = 3    

    def __init__(self) -> None:
        super().__init__()
        self.wm_title("Download Status")

        self.forecast_to_save:   Forecast = None
        self.request_type:       RequestType = RequestType.POINTS
        self.download_status:    DownloadStatus = DownloadStatus.INSTANTIATING

        self.status_text_log = ScrolledText(self)
        self.status_text_log.grid(column=0, row=0)

        self.downloadbar = ttk.Progressbar(self, orient='horizontal', mode='determinate', length=200)
        self.downloadbar.grid(column=0, row=1)

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)


    def save_download(self, download_thread: RequestThread):
        download_thread.status = DownloadStatus.SAVING_DATA
        time.sleep(1)
        if (download_thread.request_type == RequestType.POINTS):
            # TODO:: update private.json with data from this request
            print("Requested Point Data, faking save")
        else:
            self.forecast_to_save = Forecast(download_thread.response_json["properties"])
        save_forecast_data(download_thread.location, download_thread.request_type, self.forecast_to_save)
        time.sleep(1)
        download_thread.status = DownloadStatus.SAVE_COMPLETE
        time.sleep(1)

    def start_download(self, location: Location, forecast_request_type: RequestType):
        self.request_type = forecast_request_type
        print(f"Download Started for ({location.name}) of type ({forecast_request_type.name}).")
        new_download_thread = RequestThread(location, forecast_request_type)
        new_download_thread.name = f'{forecast_request_type}-{location.alias}'
        if threading.active_count() < self.max_thread_count:
            new_download_thread.start()
            self.monitor_download(new_download_thread)
        else:
            raise RuntimeError("Oh shit")
    
    def end_download(self, download_thread: RequestThread):
        if download_thread.status == DownloadStatus.REQUEST_FAILED:
            print(f'{download_thread.request_type.name} for {download_thread.location.name} Failed', download_thread.error_message)
            messagebox.showerror(f'{download_thread.request_type} for {download_thread.location.name} Failed', download_thread.error_message)
    
        if threading.active_count() == 1:
            self.downloadbar["value"] = 100
            self.closebutton = tk.Button(self, text="Close", command=self.close_manager)
            self.closebutton.grid(column=0, row=2)

    def monitor_download(self, download_thread: RequestThread):
        if download_thread.status.value >= self.download_status.value:
            self.download_status = download_thread.status
        progress_count = self.downloadbar["value"]
        for thread in threading.enumerate():
            if isinstance(thread, RequestThread):
                progress_count += (thread.status.value * 10) / DownloadStatus.max_value()
        if threading.active_count() > 1:
            if progress_count > self.downloadbar["value"]:
                self.downloadbar["value"] = round(progress_count / (threading.active_count() - 1))

        if download_thread.is_alive():
            if download_thread.status == DownloadStatus.REQUEST_SUCCESS:
                self.save_download(download_thread)
            log_text = f'({download_thread.location.name}): {download_thread.request_type.name} -> {download_thread.status}\n'
            self.status_text_log.insert(END, log_text)
            self.after(1000, lambda: self.monitor_download(download_thread))
        else:
            self.end_download(download_thread)

    def close_manager(self) -> None:
        widgets = self.grid_slaves()
        for l in widgets:
            l.destroy()
        widgets = None
