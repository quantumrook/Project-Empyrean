from typing import Any
import TKinterModernThemes as TKMT

from PIL import Image, ImageTk

from gui.icons.icons import icons


class ControlButtons_Frame():

    def __init__(self, master, frame: TKMT.WidgetFrame, commands: dict[str, Any]):
        self.frame = frame
        self.frame.master = master
        images = { }
        for icon_name, icon_path in icons.items():
            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.Resampling.LANCZOS)
            images[icon_name] = ImageTk.PhotoImage(img)

        row_counter = 0
        self.buttons = { }
        for name, img in images.items():
            button = self.frame.Button("", commands[name], row=0, col=row_counter, widgetkwargs={"image" : img, "name" : name})
            button.image = img
            row_counter += 1

            self.buttons[name] = button



    def toggle_download_button_state(self, new_state):
        self.buttons["download"]['state'] = new_state