
import TKinterModernThemes as TKMT

from gui.frames.forecast.extended_display import Extended_DisplayFrame
from gui.frames.forecast.hourly_display import Hourly_DisplayFrame
from utils.structures.forecast.forecast_type import ForecastType
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable

class Forecast_Notebook(TKMT.WidgetFrame):

    def __init__(self, master, name, location: Location):
        super().__init__(master, name)

        self.notebook = self.master.Notebook(name)
        self.notebook.notebook.name = name
        self.location = location
        self.display_frames = {
            ForecastType.HOURLY : None,
            ForecastType.EXTENDED : None
        }
        self.hourly_tab = None
        self.extended_tab = None

        self.active_tab = WatchedVariable()
        self.active_tab.value = None
        self.active_tab.on_change = self.active_tab_changed

        self.active = WatchedVariable()
        self.active.value = False
        self.active.on_change = self.has_focus

        self.is_first_view = True
        self.notebook.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def has_focus(self):
        if self.active.value == False:
            return
        if self.is_first_view:
            self.hourly_tab = self.notebook.addTab(ForecastType.HOURLY.value.title())
            self.extended_tab = self.notebook.addTab(ForecastType.EXTENDED.value.title())
            self.hourly_tab = Hourly_DisplayFrame(self.hourly_tab.master, f'{self.location.alias}HourlyDisplayFrame', self.location)       
            self.extended_tab = Extended_DisplayFrame(self.extended_tab.master, f'{self.location.alias}ExtendedDisplayFrame', self.location)
            self.is_first_view = False
            
    def active_tab_changed(self):
        if self.active_tab.value == ForecastType.HOURLY.value.title():
            self.hourly_tab.has_focus()
        if self.active_tab.value == ForecastType.EXTENDED.value.title():
            self.extended_tab.has_focus()
            
    def on_tab_change(self, event):
        if event.widget.name == self.notebook.name:
            self.active_tab.value = event.widget.tab('current')['text']
        else:
            self.active.value = False
            self.active_tab.value = None
