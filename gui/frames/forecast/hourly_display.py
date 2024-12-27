import tkinter as tk

import TKinterModernThemes as TKMT
from utils.download.request_type import RequestType
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.forecast.forecast_type import ForecastType
from utils.structures.location.location import Location
from utils.text_wrapper import *


class Hourly_DisplayFrame(TKMT.WidgetFrame):
    def __init__(self, master, name: str, hourly: EmpyreanForecast, extended: EmpyreanForecast, location: Location, control_buttons: dict[str, tk.Button]):
        super().__init__(master, name)

        self.hourly_forecast: EmpyreanForecast = hourly
        self.extended_forecast: EmpyreanForecast = extended
        self.location: Location = location
        self.control_buttons = control_buttons
        
        if hourly is not None and extended is not None:
            self._setup_info_display()
            self._setup_tree_display()
            self.master.info_frame.makeResizable()

        

    def _setup_info_display(self) -> None:

        summary = ""
        for entry in self.extended_forecast.forecasts[0:1]:
            summary += f" {entry.content.description.long.get_value()}"

        wrapping_str = format_text_as_wrapped(
            string_to_wrap= summary,
            add_tab= True,
            number_of_characters_per_line= 160
        )

        self.master.info_frame = self.master.addFrame("")
        self.master.info_frame.Label(
            text=format_list_as_line_with_breaks(
                list_to_compress= [
                        "Generated At:", 
                        "Last Updated:", 
                        "Valid Till:"
                    ],
                add_tab_spacing= False
            ),
            weight= "normal",
            size= 10,
            row= 0,
            col= 0,
            colspan = 1,
            rowspan = 1,
            sticky = tk.E
        )
        
        self.master.info_frame.Label(
            text=format_list_as_line_with_breaks(
                list_to_compress= [
                        f'{self.hourly_forecast.frontmatter.generated.as_string()}',
                        f'{self.hourly_forecast.frontmatter.updated.as_string()}',
                        f'{self.hourly_forecast.frontmatter.expiration.as_string()}'
                    ],
                add_tab_spacing= False
            ),
            weight="normal",
            size= 10,
            row= 0,
            col= 1,
            colspan = 1,
            rowspan = 1,
            sticky = tk.W
        )

        self.master.info_frame.Label(
            text=wrapping_str,
            weight="normal",
            size= 10,
            row= 1,
            col= 0,
            colspan = 2,
            rowspan = 1,
            sticky = tk.E
        )

    def _setup_tree_display(self) -> None:
        tree_dict = self.hourly_forecast.to_hourly_tree_dict()
        one_fifth = round(768 / 5)
        four_fifths = 768-one_fifth
        self.master.info_frame.Treeview(
                columnnames     = ['By Date and Time', 'Forecast'], 
                columnwidths    = [one_fifth, four_fifths], 
                height          = 18,
                data            = tree_dict,
                subentryname    = 'subdata',
                datacolumnnames = ['name', 'value'],
                openkey         = 'open',
                row= 2,
                col= 0,
                colspan = 2,
                rowspan = 1,
                sticky = tk.EW
            )
    
    def refresh(self) -> None:
        self._setup_info_display()
        self._setup_tree_display()
        self.master.info_frame.makeResizable()