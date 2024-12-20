import tkinter as tk

from gui.frames.forecast_request_info import ForecastRequestInfo_LabelFrame
from gui.notebooks.forecast_viewer import ForecastViewer_Notebook

class MainWindow(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title('Project Empyrean')
        self.geometry("800x1200")

        self.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=24)

        request_info = ForecastRequestInfo_LabelFrame(self)
        request_info.grid(column=0, row=0,sticky=tk.NW)
        forecast_viewer = ForecastViewer_Notebook(self)
        forecast_viewer.grid(column=0, row=1, sticky=tk.NSEW)
