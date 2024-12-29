import tkinter as tk

class NewLocation_Window(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.app_root = master
        self.title("Add a new Location")
        
        self.center_window()
        self.lat_lon_frame()
        


    def center_window(self):
        self.width = 400
        self.height = 300

        screen_width = self.app_root.winfo_screenwidth()
        screen_height = self.app_root.winfo_screenheight()
        x = int((screen_width/2) - (self.width/2))
        y = int((screen_height/2) - (self.height/2))

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def lat_lon_frame(self):

        self.latitude_var = tk.StringVar()
        self.longitude_var = tk.StringVar()

        lblFrame = tk.LabelFrame(self, text="By Latitude and Longitude")
        lblFrame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.EW)

        tk.Label(lblFrame, text="Latitude:").grid(row=0, column=0)
        lat_entry = tk.Entry(lblFrame, textvariable=self.latitude_var)
        lat_entry.grid(row=0, column=1)

        tk.Label(lblFrame, text="Longitude:").grid(row=1, column=0)
        lon_entry = tk.Entry(lblFrame, textvariable=self.longitude_var)
        lon_entry.grid(row=1, column=1)

        button = tk.Button(lblFrame, text="Verify")
        button.grid(row=0, rowspan=2, column=2)