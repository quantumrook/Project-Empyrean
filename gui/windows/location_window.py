import tkinter as tk
import TKinterModernThemes as TKMT

class Themed_NewLocation_Window(TKMT.ThemedTKinterFrame):

    def __init__(self, title, theme = '', mode = '', usecommandlineargs=True, useconfigfile=True):
        super().__init__(title, theme, mode, usecommandlineargs, useconfigfile)

        self.center_window()
        self.lat_lon_frame()

    def center_window(self):
        self.width = 500
        self.height = 300

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width/2) - (self.width/2))
        y = int((screen_height/2) - (self.height/2))

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def lat_lon_frame(self):

        self.latitude_var = tk.StringVar()
        self.longitude_var = tk.StringVar()

        
        lblFrame = self.addLabelFrame(text="By Latitude and Longitude", row=0, col=0, sticky=tk.EW)

        lblFrame.Label(text="Latitude:", row=0, col=0, weight="normal")
        lat_entry = lblFrame.Entry(textvariable=self.latitude_var, row=0, col=1)

        lblFrame.Label(text="Longitude", row=1, col=0, weight="normal")
        lon_entry = lblFrame.Entry(textvariable=self.longitude_var, row=1, col=1)

        button = lblFrame.Button(text="Verify", command=None, row=0, rowspan=2, col=2)