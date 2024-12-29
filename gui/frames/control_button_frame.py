from typing import Any
import TKinterModernThemes as TKMT
import tkinter as tk
from PIL import Image, ImageTk
import tksvg
from gui.icons.icons import png_icons, svg_icons
from gui.windows.location_window import NewLocation_Window


class ControlButtons_Frame():

    def __init__(self, master, frame: TKMT.WidgetFrame, commands: dict[str, Any], root):
        
        self.app_root = root
        
        self.frame = frame
        self.master = master
        self.buttons = { }

        self.buttons["location"] = self.frame.Button("Add Location", self.on_location_click, col=0)
        self.frame.Label(text="", col=1)
        
        images = { }
        for icon_name, icon_path in png_icons.items():
            img = Image.open(icon_path)
            img = img.resize((36, 36), Image.Resampling.LANCZOS)
            images[icon_name] = ImageTk.PhotoImage(img)

        col_counter = 2
        
        for name, img in images.items():
            if name == "splash":
                continue
            # if name == 'download':
            #     cloud = self.convert_svg()
            #     button = self.frame.Button("", commands[name], row=0, col=col_counter, widgetkwargs={"image" : cloud, "name" : name})            
            #     button.image = cloud
            # else:
            button = self.frame.Button("", commands[name], row=0, col=col_counter, widgetkwargs={"image" : img, "name" : name})            
            button.image = img
            col_counter += 1

            self.buttons[name] = button
        
        self.frame.master.columnconfigure(0, weight=20)
        self.frame.master.columnconfigure(1, weight=60)
        self.frame.master.columnconfigure(2, weight=10)
        self.frame.master.columnconfigure(3, weight=10)


    def convert_svg(self):
        svg_image = tksvg.SvgImage(file= svg_icons["wi-cloud-down"], scaletoheight=36)
        return svg_image


    def toggle_download_button_state(self, new_state):
        self.buttons["download"]['state'] = new_state

    def on_location_click(self):
        self.location_window = NewLocation_Window(self.app_root)