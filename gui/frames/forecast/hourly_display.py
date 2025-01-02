"""Contains the logic for displaying an hourly forecast.
"""
import tkinter as tk

from gui.frames.at_a_glance_frame import AtAGlanceFrame
from gui.frames.forecast.forecast_display import ForecastDisplayFrame
from gui.frames.matplotlib_frames.rainchance_frame import RainChanceFrame
from gui.frames.matplotlib_frames.temperature_frame import TemperatureFrame
from utils.structures.forecast.forecast_type import ForecastType
from utils.text_wrapper import format_list_as_line_with_breaks, format_text_as_wrapped


class HourlyDisplayFrame(ForecastDisplayFrame):
    """Extends the ForecastDisplayFrame with relevant information specific
    to an hourly forecast.

    Args:
        ForecastDisplayFrame (ForecastDisplayFrame): The base class and contract
        implemented and extended.
    """
    def __init__(self, master, name, location, at_a_glance: AtAGlanceFrame):
        super().__init__(master, name, location)
        self.at_a_glance = at_a_glance
        self.plots_frame = self.addFrame("plots", row=2, col=0, pady=0, sticky=tk.N)
        self.temperature_frame = TemperatureFrame(
            master=self.plots_frame,
            name="TemperaturePlotContainer",
            plotname="Temperature vs Time",
            row=0,
            col=0
        )
        self.rain_frame = RainChanceFrame(
            master=self.plots_frame,
            name="RainPlotContainer",
            plotname="Rain Chance vs Time",
            row=0,
            col=1
        )

    def __add_content_to_info_display(self) -> None:
        """Adds additional forecast information content to the info display label
        frame.
        """
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
            sticky = tk.W,
            pady=4
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
            sticky = tk.EW,
            pady=4
        )

    def on_hourly_forecast_change(self) -> None:
        """Callback for triggering the creation of visual aides.
        """
        # self._setup_plots_frame()
        self.temperature_frame.prepare_data(self.hourly_forecast.value)
        self.rain_frame.prepare_data(self.hourly_forecast.value)

    def on_extended_forecast_change(self) -> None:
        """Callback for triggering the addition of additional
        forecast information.
        """
        self.__add_content_to_info_display()

    def has_focus(self) -> None:
        """Callback used to trigger the loading of forecast data to enable display
        of widgets to user.
        """
        if self.hourly_forecast.value is None:
            self.hourly_forecast.value = self.try_get_data(ForecastType.HOURLY)
            self.at_a_glance.hourly_forecast.value = self.hourly_forecast.value
        if self.extended_forecast.value is None:
            self.extended_forecast.value = self.try_get_data(ForecastType.EXTENDED)
