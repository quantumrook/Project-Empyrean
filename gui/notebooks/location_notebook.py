"""Contains the logic for creating a TKMT themed tkinter notebook widget.
"""
import tkinter as tk

import TKinterModernThemes as TKMT

from gui.frames.at_a_glance_frame import AtAGlanceFrame
from gui.notebooks.forecast_notebook import ForecastNotebook
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable

class LocationNotebook(TKMT.WidgetFrame):
    """Creates the tkinter notebook widget, whose tabs are user specified locations.

    Args:
        TKMT (WidgetFrame): The TKMT class that is extended.
    """
    def __init__(self, master, name, locations: list[Location], at_a_glance: AtAGlanceFrame):
        super().__init__(master, name)

        self.at_a_glance = at_a_glance
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

        self.__add_new_location_tab()
        self.notebook.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def __add_new_location_tab(self):
        """Helper function for creating a new tab for each location.

        Args:
            at_a_glance (AtAGlanceFrame): Container for the "At a Glance" widgets. The reference
            is passed down to the forecast notebook
            that is instatiated on the location's tab.
        """
        for location in self.locations:
            if location.name in list(self.location_tabs.keys()):
                continue
            frame = self.notebook.addTab(location.name)
            forecastviews = ForecastNotebook(frame, f"sub{location.alias}", location, self.at_a_glance)
            self.location_tabs[location.name] = forecastviews
            if self.active_location.value is None:
                self.active_location.value = location

    def trigger_refresh(self):
        """Callback used to notify that the current tab has changed.
        """
        self.__add_new_location_tab()
        self.location_tabs[self.active_location.value.name].active_tab_changed()

    def on_tab_change(self, event):
        """Event listener for when the location tab changes. Updates the reference to the current
        active location to enable callbacks
        to execute.

        Args:
            event : tkinter <<NotebookTabChanged>> event that has been triggered.
        """
        for location in self.locations:
            if event.widget.tab('current')['text'] == location.name:
                self.active_location.value = location

    def on_location_change(self):
        """Callback used to tell the corresponding forecast notebook that it is now active.
        """
        self.location_tabs[self.active_location.value.name].active.value = True
