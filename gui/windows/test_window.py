
import TKinterModernThemes as TKMT

from gui.frames.forecast.hourly_display import Hourly_DisplayFrame
from gui.notebooks.forecast_viewer import ForecastViewer_Notebook

from utils.download_manager import ForecastType
from utils.json.forecast import Forecast
from utils.json.private_reader import *
from utils.private import *
from utils.text_wrapper import *



class MainWindow(TKMT.ThemedTKinterFrame):

    locations: list[Location] = [ ]
    current_location_index = -1

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.locations: list[Location] = [ ]
        self.forecasts: dict[str, dict[ForecastType, Forecast]] = { }
        self.load_private_data()

        self.frame = self.addFrame('forecastStuff')
        #self.forecast_hourly_display = Forecast_Hourly_DisplayFrame(self, 'ForecastDisplayClass', None, self.locations[0])
        self.add_forecast_notebook()
        self.run()

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{project_directory_path}\\Project-Empyrean\\utils\\private.json')
        forecasts = None
        for location in self.locations:
            self.forecasts[location.alias] = { }
            for forecast_type in [ForecastType.HOURLY, ForecastType.EXTENDED]:
                self.forecasts[location.alias][forecast_type] = None
        
    def add_forecast_notebook(self) -> None:
        self.forecast_notebook = self.frame.Notebook(
                name = "",
                row = 0,
                col = 0,
                sticky = "nsew"
            )

        self.forecast_notebooks = { }

        forecast_types = [ForecastType.HOURLY, ForecastType.EXTENDED]
        for location in self.locations:
            frame = self.forecast_notebook.addTab(f"{location.name}")
            self.forecast_notebooks[f'{location.alias}'] = frame.Notebook(
                name = f"sub{location.alias}",
                row=0,
                col=0,
                sticky = "nsew"
            )
            for forecast_type in forecast_types:
                subframe = self.forecast_notebooks[f'{location.alias}'].addTab(f"{forecast_type.name.title()}")
                match forecast_type:
                    case ForecastType.HOURLY:
                        hourly_frame = Hourly_DisplayFrame(subframe, 'ForecastDisplayClass', None, location)
                    case ForecastType.EXTENDED:
                        continue

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