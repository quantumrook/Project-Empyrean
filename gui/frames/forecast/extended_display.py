import tkinter as tk

from gui.frames.forecast.forecast_display import Forecast_DisplayFrame
from utils.structures.forecast.forecast_type import ForecastType
from utils.structures.location.location import Location
from utils.text_wrapper import *


class Extended_DisplayFrame(Forecast_DisplayFrame):
    def __init__(self, master, name: str, location: Location):
        super().__init__(master, name, location)
        self.treeview = None

    def __add_content_to_info_display(self):
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

    def _setup_tree_display(self) -> None:
        tree_dict = self.extended_forecast.value.to_extended_tree_dict()
        one_fifth = round(800 / 5) #TODO Replace hardcoded width
        four_fifths = 800-one_fifth
        self.treeview = self.info_frame.Treeview(
                columnnames     = ['By Date and Time', 'Forecast'], 
                columnwidths    = [one_fifth, four_fifths], 
                height          = 20,
                data            = tree_dict,
                subentryname    = 'subdata',
                datacolumnnames = ['name', 'value'],
                openkey         = 'open',
                row= 0,
                col= 0,
                colspan = 2,
                rowspan = 1,
                sticky = tk.EW
            )
    
    def on_extended_forecast_change(self):
        self.__add_content_to_info_display()
        if self.treeview is None:
            self._setup_tree_display()
        #TODO : Else, update the data

    def has_focus(self) -> None:
        if self.extended_forecast.value is None:
            self.extended_forecast.value = self.try_get_data(ForecastType.EXTENDED)
