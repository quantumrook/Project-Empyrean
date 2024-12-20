from enum import Enum
from msilib.schema import ComboBox
from tkinter import CHECKBUTTON, RADIOBUTTON

class WidgetType(Enum):
    BUTTON          = 0
    CANVAS          = 1
    CHECKBUTTON     = 2
    COMBOBOX        = 3
    ENTRY           = 4
    LABEL           = 5
    LISTBOX         = 6
    MENU            = 7
    MENUBUTTON      = 8
    RADIOBUTTON     = 9
    SCALE           = 10
    SCROLLBAR       = 11
    TEXT            = 12
    FRAME           = 13

    @classmethod
    def list(cls) -> list:
        """
        Returns all of the widget types as a list.
        
        Source: https://stackoverflow.com/a/54919285
        """
        return list(map(lambda c: c.value, cls))
