"""Creates a Splash Screen to display while program launches.
"""
import tkinter as tk
from gui.icons.icons import png_icons

class SplashScreen(tk.Toplevel):
    """A tkinter window that displays a graphic while the program launches.

    Args:
        tk (Toplevel): The tkinter window class that's extended.
    """
    def __init__(self, master):
        """Creates a window and hides the OS window frame. Loads and displays an image, centered on the user's screen.

        Args:
            master (tk.Toplevel): The program root window.
        """
        super().__init__(master)

        self.overrideredirect(True)
        self.title("Splash Screen")

        x, y = self.__center_window()
        self.geometry(f"1263x995+{x}+{y}")

        self.image = tk.PhotoImage(file=png_icons["splash"]) 
        label = tk.Label(self, image = self.image)
        label.pack()      

        self.update()

    def __center_window(self):
        """Helper function to center this new window in the center of the user's screen.
        """
        self.width = 1263
        self.height = 995

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width/2) - (self.width/2))
        y = int((screen_height/2) - (self.height/2))

        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")