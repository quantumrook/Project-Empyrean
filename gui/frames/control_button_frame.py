"""Contains the logic for the control buttons displayed at the top
of the main window for user interaction.
"""
from tkinter import messagebox
import TKinterModernThemes as TKMT
from PIL import Image, ImageTk
import tksvg
from gui.icons.icons import png_icons, svg_icons
from gui.windows.location_window import NewLocationWindow
from gui.windows.request_manager import RequestThreadManagerWindow
from utils.download.download_status import DownloadStatus
from utils.download.request_type import RequestType
from utils.structures.datetime import TODAY, EmpyreanDateTime


class ControlButtonsFrame(TKMT.WidgetFrame):
    """Creates a TKMT WidgetFrame to contain and organize the buttons.

    Args:
        TKMT (WidgetFrame): TKMT base class that is extended.
    """
    def __init__(self, master, name, main_window):
        super().__init__(master, name)
        self.main_window = main_window
        self.frame = self.addFrame(name='cb_frame', row=0, col=0, padx=0, pady=0, gridkwargs={"ipadx":0, "ipady":0})
        # self.frame.master['borderwidth'] = 1
        # self.frame.master['relief'] = 'solid'
        self.buttons = { }

        self.buttons["location"] = self.frame.Button("Add Location", self.on_location_click, col=0, sticky="ns", padx=0, pady=4, gridkwargs={"ipadx":0, "ipady":0})
        self.frame.Label(text="", col=1)

        images = { }
        for icon_name, icon_path in png_icons.items():
            img = Image.open(icon_path)
            img = img.resize((42, 42), Image.Resampling.LANCZOS)
            images[icon_name] = ImageTk.PhotoImage(img)

        col_counter = 2

        commands = {
            "popout" : self._on_click_get_markdown,
            "download" : self._on_click_get_forecast
        }

        for name, img in images.items():
            if name == "splash":
                continue
            button = self.frame.Button(
                "",
                commands[name],
                row=0,
                col=col_counter,
                widgetkwargs={"image" : img, "name" : name},
                gridkwargs={"ipadx" : 0, "ipady": 0},
                padx=4,
                pady=4,
                sticky="n"
            )
            button.image = img
            col_counter += 1

            self.buttons[name] = button

        # self.frame.master.rowconfigure(0, minsize=100, weight=1)

        self.frame.master.columnconfigure(0, minsize=100, weight=20)
        self.frame.master.columnconfigure(1, minsize=(1024-300), weight=60)
        self.frame.master.columnconfigure(2, minsize=50, weight=10)
        self.frame.master.columnconfigure(3, minsize=50, weight=10)

        self.request_window = None

    def convert_svg(self):
        """Helper function to load and convert a svg to be a button image.
        """
        svg_image = tksvg.SvgImage(file= svg_icons["wi-cloud-down"], scaletoheight=36)
        return svg_image

    #TODO :: Reimplement the disabling of the download button if we already have today's forecast
    def toggle_download_button_state(self, new_state):
        """Callback used to enable or disable the download button depending on
        if the user already has today's forecast for the current active location.

        Args:
            new_state (str): the state of the button.
        """
        self.buttons["download"]['state'] = new_state

    def on_location_click(self):
        """Event function for spawning the NewLocationWindow.
        """
        self.location_window = NewLocationWindow("Add a new location", self.main_window)

    def _on_click_get_markdown(self):
        print("Not implemented yet!")

    def _on_click_get_forecast(self):
        """Event function used to spawn and queue up requests to the RequestThreadManager
        to enable fetching of forecasts.
        """
        active_location = self.main_window.location_notebook.active_location.value
        if not self.__points_is_valid():

            self.request_window = RequestThreadManagerWindow()
            print(f'Forecast Request: {RequestType.POINTS.value} @ {active_location.alias}')
            self.request_window.enqueue_download(active_location, RequestType.POINTS)

            #TODO :: Add in option to bypass points request anyways?

        for request_type in [RequestType.HOURLY, RequestType.EXTENDED]:
            hourly_tab = self.main_window.location_notebook.location_tabs[active_location.name].hourly_tab
            extended_tab = self.main_window.location_notebook.location_tabs[active_location.name].extended_tab
            if hourly_tab.hourly_forecast.value is not None and extended_tab.extended_forecast.value is not None:
                #TODO :: Display a message?
                messagebox.showinfo("Forecast Information", "You already have today's forecast.")
                continue
            # TODO:: Check if the forecast is still valid

            if self.request_window is None:
                self.request_window = RequestThreadManagerWindow()

            print(f'Forecast Request: {request_type.value} @ {active_location.alias}')
            self.request_window.enqueue_download(
                location=active_location,
                forecast_request_type=request_type
            )

        if self.request_window is not None:
            self.request_window.monitor_queue()
            self._monitor_requests()

    def _monitor_requests(self):
        if self.request_window.download_status == DownloadStatus.SAVE_COMPLETE:
            print("Save Complete - Displaying data.")

            self.request_window.destroy()
            self.request_window = None
            self.main_window.location_notebook.trigger_refresh()
        else:
            self.frame.master.after(1000, self._monitor_requests)

    def __points_is_valid(self) -> bool:
        active_location = self.main_window.location_notebook.active_location.value
        date = active_location.api_grid.lastverified
        last_verified = EmpyreanDateTime.from_Empyrean({
            EmpyreanDateTime.Keys.time_zone : active_location.timezone,
            EmpyreanDateTime.Keys.date : date,
            EmpyreanDateTime.Keys.time : "01:00"
        })
        return EmpyreanDateTime.is_in_range(
                questionable_datetime=TODAY,
                starting_datetime=last_verified,
                ending_datetime=EmpyreanDateTime.add_days(last_verified, 14)
        )
