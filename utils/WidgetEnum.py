from enum import Enum, auto

class WidgetType(Enum):
    BUTTON          = auto()
    CANVAS          = auto()
    CHECKBUTTON     = auto()
    COMBOBOX        = auto()
    ENTRY           = auto()
    LABEL           = auto()
    LISTBOX         = auto()
    MENU            = auto()
    MENUBUTTON      = auto()
    RADIOBUTTON     = auto()
    SCALE           = auto()
    SCROLLBAR       = auto()
    TEXT            = auto()
    FRAME           = auto()
    LABELFRAME      = auto()

    @classmethod
    def list(cls) -> list:
        """
        Returns all of the widget types as a list.

        Source: https://stackoverflow.com/a/54919285
        """
        return list(map(lambda c: c.value, cls))
