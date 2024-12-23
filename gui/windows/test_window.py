from functools import partial
from tkinter import font
import TKinterModernThemes as TKMT
import json
from gui.frames.forecast_display import Forecast_DisplayFrame


from utils.json.forecast import Forecast, ForecastData

from utils.private import *
from utils.json.private_reader import *


class MainWindow(TKMT.ThemedTKinterFrame):

    locations: list[Location] = [ ]
    current_location_index = -1

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.locations: list[Location] = [ ]
        self.load_private_data()

        self.treeview_widget = [ ]

        self.frame = self.addFrame('forecastStuff')
        forecast_display = Forecast_DisplayFrame(self, 'ForecastDisplayClass', None, self.locations[0])

        self.json_data = get_test_data(f'{project_directory_path}\\Project-Empyrean\\utils\\json\\tree_test_forecast_3.json')
        
        self.run()

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{project_directory_path}\\Project-Empyrean\\utils\\private.json')
    
    def example_tree(self, tree_data):
        self.frame = self.addLabelFrame(f'Package Example')

        self.treeview_widget.append(self.frame.Treeview(
                columnnames     = ['Files', 'Purpose'], 
                columnwidths    = [120, 120], 
                height          = 10,
                data            = tree_data,
                subentryname    = 'subfiles',
                datacolumnnames = ['name', 'purpose'],
                openkey         = 'open',
            )
        )

    def tree_two(self):
        tree_data = get_test_data(f'{project_directory_path}\\Project-Empyrean\\utils\\json\\tree_test_forecast_3.json')
        forecast_type = tree_data[0]["forecast_type"].title()       
        self.frame = self.addLabelFrame(f"<Location> {forecast_type}")
        
        self.treeview_widget.append(self.frame.Treeview(
                columnnames     = ['By Date and Time', 'Forecast'], 
                columnwidths    = [60, 180], 
                height          = 10,
                data            = tree_data,
                subentryname    = 'subdata',
                datacolumnnames = ['name', 'value'],
                openkey         = 'open',
            ))   
    
    def _setup_info_display(self) -> None:
        info_frame_content = [ ]   
        info_frame_content.append(f'Generated At: {self.json_data[0]["info"]["generatedAt"]["date"]} {self.json_data[0]["info"]["generatedAt"]["time"]}\n')
        info_frame_content.append(f'Last Updated: {self.json_data[0]["info"]["updateTime"]["date"]} {self.json_data[0]["info"]["updateTime"]["time"]}\n')
        info_frame_content.append(f'Valid Till: {self.json_data[0]["info"]["validTimes"]["date"]} {self.json_data[0]["info"]["validTimes"]["time"]}\n')
        
        info_frame_content_as_str = ''
        for line in info_frame_content:
            info_frame_content_as_str += line

        print("Creating frame")
        self.frame.info_frame = self.frame.addLabelFrame(f"InfoFrame")
        self.frame.info_frame.Text(text=info_frame_content_as_str)
        print("Done")

    def _setup_tree_display(self) -> None:

        forecast_type = self.json_data[0]["forecast_type"].title()

        print("Creating Tree Frame")
        self.frame.tree_frame = self.frame.addLabelFrame(f"{self.location.name}'s {forecast_type} Forecast")
        print("Creating Tree")
        self.treeview_widget = self.frame.tree_frame.Treeview(
                columnnames     = ['By Date and Time', 'Forecast'], 
                columnwidths    = [100, 300], 
                height          = 10,
                data            = self.json_data,
                subentryname    = 'subdata',
                datacolumnnames = ['name', 'value'],
                openkey         = 'open',
            )
        print("DOne")