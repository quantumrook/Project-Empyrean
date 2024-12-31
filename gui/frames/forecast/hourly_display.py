import tkinter as tk

from gui.frames.at_a_glance_frame import At_A_Glance_Frame
from gui.frames.forecast.forecast_display import Forecast_DisplayFrame
from utils.structures.datetime import TODAY
from utils.structures.forecast.forecast_type import ForecastType
from utils.text_wrapper import format_list_as_line_with_breaks, format_text_as_wrapped


class Hourly_DisplayFrame(Forecast_DisplayFrame):

    def __init__(self, master, name, location, at_a_glance: At_A_Glance_Frame):
        super().__init__(master, name, location)
        self.at_a_glance = at_a_glance
    
    def __add_content_to_info_display(self) -> None:
        self.info_frame.Label(
            text=format_list_as_line_with_breaks(
                list_to_compress= [
                        self.extended_forecast.value.frontmatter.generated.as_string(),
                        self.extended_forecast.value.frontmatter.updated.as_string(),
                        self.extended_forecast.value.frontmatter.expiration.as_string()
                    ],
                add_tab_spacing= False
            ),
            weight="normal",
            size= 10,
            row= 1,
            col= 1,
            colspan = 1,
            rowspan = 1,
            sticky = tk.W
        )
        summary = ""
        for entry in self.extended_forecast.value.forecasts[0:1]:
            summary += entry.content.description.long.get_value()

        wrapping_str = format_text_as_wrapped(
            string_to_wrap= summary,
            add_tab= True,
            number_of_characters_per_line= 160 #TODO :: calculate based of frame width
        )
        
        self.info_frame.Label(
            text=wrapping_str,
            weight="normal",
            size= 10,
            row= 0,
            col= 0,
            colspan = 2,
            rowspan = 1,
            sticky = tk.EW
        )

    def on_hourly_forecast_change(self) -> None:
        self._setup_plots_frame()

    def on_extended_forecast_change(self) -> None:
        self.__add_content_to_info_display()

    @staticmethod
    def __calculate_windchill(temperature: int, wind_speed: int) -> int:
        if temperature >= 50 or wind_speed == 0:
            return temperature
        windchill = round(35.74+(0.6215*temperature)-(35.75*pow(wind_speed, 0.16))+(0.4275*temperature*pow(wind_speed, 0.16)))
        if windchill > temperature:
            return temperature #TODO Check why this is necessary
        return windchill

    def _setup_plots_frame(self) -> None:
        is_first_hour = True
        every_four_hours = [ ]
        hours = [ ]
        temps = [ ]
        windchills = [ ]
        rain = [ ]
        for forecast in self.hourly_forecast.value.forecasts:
            if forecast.start.date == TODAY.date:
                hour = int(forecast.start.hour().split(":")[0])
                if hour > 0 and is_first_hour:
                        every_four_hours.append(hour)
                        is_first_hour = False
                if hour % 4 == 0:
                    every_four_hours.append(hour)
                hours.append(hour)
                temp = int(forecast.content.temperature.get_value())
                temps.append(temp)
                rain.append(int(forecast.content.rainChance.get_value()))
                chill = self.__calculate_windchill(temp, forecast.content.wind.speedHigh.get_value())
                windchills.append(chill)


        self.temperatureframe = self.info_frame.addLabelFrame("Temperature vs Time", row=2, col=0)
        self.temperature_canvas, fig1, self.temperature_ax, background, self.accent = self.temperatureframe.matplotlibFrame("Temperature vs Time")

        self.temperature_ax.plot(hours, windchills)
        self.temperature_ax.plot(hours, temps, c='white')
        self.temperature_ax.legend(['Windchill', 'Temperature'])

        self.temperature_ax.set_xticks(every_four_hours)
        self.temperature_ax.set_ylabel(u'\N{DEGREE SIGN}'+'F')
        
        self.rainframe = self.info_frame.addLabelFrame("Rain Chance vs Time", row=2, col=1)
        self.rain_canvas, fig2, self.rain_ax, _, _ = self.rainframe.matplotlibFrame("Rain Chance vs Time")
        self.rain_ax.set_ylabel("Rain Chance %")
        self.rain_ax.set_xticks(every_four_hours)
        self.rain_ax.plot(hours, rain, c=self.accent)

    def has_focus(self) -> None:
        if self.hourly_forecast.value is None:
            self.hourly_forecast.value = self.try_get_data(ForecastType.HOURLY)
            self.at_a_glance.hourly_forecast.value = self.hourly_forecast.value
        if self.extended_forecast.value is None:
            self.extended_forecast.value = self.try_get_data(ForecastType.EXTENDED)

