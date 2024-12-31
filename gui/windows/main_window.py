
import tkinter as tk
import TKinterModernThemes as TKMT

from gui.frames.at_a_glance_frame import At_A_Glance_Frame
from gui.frames.control_button_frame import ControlButtons_Frame
from gui.notebooks.location_notebook import Location_Notebook

from utils.private.private import directory_paths
from utils.reader import get_private_data
from utils.structures.location.location import Location


class MainWindow(TKMT.ThemedTKinterFrame):

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.root.geometry("1024x1024")

        self.locations: list[Location] = [ ]
        self.load_private_data()

        self.controlbuttons_frame = ControlButtons_Frame(self.root, "ControlButtonsFrame", self)
        self.at_a_glance_frame = At_A_Glance_Frame(self.root, "AtAGlanceFrame")

        self.frame = self.addFrame('forecastStuff', row=2, col=0, padx=0, pady=10, sticky=tk.NSEW)
        self.location_notebook = Location_Notebook(self.frame, "locationViewer", self.locations, self.at_a_glance_frame)

        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=6)

    def load_private_data(self) -> None:
        self.locations = get_private_data(filename=f'{directory_paths["private"]}\\private.json')