"""Container for the At a Glance view.
"""
import tkinter as tk

import TKinterModernThemes as TKMT
from PIL import Image, ImageTk
from gui.icons.icons import clock_icons
from utils.structures.datetime import TODAY
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.watched_variable import WatchedVariable


class AtAGlanceFrame(TKMT.WidgetFrame):
    """Creates a TKMT WidgetFrame to hold widgets that correspond to 
    the "At a glance" view and manages their updates.

    Args:
        TKMT (WidgetFrame): The TKMT class that is extended.
    """
    def __init__(self, master, name):
        super().__init__(master, name)
        self.frame = self.addLabelFrame("At a Glance", row=1, padx=0, pady=0, sticky=tk.NSEW, gridkwargs={"ipadx":0, "ipady":0})
        self.frame.master['borderwidth'] = 5
        self.frame.master['relief'] = 'solid'

        self.hourly_forecast = WatchedVariable()
        self.hourly_forecast.on_change = self.update_display

        self.clocks = None
        self.load_graphics()

        self.hour_progressbar = None
        self.clock_labels = [ ]
        self.build_at_a_glance()

    def update_display(self):
        """Callback for adding information once the hourly forecast has been loaded.
        """
        self.add_temp_labels()

    def load_graphics(self):
        """Helper function to load in graphics.
        """
        self.clocks = [ ]
        for i in range(1,13):
            img = Image.open(clock_icons[f'wi-time-{i}'])
            img = img.resize((48,48), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            if i < 12:
                self.clocks.append(img)
            else:
                self.clocks.insert(0, img)

    def build_at_a_glance(self):
        """Helper function to add in the initial widgets that don't need forecast
        information.
        """
        just_hour = tk.IntVar()
        hour = int(TODAY.hour())
        just_hour.set(hour)
        self.hour_progressbar = self.frame.Progressbar(just_hour, mode='determinate', lower=5, upper=18, row=1, col=1, colspan=12, padx=10, pady=0)

        for col in range(6,18):
            hour_normalized = col
            if hour_normalized > 11:
                hour_normalized -= 12
            clock_lbl = self.frame.Label(f"", widgetkwargs={"image" : self.clocks[hour_normalized]}, row=0, col=(col-5), padx=5, pady=5)
            self.clock_labels.append(clock_lbl)

    def add_temp_labels(self):
        """Helper function to add in widgets that do need forecast information.
        """
        temps = { }
        short = { }
        forecast_data: EmpyreanForecast = self.hourly_forecast.value
        for forecast in forecast_data.forecasts: # pylint: disable=E1101
            if forecast.start.date == TODAY.date:
                temps[forecast.start.time] = forecast.content.temperature.get_value()
                short[forecast.start.time] = forecast.content.description.short.get_value()

        #TODO check if labels already exist, if they do, just update.

        for time, temp in temps.items():
            hour = int(time.split(":")[0])
            if hour >= 6 and hour <= 17:
                temp_lbl = self.frame.Label(text=str(temp), row=2, col=(hour-5))
                # short_lbl = self.at_a_glance_frame.Label(text=short[time], row=3, col=(hour-5), size=10)

    # def build_animation(self):
    #     self.animation_data = { }
    #     hourly: EmpyreanForecast = None
    #     for location, forecast_type in self.display_frames.items():
    #         if location == self.active_location.alias:
    #             for forecast_type, frame in self.display_frames[location].items():
    #                 if forecast_type == ForecastType.HOURLY:
    #                     hourly = frame.hourly_forecast
    #     if hourly is None:
    #         return

    #     clocks = [ ]
    #     for i in range(1,13):
    #         img = Image.open(clock_icons[f'wi-time-{i}'])
    #         img = img.resize((48,48), Image.Resampling.LANCZOS)
    #         img = ImageTk.PhotoImage(img)
    #         if i < 12:
    #             clocks.append(img)
    #         else:
    #             clocks.insert(0, img)

    #     low = 273
    #     high = -273
    #     earliest_hour = 23
    #     for forecast in hourly.forecasts:
    #         if forecast.start.date == TODAY.date:
    #             temp = int(forecast.content.temperature.get_value())
    #             if temp < low:
    #                 low = temp
    #             if temp > high:
    #                 high = temp
    #             hour = int(forecast.start.hour())
    #             if hour < earliest_hour:
    #                 earliest_hour = hour
    #             if hour > 11:
    #                 hour -= 12
    #             self.animation_data[forecast.start.time] = {
    #                 "img"  : clocks[hour],
    #                 "temp" : forecast.content.temperature.get_value(),
    #                 "rain" : forecast.content.rainChance.get_value()
    #             }
    #     self.animation_current_key = list(self.animation_data.keys())[0]
    #     self.anim_clock_lbl = self.at_a_glance_frame.Label(text="", row=0, col=0, widgetkwargs={"image" : self.animation_data[self.animation_current_key]["img"]})

    #     self.anim_prog_var = tk.IntVar()
    #     self.anim_prog_var.set(earliest_hour)
    #     self.anim_prog_bar = self.at_a_glance_frame.Progressbar(self.anim_prog_var, mode="determinate", lower=earliest_hour, upper=len(self.animation_data.keys()), row=1, col=0)

    #     self.anim_temp_var = tk.StringVar()
    #     self.anim_temp_var.set(self.animation_data[self.animation_current_key]["temp"])
    #     self.anim_temp_lbl = self.at_a_glance_frame.Label(text="", row=2, col=0, widgetkwargs={"textvariable" : self.anim_temp_var})

    # def play_animation(self):

    #     if (self.is_playing == False):
    #         self.is_playing = True
    #     keys = list(self.animation_data.keys())
    #     index = keys.index(self.animation_current_key) + 1
    #     if index == len(keys):
    #         index = 0
    #     self.animation_current_key = keys[index]

    #     self.anim_prog_var.set(int(self.animation_current_key.split(":")[0]))
    #     img = self.animation_data[self.animation_current_key]["img"]
    #     self.anim_clock_lbl.configure(image=img)
    #     self.anim_clock_lbl.image = img
    #     self.anim_temp_var.set(self.animation_data[self.animation_current_key]["temp"])
    #     self.root.update()
    #     self.root.after(1000, self.play_animation)