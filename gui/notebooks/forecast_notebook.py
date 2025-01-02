"""Contains logic for creating a TKMT themed tkinter notbook widget to hold
forecast information for a given location.
"""
import TKinterModernThemes as TKMT

from gui.frames.at_a_glance_frame import AtAGlanceFrame
from gui.frames.forecast.extended_display import ExtendedDisplayFrame
from gui.frames.forecast.hourly_display import HourlyDisplayFrame
from utils.structures.forecast.forecast_type import ForecastType
from utils.structures.location.location import Location
from utils.structures.watched_variable import WatchedVariable

class ForecastNotebook(TKMT.WidgetFrame):
    """Creates a (TKMT themed) tkinter notebook widget, whose tabs are the types of forecasts.

    Args:
        TKMT (WidgetFrame): The TKMT class that is extended.
    """
    def __init__(self, master, name, location: Location, at_a_glance: AtAGlanceFrame):
        super().__init__(master, name)

        self.at_a_glance = at_a_glance

        self.notebook = self.master.Notebook(name, row=1, col=0, padx=0, pady=0)
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
        """Callback used to trigger delayed creation of children frames for each tab.
        """
        if not self.active.value:
            return
        if self.is_first_view:
            self.hourly_tab = self.notebook.addTab(ForecastType.HOURLY.value.title())
            self.extended_tab = self.notebook.addTab(ForecastType.EXTENDED.value.title())
            self.hourly_tab = HourlyDisplayFrame(
                self.hourly_tab.master,
                f'{self.location.alias}HourlyDisplayFrame',
                self.location,
                self.at_a_glance
            )
            self.extended_tab = ExtendedDisplayFrame(
                self.extended_tab.master,
                f'{self.location.alias}ExtendedDisplayFrame',
                self.location
            )
            self.is_first_view = False

    def active_tab_changed(self):
        """Callback used for notifying the corresponding display frame that it is
        currently visible.
        """
        if self.active_tab.value == ForecastType.HOURLY.value.title():
            self.hourly_tab.has_focus()
        if self.active_tab.value == ForecastType.EXTENDED.value.title():
            self.extended_tab.has_focus()

    def on_tab_change(self, event):
        """Event listener for when the forecast tab changes. Updates the reference to the 
        current active forecast to enable callbacks to execute.

        Args:
            event : tkinter <<NotebookTabChanged>> event that has been triggered.
        """
        if event.widget.name == self.notebook.name:
            self.active_tab.value = event.widget.tab('current')['text']
        else:
            self.active.value = False
            self.active_tab.value = None
