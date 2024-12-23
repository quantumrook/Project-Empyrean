import tkinter as tk

import TKinterModernThemes as TKMT
from utils.json.location import Location

from utils.private import project_directory_path
from utils.json.forecast import Forecast
from utils.json.private_reader import get_test_data
from utils.text_wrapper import *

class Hourly_DisplayFrame(TKMT.WidgetFrame):
    def __init__(self, master, name: str, forecast: Forecast, location: Location):
        super().__init__(master, name)

        self.forecast: Forecast = forecast
        self.location: Location = location

        self.json_data = get_test_data(f'{project_directory_path}\\Project-Empyrean\\utils\\json\\tree_test_forecast.json')
        
        self._setup_info_display()
        self._setup_tree_display()
        self.master.info_frame.makeResizable()

    def _setup_info_display(self) -> None:
        
        forecast_type = self.json_data[0]["forecast_type"].title()

        wrapping_str = format_text_as_wrapped(
            string_to_wrap= self.json_data[0]["info"]["long"],
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
                        f'{self.json_data[0]["info"]["generatedAt"]["date"]} {self.json_data[0]["info"]["generatedAt"]["time"]}',
                        f'{self.json_data[0]["info"]["updateTime"]["date"]} {self.json_data[0]["info"]["updateTime"]["time"]}',
                        f'{self.json_data[0]["info"]["validTimes"]["date"]} {self.json_data[0]["info"]["validTimes"]["time"]}'
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
        self.master.info_frame.Treeview(
                columnnames     = ['By Date and Time', 'Forecast'], 
                columnwidths    = [2, 5], 
                height          = 10,
                data            = self.json_data,
                subentryname    = 'subdata',
                datacolumnnames = ['name', 'value'],
                openkey         = 'open',
                row= 2,
                col= 0,
                colspan = 2,
                rowspan = 1,
                sticky = tk.EW
            )
        