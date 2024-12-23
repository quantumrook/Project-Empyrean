import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from utils.gridplacement import *
from utils.WidgetEnum import *

class LabelFrame(ttk.Labelframe):

    def __init__(self, container, padding: dict[str, int] = { }, ipadding: dict[str, int] = { }, title: str = '' ) -> None:
        super().__init__(container)

        self.container = container
        self.subframes = { }
        self.widgets = { }
        self.display_label_vars = { }

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
        return { 'padx' : (5,5), 'pady' : (5,5)}

    def get_default_ipadding() -> dict[str, int]:
        return { 'ipadx' : (5,5), 'ipady' : (5,5)}

    def add_widget(self, widget, widget_type: WidgetType, widget_name: str, placement: GridPlacement) -> None:
        if widget_type not in self.widgets.keys():
            self.widgets[widget_type] = { }
        self.widgets[widget_type][widget_name] = widget
        self.widgets[widget_type][widget_name].grid(
            column= placement.col,
            columnspan = placement.span["col"],
            row= placement.row,
            rowspan = placement.span["row"],
            sticky = placement.sticky
        )

    def add_changing_Label(self, widget, widget_type: WidgetType, widget_name: str, placement: GridPlacement, variable_string: tk.StringVar, wrap_text: bool) -> None:
        if widget_type not in self.widgets.keys():
            self.widgets[widget_type] = { }
        self.display_label_vars[widget_name] = variable_string
        self.widgets[widget_type][widget_name] = widget
        self.widgets[widget_type][widget_name].grid(
            column= placement.col,
            columnspan = placement.span["col"],
            row= placement.row,
            rowspan = placement.span["row"],
            sticky = placement.sticky,
            padx=5,
            pady=5
        )
    
    def add_frame(self, frame, type: WidgetType, name: str, placement: GridPlacement) -> None:
        if name not in list(self.subframes.keys()):
            self.subframes[name] = { type: None}
        self.subframes[name][type] = frame
        self.subframes[name][type].grid(
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
