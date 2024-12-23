from decimal import ROUND_UP
from re import I
import tkinter as tk
from tkinter import ttk

import TKinterModernThemes as TKMT
from utils.json.location import Location

from utils.private import project_directory_path
from utils.json.forecast import Forecast
from utils.json.private_reader import get_test_data

class Forecast_DisplayFrame(TKMT.WidgetFrame):
    def __init__(self, master, name: str, forecast: Forecast, location: Location):
        super().__init__(master, name)

        self.forecast: Forecast = forecast
        self.location: Location = location

        self.json_data = get_test_data(f'{project_directory_path}\\Project-Empyrean\\utils\\json\\tree_test_forecast_3.json')
        
        self._setup_info_display()
        self._setup_tree_display()     
    
    def _wrap_detailed_forecast(self, detailed: str) -> str:

        characters_per_row = 80
        number_of_rows = round(len(detailed)/characters_per_row)

        wrapping_string = '    '
        for char_row_i in range(0, number_of_rows):
            if char_row_i == 0:
                col_end_early_count = 4
                col_start_early_count = 0
            else:
                col_start_early_count = 0
                col_end_early_count = 0
            over_fill = ''
            row = ''
            start_of_last_word = False
            end_of_last_word = False
            for char_col_i in range(col_start_early_count, characters_per_row - col_end_early_count):
                index = char_col_i + char_row_i * characters_per_row
                if index < len(detailed):     
                    if characters_per_row - char_col_i <= 6:
                        if detailed[index] == ' ' and start_of_last_word == False:
                            start_of_last_word = True
                            row += detailed[index]
                        elif detailed[index] == ' ' and start_of_last_word == True:
                            end_of_last_word = True
                            row += detailed[index]
                        elif end_of_last_word == True:
                            over_fill += detailed[index]
                        else:
                            row += detailed[index]
                    else:
                        row += detailed[index]
                else:
                    break
            wrapping_string += row + '\n' + over_fill

        return wrapping_string

    def _check_for_upcoming_white_space(self, line, index, characters_per_row):
        overfill = ''
        for i in range(0,characters_per_row-index):
            if len(line) < index + i:
                overfill += line[index+i]
                if line[index+i] == ' ':
                    overfill += ' '
                    return (True, overfill)
        return (False, '')

    def _setup_info_display(self) -> None:
        info_frame_content = [ ]   
        info_frame_content.append(f'Generated At: {self.json_data[0]["info"]["generatedAt"]["date"]} {self.json_data[0]["info"]["generatedAt"]["time"]}\n')
        info_frame_content.append(f'Last Updated: {self.json_data[0]["info"]["updateTime"]["date"]} {self.json_data[0]["info"]["updateTime"]["time"]}\n')
        info_frame_content.append(f'Valid Till: {self.json_data[0]["info"]["validTimes"]["date"]} {self.json_data[0]["info"]["validTimes"]["time"]}\n')

        detailed_forecast = self.json_data[0]["info"]["longWOB"]
        wrapping_str = self._wrap_detailed_forecast(detailed_forecast)

        info_frame_content.append(f'\n{self.json_data[0]["info"]["short"]}:\n{wrapping_str}\n\n\t{self.json_data[0]["info"]["longWB"]}')

        info_frame_content_as_str = ''
        for line in info_frame_content:
            info_frame_content_as_str += line

        self.master.info_frame = self.master.addLabelFrame(f"InfoFrame")
        self.master.info_frame.Text(text=info_frame_content_as_str)

    def _setup_tree_display(self) -> None:

        forecast_type = self.json_data[0]["forecast_type"].title()

        self.master.tree_frame = self.master.addLabelFrame(f"{self.location.name}'s {forecast_type} Forecast")
        
        self.treeview_widget = self.master.tree_frame.Treeview(
                columnnames     = ['By Date and Time', 'Forecast'], 
                columnwidths    = [100, 300], 
                height          = 10,
                data            = self.json_data,
                subentryname    = 'subdata',
                datacolumnnames = ['name', 'value'],
                openkey         = 'open',
            )
        