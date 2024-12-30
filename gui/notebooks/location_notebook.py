
import TKinterModernThemes as TKMT
import tkinter as tk
from gui.notebooks.forecast_notebook import Forecast_Notebook
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable

class Location_Notebook(TKMT.WidgetFrame):

    def __init__(self, master, name, locations: list[Location]):
        super().__init__(master, name)

        self.locations = locations

        self.active_location = WatchedVariable()
        self.active_location.value = None
        self.active_location.on_change = self.on_location_change

        self.notebook = self.master.Notebook(name, row=0, col=0, sticky=tk.NSEW, padx=0, pady=0)
        self.notebook.notebook.name = name

        self.hourly_tab = None
        self.extended_tab = None
        
        self.is_first_view = True

        self.location_tabs = { }

        self.add_new_location_tab()
        self.notebook.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def add_new_location_tab(self):
        for location in self.locations:
            frame = self.notebook.addTab(location.name)
            forecastviews = Forecast_Notebook(frame, f"sub{location.alias}", location)
            self.location_tabs[location.name] = forecastviews

        
    def on_tab_change(self, event):
        print(event.widget.name, self.notebook.name)

        for location in self.locations:
            if event.widget.tab('current')['text'] == location.name:
                self.active_location.value = location
        print(event.widget.tab('current')['text'])

    def on_location_change(self):
        print("activating sub tab")
        self.location_tabs[self.active_location.value.name].active.value = True