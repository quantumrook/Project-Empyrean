import tkinter as tk

from PIL import Image, ImageTk
import TKinterModernThemes as TKMT
from gui.icons.icons import clock_icons
from utils.structures.datetime import TODAY

class AtAGlance(TKMT.ThemedTKinterFrame):

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Project Empyrean - At a Glance", theme, mode, usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        x, y = self.centerWindow(1024, 768)
        self.root.geometry(f"1024x768+{x}+{y}")

        self.build_glance_container()


    def centerWindow(self, width, height):  # Return 4 values needed to center Window
        screen_width = self.root.winfo_screenwidth()  # Width of the screen
        screen_height = self.root.winfo_screenheight() # Height of the screen     
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        return int(x), int(y)

    def build_glance_container(self):
        self.containing_lblFrame = self.addLabelFrame("At A Glance:", sticky=tk.NSEW)

        clocks = self.__get_clocks()        

        current_hour = int(TODAY.hour())
        for col in range(0,12):
            hour_normalized = current_hour + col
            if hour_normalized > 11:
                hour_normalized -= 12
            clock_lbl = self.containing_lblFrame.Label(f"", widgetkwargs={"image" : clocks[hour_normalized]}, row=0, col=col)



    def __get_clocks(self):
        clocks = [ ]
        for i in range(1,13):
            img = Image.open(clock_icons[f'wi-time-{i}'])
            img = img.resize((48,48), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            if i < 12:
                clocks.append(img)
            else:
                clocks.insert(0, img)
        return clocks