"""Module that provides the root window for Project-Empyrean"""
import tkinter as tk
import TKinterModernThemes as TKMT

from gui.frames.at_a_glance_frame import AtAGlanceFrame
from gui.frames.control_button_frame import ControlButtonsFrame
from gui.notebooks.location_notebook import LocationNotebook

from utils.private.private import directory_paths
from utils.reader import get_private_data
from utils.structures.location.location import Location


class MainWindow(TKMT.ThemedTKinterFrame):
    """The Main Window class for Project-Empyrean. Extends the TkinterModernThemes base window frame.

    Args:
        TKMT (ThemedTKinterFrame): the base class from TkinterModernThemes to be extended
    """

    def __init__(self, theme: str, mode: str, usecommandlineargs=True, usethemeconfigfile=True):
        """Instantiates the extended TKMT WidgetFrames that hold the UI Components.

        Args:
            theme (str): Specifies the theme that TKMT should use.
            mode (str): Specifies either light or dark mode for the corresponding theme.
            usecommandlineargs (bool, optional): Additional args for initializing the TKMT Root Window. Defaults to True.
            usethemeconfigfile (bool, optional): Specifies if TKMT should use the config file for the declared theme. Defaults to True.
        """
        super().__init__(
            "Project Empyrean",
            theme,
            mode,
            usecommandlineargs=usecommandlineargs,
            useconfigfile=usethemeconfigfile
        )

        self.root.geometry("1024x1024")

        self.locations: list[Location] = [ ]
        self.load_private_data()

        self.controlbuttons_frame = ControlButtonsFrame(self.root, "ControlButtonsFrame", self)
        self.at_a_glance_frame = AtAGlanceFrame(self.root, "AtAGlanceFrame")

        self.forecast_frame = self.addFrame('forecastStuff', row=2, col=0, padx=0, pady=0, sticky=tk.NSEW, gridkwargs={"ipadx":0, "ipady":0})
        self.location_notebook = LocationNotebook(
            self.forecast_frame,
            "locationViewer",
            self.locations,
            self.at_a_glance_frame
        )

        r1=70
        r2=160
        self.root.rowconfigure(0, minsize=r1)
        self.root.rowconfigure(1, minsize=r2)
        self.root.rowconfigure(2, minsize=(1024-r1-r2))

    def load_private_data(self) -> None:
        """Loads in any `Location` that is currently saved to private.json. 
        This corresponds to any locations that the user has specified while running the app through the "Add a Location" button workflow.
        """
        self.locations = get_private_data(
            filename=f'{directory_paths["private"]}\\private.json'
        )
