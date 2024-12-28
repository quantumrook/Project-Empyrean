from typing import Any
import TKinterModernThemes as TKMT

from PIL import Image, ImageTk

from gui.icons.icons import icons


class ControlButtons_Frame():

    def __init__(self, master, frame: TKMT.WidgetFrame, commands: dict[str, Any]):
        self.frame = frame
        self.master = master


        self.frame.Label(text="", col=0)
        
        images = { }
        for icon_name, icon_path in icons.items():
            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.Resampling.LANCZOS)
            images[icon_name] = ImageTk.PhotoImage(img)

        col_counter = 1
        self.buttons = { }
        for name, img in images.items():
            button = self.frame.Button("", commands[name], row=0, col=col_counter, widgetkwargs={"image" : img, "name" : name})
            button.image = img
            col_counter += 1

            self.buttons[name] = button
        
        self.frame.master.columnconfigure(0, weight=80)
        self.frame.master.columnconfigure(1, weight=10)
        self.frame.master.columnconfigure(2, weight=10)




    def toggle_download_button_state(self, new_state):
        self.buttons["download"]['state'] = new_state