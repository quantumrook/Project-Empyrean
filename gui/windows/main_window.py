import tkinter as tk
from tkinter import ttk

from gui.frames.forecast_alert_info import ForecastAlertInfo_LabelFrame
from gui.frames.forecast_request_info import ForecastRequestInfo_LabelFrame
from gui.notebooks.forecast_viewer import ForecastViewer_Notebook

class MainWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()

        # self.style = ttk.Style(self)
        # self.style.configure('TLabelframe.Label', font=('Tahoma', 14))
        # self.style.configure('TLabel', font=('Tahoma', 12))

        self.title('Project Empyrean')
        self.geometry("800x1200")

        self.set_default_style()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=24)

        request_info = ForecastRequestInfo_LabelFrame(self)
        request_info.grid(column=0, row=0,sticky=tk.NW)

        alert_info = ForecastAlertInfo_LabelFrame(self)
        alert_info.grid(column=1, row=0,sticky=tk.NW)

        forecast_viewer = ForecastViewer_Notebook(self)
        forecast_viewer.grid(column=0, columnspan=2, row=1, sticky=tk.NSEW)

    def set_default_style(self):
        self.style = ttk.Style(self)
        self.style.configure('.',                   font=('Tahmoa', 10))
        self.style.configure('TLabelframe.Label',   font=('Tahoma', 12))
        self.style.configure('TNotebook.Tab',       font=('Tahoma', 12))