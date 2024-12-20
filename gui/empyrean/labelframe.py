import tkinter.ttk as ttk
from tkinter import messagebox

from utils.gridplacement import *
from utils.WidgetEnum import *

class LabelFrame(ttk.Labelframe):

    container = None
    widgets = { }
    display_label_vars = { }

    def __init__(self, container, padding: dict[str, int] = { }, ipadding: dict[str, int] = { }, title: str = '' ) -> None:
        super().__init__(container)

        self.container = container

        for widget_type in WidgetType.list():
            self.widgets[widget_type] = { }
        
        if padding == False:
            padding = self.get_default_padding()
        if ipadding == False:
            ipadding = self.get_default_ipadding()

        options = {k: v for d in (padding, ipadding) for k, v in d.items()}
        self.configure(cnf=options)
        self.update_title(title)
        
    def get_default_padding() -> dict[str, int]:
        return { 'padx' : 5, 'pady' : 5}

    def get_default_ipadding() -> dict[str, int]:
        return { 'ipadx' : 5, 'ipady' : 5}

    def add_widget(self, widget, widget_type: WidgetType, widget_name: str, placement: GridPlacement) -> None:
        self.widgets[widget_type.value][widget_name] = widget
        self.widgets[widget_type.value][widget_name].grid(
            column= placement.col,
            columnspan = placement.span["col"],
            row= placement.row,
            rowspan = placement.span["row"],
            sticky = placement.sticky
        )

    def update_title(self, new_title: str)-> None:
        self.configure(text=new_title)

    def update_label(self, label_alias: str, new_text: str)->None:
        if label_alias in list(self.display_label_vars.keys()):
            self.display_label_vars[label_alias].set(new_text)
        else:
            messagebox.showerror("Error:", f"Tried to update a text label with the wrong name or it doesn't exist.\n{label_alias=}\nPossible matches: {list(self.display_label_vars.keys())}")

    def update_labels(self, label_aliases: list[str], new_text: list[str]) -> None:
        for label_alias, text in zip(label_aliases, new_text):
            if label_alias in list(self.display_label_vars.keys()):
                self.display_label_vars[label_alias].set(text)
            else:
                messagebox.showerror("Error:", f"Tried to update a text label with the wrong name or it doesn't exist.\n{label_alias=}\nPossible matches: {list(self.display_label_vars.keys())}")
