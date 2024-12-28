import tkinter as tk

import TKinterModernThemes as TKMT
from utils.structures.forecast.empyrean.forecast import EmpyreanForecast
from utils.structures.location.location import Location
from utils.text_wrapper import *


class Extended_DisplayFrame(TKMT.WidgetFrame):
    def __init__(self, master, name: str, hourly: EmpyreanForecast, extended: EmpyreanForecast, location: Location):
        super().__init__(master, name)

        self.is_stale = {
            "hourly" : False,
            "extended" : False
        }

        self.hourly_forecast = None
        self.extended_forecast = None
        
        self.location: Location = location
        
        self.master.info_frame = self.master.addFrame("")
        self.master.info_frame.makeResizable()

        self.treeview = None

        #self.update(hourly, extended)
        

    def _setup_info_display(self) -> None:

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
            row= 1,
            col= 0,
            colspan = 1,
            rowspan = 1,
            sticky = tk.E
        )
        
        self.master.info_frame.Label(
            text=format_list_as_line_with_breaks(
                list_to_compress= [
                        f'{self.extended_forecast.frontmatter.generated.as_string()}',
                        f'{self.extended_forecast.frontmatter.updated.as_string()}',
                        f'{self.extended_forecast.frontmatter.expiration.as_string()}'
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
        tree_dict = self.extended_forecast.to_extended_tree_dict()
        one_fifth = round(768 / 5)
        four_fifths = 768-one_fifth
        self.master.info_frame.Treeview(
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
    
    def refresh(self) -> None:
        if self.is_stale["hourly"]:
            # if self.treeview is not None:
            #     self.treeview.destroy()
            self._setup_tree_display()
        
        if self.is_stale["extended"]:
            # widgets = self.master.info_frame.widgets
            # for l in widgets:
            #     l.destroy()
            # widgets = None
            self._setup_info_display()
            
    def update_hourly(self, hourly: EmpyreanForecast) -> None:
        if hourly is None:
            return
        self.hourly_forecast = hourly
        self.is_stale["hourly"] = True

    def update_extended(self, extended: EmpyreanForecast) -> None:
        if extended is None:
            return
        self.extended_forecast = extended
        self.is_stale["extended"] = True

    def update(self, hourly: EmpyreanForecast, extended: EmpyreanForecast) -> None:
        self.update_hourly(hourly)
        self.update_extended(extended)
        self.refresh()