import tkinter as tk

import TKinterModernThemes as TKMT
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.location.location import Location
from utils.text_wrapper import *


class Extended_DisplayFrame(TKMT.WidgetFrame):
    def __init__(self, master, name: str, hourly: EmpyreanForecast, extended: EmpyreanForecast, location: Location):
        super().__init__(master, name)

        self.hourly_forecast: EmpyreanForecast = hourly
        self.extended_forecast: EmpyreanForecast = extended
        self.location: Location = location
        
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
            number_of_characters_per_line= 80
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
        tree_dict = self.hourly_forecast.to_extended_tree_dict()
        self.master.info_frame.Treeview(
                columnnames     = ['By Date and Time', 'Forecast'], 
                columnwidths    = [2, 5], 
                height          = 10,
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
        