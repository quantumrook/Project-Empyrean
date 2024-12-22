from tkinter import ttk

from utils.gridplacement import *
from utils.WidgetEnum import *

class Notebook(ttk.Notebook):

    def __init__(self, container, padding: dict[str, int] = { }, ipadding: dict[str, int] = { }) -> None:
        super().__init__(container)

        self.subframes = { }
        self.current_tab = None
        self.previous_tab = None

        if padding == False:
            padding = self.get_default_padding()
        if ipadding == False:
            ipadding = self.get_default_ipadding()

        options = {k: v for d in (padding, ipadding) for k, v in d.items()}
        self.configure(cnf=options)

        self.bind('<<NotebookTabChanged>>', self.on_tab_change)
        

    def add_frame(self, frame, type: WidgetType, subframe_name: str, frame_title: str, placement: GridPlacement) -> None:
        if subframe_name not in list(self.subframes.keys()):
            self.subframes[subframe_name] = { type: None}
        self.subframes[subframe_name][type] = frame
        self.subframes[subframe_name][type].grid(
            column= placement.col,
            columnspan = placement.span["col"],
            row= placement.row,
            rowspan = placement.span["row"],
            sticky = placement.sticky
        )

        self.add(frame, text=frame_title)

    def on_tab_change(self, event):
        pass
        # print(f'\t\tsuper.on_tab_change')
        # self.previous_tab = self.current_tab
        # self.current_tab = event.widget.tab('current')['text']
        # print(f'\t\t{self.previous_tab=}, {self.current_tab=}')

    def get_default_padding() -> dict[str, int]:
        return { 'padx' : 5, 'pady' : 5}

    def get_default_ipadding() -> dict[str, int]:
        return { 'ipadx' : 5, 'ipady' : 5}

    def add_widget_to_frame(self, widget, frame_name: str, widget_type: WidgetType, widget_name: str, placement: GridPlacement) -> None:
        self.subframes[frame_name].add_widget(
            widget      = widget,
            widget_type = widget_type,
            widget_name = widget_name,
            placement   = placement
        )
