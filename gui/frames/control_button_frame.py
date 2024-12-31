from tkinter import messagebox
import TKinterModernThemes as TKMT
from PIL import Image, ImageTk
import tksvg
from gui.icons.icons import png_icons, svg_icons
from gui.windows.location_window import Themed_NewLocation_Window
from gui.windows.request_manager import RequestThreadManager_Window
from utils.download.download_status import DownloadStatus
from utils.download.request_type import RequestType
from utils.structures.datetime import TODAY, EmpyreanDateTime


class ControlButtons_Frame(TKMT.WidgetFrame):

    def __init__(self, master, name, main_window):
        super().__init__(master, name)
        self.main_window = main_window
        self.frame = self.addFrame(name='cb_frame', row=0, col=0, padx=0, pady=0)
        self.buttons = { }

        self.buttons["location"] = self.frame.Button("Add Location", self.on_location_click, col=0)
        self.frame.Label(text="", col=1)
        
        images = { }
        for icon_name, icon_path in png_icons.items():
            img = Image.open(icon_path)
            img = img.resize((36, 36), Image.Resampling.LANCZOS)
            images[icon_name] = ImageTk.PhotoImage(img)

        col_counter = 2
        
        commands = {
            "popout" : self._on_click_get_markdown,
            "download" : self._on_click_get_forecast
        }

        for name, img in images.items():
            if name == "splash":
                continue
            # if name == 'download':
            #     cloud = self.convert_svg()
            #     button = self.frame.Button("", commands[name], row=0, col=col_counter, widgetkwargs={"image" : cloud, "name" : name})            
            #     button.image = cloud
            # else:
            button = self.frame.Button("", commands[name], row=0, col=col_counter, widgetkwargs={"image" : img, "name" : name})            
            button.image = img
            col_counter += 1

            self.buttons[name] = button
        
        self.frame.master.columnconfigure(0, weight=20)
        self.frame.master.columnconfigure(1, weight=60)
        self.frame.master.columnconfigure(2, weight=10)
        self.frame.master.columnconfigure(3, weight=10)

        self.request_window = None

    def convert_svg(self):
        svg_image = tksvg.SvgImage(file= svg_icons["wi-cloud-down"], scaletoheight=36)
        return svg_image

    #TODO :: Reimplement the disabling of the download button if we already have today's forecast
    def toggle_download_button_state(self, new_state):
        self.buttons["download"]['state'] = new_state

    def on_location_click(self):
        self.location_window = Themed_NewLocation_Window("Add a new location", self.root_window)

    def _on_click_get_markdown(self):
        print("Not implemented yet!")

    def _on_click_get_forecast(self):
        active_location = self.main_window.location_notebook.active_location.value
        if self.__points_is_valid() == False:

            self.request_window = RequestThreadManager_Window()
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
                self.request_window = RequestThreadManager_Window()

            print(f'Forecast Request: {request_type.value} @ {active_location.alias}')
            self.request_window.enqueue_download(location=active_location, forecast_request_type=request_type)

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