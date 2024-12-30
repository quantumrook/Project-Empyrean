import tkinter as tk
from gui.icons.icons import png_icons

class SplashScreen(tk.Toplevel):

    def __init__(self, master, background):
        super().__init__(master, background=background)

        self.overrideredirect(True)
        self.title("Splash Screen")

        x, y = self.centerWindow(1263, 995, master)
        self.geometry(f"1263x995+{x}+{y}")

        self.image = tk.PhotoImage(file=png_icons["splash"]) 
        label = tk.Label(self, image = self.image)
        label.pack()      

        self.update()

    def centerWindow(self, width, height, root):  # Return 4 values needed to center Window
        screen_width = root.winfo_screenwidth()  # Width of the screen
        screen_height = root.winfo_screenheight() # Height of the screen     
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        return int(x), int(y)
