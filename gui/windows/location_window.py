import tkinter as tk
from tkinter import messagebox
import TKinterModernThemes as TKMT

from gui.windows.request_manager import RequestThreadManager_Window
from utils.download.download_status import DownloadStatus
from utils.download.request_type import RequestType
from utils.structures.location.location import Location

class Themed_NewLocation_Window(TKMT.ThemedTKinterFrame):

    def __init__(self, title, root_window, theme = '', mode = '', usecommandlineargs=True, useconfigfile=True):
        super().__init__(title, theme, mode, usecommandlineargs, useconfigfile)

        self.app_root_window = root_window
        self.request_window = None
        self.center_window()
        self.location_details_frame()
        self.lat_lon_frame()

    def center_window(self):
        self.width = 450
        self.height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width/2) - (self.width/2))
        y = int((screen_height/2) - (self.height/2))

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def location_details_frame(self):

        self.alias_var = tk.StringVar()
        self.name_var = tk.StringVar()
        lblFrame = self.addLabelFrame(text="Location Details", row=0, col=0, sticky=tk.EW)

        lblFrame.Label(text="Alias:", row=0, col=0, weight="normal")
        alias_entry = lblFrame.Entry(textvariable=self.alias_var, row=0, col=1)

        lblFrame.Label(text="Display Name", row=1, col=0, weight="normal")
        displayname_entry = lblFrame.Entry(textvariable=self.name_var, row=1, col=1)

    def lat_lon_frame(self):

        self.lattitude_var = tk.StringVar()
        self.longitude_var = tk.StringVar()

        
        lblFrame = self.addLabelFrame(text="By Latitude and Longitude", row=1, col=0, sticky=tk.EW)

        lblFrame.Label(text="Lattitude:", row=0, col=0, weight="normal")
        lat_entry = lblFrame.Entry(textvariable=self.lattitude_var, row=0, col=1)

        lblFrame.Label(text="Longitude", row=1, col=0, weight="normal")
        lon_entry = lblFrame.Entry(textvariable=self.longitude_var, row=1, col=1)

        button = lblFrame.Button(text="Verify", command=self.on_click_verify_button, row=0, rowspan=2, col=2)

    def handleExit(self):
        self.root.destroy()

    def build_location(self):
        self.new_location = Location(
            {
                "alias" : self.alias_var.get(),
                "name"  : self.name_var.get(),
                "position" : {
                    "lattitude" : self.lattitude_var.get(), 
                    "longitude" : self.longitude_var.get()
                    },
                "api_grid" : { 
                    "lastverified" : "",
                    "x" : "",
                    "y" : "",
                    "station" : ""
                },
                "timezone" : ""
            }
        )

    def on_click_verify_button(self):
        self.build_location()

        if self.request_window is None:
            self.request_window = RequestThreadManager_Window()
            self.request_window.location_properties = { 
                Location.Keys.alias : self.alias_var.get(),
                Location.Keys.name : self.name_var.get(),
                Location.Keys.timezone : ""
            }
        else:
            messagebox.showwarning("Download in Progress", "Please wait for the current downloads to finish before trying again.")
            return
        
        print(f'Forecast Request: {RequestType.POINTS} @ {self.new_location.alias}')
        self.request_window.enqueue_download(location=self.new_location, forecast_request_type=RequestType.POINTS)
        self.request_window.monitor_queue()
        self._monitor_requests()

    def _monitor_requests(self):
        if self.request_window.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")

            self.app_root_window.locations.append(self.request_window.updated_location)
            self.request_window.destroy()
            self.request_window = None
            self.app_root_window.add_new_location_tab()
            self.handleExit()
        else:
            self.root.after(1000, self._monitor_requests)