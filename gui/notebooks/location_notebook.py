
import TKinterModernThemes as TKMT
import tkinter as tk
from gui.frames.at_a_glance_frame import At_A_Glance_Frame
from gui.notebooks.forecast_notebook import Forecast_Notebook
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable

class Location_Notebook(TKMT.WidgetFrame):

    def __init__(self, master, name, locations: list[Location], at_a_glance: At_A_Glance_Frame):
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

        self.add_new_location_tab(at_a_glance)
        self.notebook.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def add_new_location_tab(self, at_a_glance):
        for location in self.locations:
            frame = self.notebook.addTab(location.name)
            forecastviews = Forecast_Notebook(frame, f"sub{location.alias}", location, at_a_glance)
            self.location_tabs[location.name] = forecastviews

    def trigger_refresh(self):
        self.location_tabs[self.active_location.value.name].active_tab_changed()
        
    def on_tab_change(self, event):
        for location in self.locations:
            if event.widget.tab('current')['text'] == location.name:
                self.active_location.value = location

    def on_location_change(self):
        self.location_tabs[self.active_location.value.name].active.value = True