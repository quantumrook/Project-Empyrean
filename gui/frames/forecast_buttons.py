import tkinter as tk

from gui.empyrean.labelframe import LabelFrame
from gui.icons.icons import icons
from gui.widget_enum import WidgetType
from PIL import Image, ImageTk
from utils.structures.grid_placement import GridPlacement
from utils.structures.location.location import Location


class ForecastButtons_LabelFrame(LabelFrame):

    def __init__(self, container, location: Location) -> None:
        super().__init__(container)
        self._title = ""
        self.location = location

        self.__add_content()
        self.get_buttons()

    def __add_content(self):
        images = { }
        for icon_name, icon_path in icons.items():
            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.Resampling.LANCZOS)
            images[icon_name] = ImageTk.PhotoImage(img)

        row_counter = 0
        for name, img in images.items():
            self.add_widget(
                widget= tk.Button(self, image=img),
                widget_type= WidgetType.BUTTON,
                widget_name= name.title(),
                placement= GridPlacement(col=0, row = row_counter, span={"col":1, "row":1}, sticky=tk.NSEW)
            )
            self.widgets[WidgetType.BUTTON][name.title()].image = img
            row_counter += 1

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def get_buttons(self) -> dict[str, tk.Button]:
        return self.widgets[WidgetType.BUTTON]
    