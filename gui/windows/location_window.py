"""Provides the logic and object for users to add a new location to the program"""
import tkinter as tk
from tkinter import messagebox
import TKinterModernThemes as TKMT

from gui.windows.request_manager import RequestThreadManagerWindow
from utils.download.download_status import DownloadStatus
from utils.download.request_type import RequestType
from utils.structures.location.location import Location

class NewLocationWindow(TKMT.ThemedTKinterFrame):
    """An extended TKMT Window for querying information from the user to add a new location to the program. Performs a POINTS request from the NWS 
    API to fill in the required missing information.
    """

    def __init__(self, title, root_window, theme = '', mode = '',
                 usecommandlineargs=True, useconfigfile=True):
        """Creates the window used to capture Latitude and Longitude information about the location the user would like to receive forecasts for.

        Args:
            title (str): The title of the window.
            root_window (ThemedTKinterFrame): The program's root window, used to pass information back.
            theme (str, optional): The window's theme, if not supplied, defaults to the current active theme (from instantiating the root window)
            mode (str, optional): The light or dark parameter for the theme, defaults to current active mode (from the root window) if omitted.
            usecommandlineargs (bool, optional): Additional arguments for instantiation, Defaults to True.
            useconfigfile (bool, optional): Specifies whether to use the built in config theme file. Defaults to True.
        """
        super().__init__(title, theme, mode, usecommandlineargs, useconfigfile)

        self.main_window = root_window
        self.request_window = None
        self.new_location = None # TODO:: change to watched variable?
        self.__center_window()
        self.__location_details_frame()
        self.__lat_lon_frame()

    def __center_window(self):
        """Helper function to center this new window in the center of the user's screen
        """
        self.width = 450
        self.height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width/2) - (self.width/2))
        y = int((screen_height/2) - (self.height/2))

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def __location_details_frame(self):
        """A container for the Labels and Entries used to obtain the location's
        alias and tab display name.
        """
        self.alias_var = tk.StringVar()
        self.name_var = tk.StringVar()
        lbl_frame = self.addLabelFrame(text="Location Details", row=0, col=0, sticky=tk.EW)

        lbl_frame.Label(text="Alias:", row=0, col=0, weight="normal")
        lbl_frame.Entry(textvariable=self.alias_var, row=0, col=1)

        lbl_frame.Label(text="Display Name", row=1, col=0, weight="normal")
        lbl_frame.Entry(textvariable=self.name_var, row=1, col=1)

    def __lat_lon_frame(self):
        """A container for the Labels and Entries used to obtain the location's
        latitude and longitude
        """
        self.latitude_var = tk.StringVar()
        self.longitude_var = tk.StringVar()

        lbl_frame = self.addLabelFrame(text="By Latitude and Longitude", row=1, col=0, sticky=tk.EW)

        lbl_frame.Label(text="Latitude:", row=0, col=0, weight="normal")
        lbl_frame.Entry(textvariable=self.latitude_var, row=0, col=1)

        lbl_frame.Label(text="Longitude", row=1, col=0, weight="normal")
        lbl_frame.Entry(textvariable=self.longitude_var, row=1, col=1)

        lbl_frame.Button(text="Verify", command=self.__on_click_verify_button, row=0, rowspan=2, col=2)

    def handleExit(self):
        """The method called when the window is to be closed.
        """
        self.root.destroy()

    def __build_location(self):
        """Helper function to construct a new Location object from user input."""
        self.new_location = Location(
            {
                "alias" : self.alias_var.get(),
                "name"  : self.name_var.get(),
                "position" : {
                    "latitude" : self.latitude_var.get(), 
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

    def __on_click_verify_button(self):
        """Builds a location based off user input and queries the NWS API with a POINTS request to fill in the required information to execute forecast 
        requests.
        """
        self.__build_location()

        if self.request_window is None:
            self.request_window = RequestThreadManagerWindow()
            self.request_window.location_properties = {
                Location.Keys.alias : self.alias_var.get(),
                Location.Keys.name : self.name_var.get(),
                Location.Keys.timezone : ""
            }
        else:
            messagebox.showwarning("Download in Progress",
                "Please wait for the current downloads to finish before trying again.")
            return

        print(f'Forecast Request: {RequestType.POINTS} @ {self.new_location.alias}')
        self.request_window.enqueue_download(location=self.new_location, forecast_request_type=RequestType.POINTS)
        self.request_window.monitor_queue()
        self._monitor_requests()

    def _monitor_requests(self):
        if self.request_window.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")

            self.main_window.locations.append(self.request_window.updated_location.value)
            self.main_window.location_notebook.trigger_refresh()
            self.request_window.destroy()
            self.request_window = None
            self.handleExit()
        else:
            self.root.after(1000, self._monitor_requests)
