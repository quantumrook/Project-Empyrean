"""Module responsible for spawning RequestThreads to query the NWS API.

Raises:
    RuntimeError: Error raised if too many threads were to be spawned to prevent a situation 
    where it could possibly spam the API.
"""
import threading
import tkinter as tk
from tkinter import END, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from utils.download.download_status import DownloadStatus
from utils.download.request_thread import RequestThread
from utils.download.request_type import RequestType
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable


class RequestThreadManagerWindow(tk.Toplevel):
    """A tkinter styled window that displays the current request thread status to the user as 
    each request is processed.

    Args:
        tk (Toplevel): the tkinter window module.

    Raises:
        RuntimeError: Error raised if too many threads were to be spawned to prevent a situation 
        where it could possibly spam the API. Threshold is
    specified by the `max_thread_count` variable.
    """
    max_thread_count = 5
    queue: list[RequestThread] = [ ]

    stepsize: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.wm_title("Download Status")

        self.forecast_to_save:   EmpyreanForecast = None
        self.request_type:       RequestType = RequestType.POINTS
        self.download_status:    DownloadStatus = DownloadStatus.INSTANTIATING

        self.updated_location = WatchedVariable()
        self.updated_location.value = None

        self.status_text_log = ScrolledText(self)
        self.status_text_log.grid(column=0, row=0)

        self.downloadbar = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            length=200
        )
        self.downloadbar.grid(column=0, row=1)

        self.stepsize = round(100 / DownloadStatus.max_value())

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        self.number_of_requests = 0

    def monitor_POINTS_location(self, points_request_thread: RequestThread):
        """Listener function called when we're updating the POINTS data and have 
        hourly/extended forecasts queued up as well.

        Args:
            points_request_thread (RequestThread): the POINTs thread that has finished processing
        """
        self.updated_location.value = points_request_thread.new_location.value

    def enqueue_download(self, location: Location, forecast_request_type: RequestType):
        """Creates a RequestThread for the given request type and adds it to the queue.

        Args:
            location (Location): The location to query about.
            forecast_request_type (RequestType): The type of API request to perform.
        """
        self.request_type = forecast_request_type
        print(f"Download Started for ({location.name}) of type ({forecast_request_type.value}).") #TODO: save to a log?

        new_download_thread = RequestThread(location, forecast_request_type)
        new_download_thread.name = f'{forecast_request_type}-{location.alias}'
        new_download_thread.status.on_change = lambda: self.__monitor_thread_status(
            new_download_thread)

        if forecast_request_type == RequestType.POINTS:
            new_download_thread.new_location.on_change = lambda: self.monitor_POINTS_location(
                new_download_thread)

        self.number_of_requests += 1
        self.queue.append(new_download_thread)

    def end_download(self, download_thread: RequestThread):
        """In the event that a request was denied by the API, handle displaying 
        information to the user.

        Args:
            download_thread (RequestThread): The thread that has finished the request process.
        """
        if download_thread.status == DownloadStatus.REQUEST_FAILED:
            messagebox.showerror(
                f'{download_thread.request_type} for {download_thread.location.name} Failed',
                download_thread.error_message
            )

    def __monitor_thread_status(self, download_thread: RequestThread):
        """Listener called when each RequestThread's .status property is changed. Updates the UI 
        Progress bar and text log to keep user informed.

        Args:
            download_thread (RequestThread): The thread whose status has changed.
        """
        progress_count = self.downloadbar["value"]
        progress_count += round(self.stepsize / self.number_of_requests )
        if threading.active_count() > 1:
            if progress_count > self.downloadbar["value"]:
                self.downloadbar["value"] = progress_count

        self.status_text_log.insert(
            END, 
            f"({download_thread.location.name}).{download_thread.request_type.value.title()}: {download_thread.status.value.name.title()}\n"
        )
        self.monitor_download(download_thread)

    def monitor_queue(self):
        """Function responsible for popping the next RequestThread from the queue. Current 
        implementation only permits one forecast type request to execute at a time.

        Raises:
            RuntimeError: Forces an exception if the current number of threads exceeds the 
            `number_of_requests` originally queued up. Safeguard to prevent runaway spawning.
        """
        current_thread_count = 0
        currently_updating_location = False

        for thread in threading.enumerate():
            if isinstance(thread, RequestThread):
                if thread.request_type == RequestType.POINTS:
                    currently_updating_location = True
                current_thread_count += 1
        if current_thread_count > self.number_of_requests:
            raise RuntimeError("Forcing Exception - too many threads tried to execute.")

        #TODO :: Allow Hourly and Extended to download simultaneously?

        if not currently_updating_location and len(self.queue) > 0:
            new_download_thread = self.queue.pop(0)
            new_download_thread.start()
            new_download_thread.new_location.on_change = lambda: new_download_thread.update_location_with_new_POINTS_data(self.updated_location)
            self.monitor_download(new_download_thread)
        elif len(self.queue) == 0:
            self.download_status = DownloadStatus.SAVE_COMPLETE
            self.downloadbar["value"] = 100
            self.closebutton = tk.Button(self, text="Close", command=self.close_manager)
            self.closebutton.grid(column=0, row=2)

    def monitor_download(self, download_thread: RequestThread):
        """Callback used to tell the Manager to check about spawning a new thread.

        Args:
            download_thread (RequestThread): the thread that has either a failed request or 
            completed saving the data.
        """
        if download_thread.status.value == DownloadStatus.SAVE_COMPLETE:
            self.monitor_queue()
        else:
            self.end_download(download_thread)
        

    def close_manager(self) -> None:
        """Handler for closing the window when all threads are complete. Destroys all 
        widgets and itself.
        """
        widgets = self.grid_slaves()
        for l in widgets:
            l.destroy()
        widgets = None
        self.destroy()
