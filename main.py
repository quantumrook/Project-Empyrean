import time
import gui.windows.main_window as mw
import tkinter as tk

from gui.windows.splash_window import SplashScreen
from gui.windows.at_a_glance import AtAGlance

if __name__ == "__main__":

    app = AtAGlance("park", "dark")
    app.run()

    # app = mw.MainWindow("park", "dark")
    # app.root.withdraw()

    # splashscreen = SplashScreen(master=app.root, background="white")
    
    # #TODO :: Replace with thread so we can load in the background
    # time.sleep(1)
    # while splashscreen.attributes('-alpha') > 0:
    #     current_alpha = splashscreen.attributes('-alpha')
    #     splashscreen.attributes('-alpha', (current_alpha - 0.05))
    #     splashscreen.update()
    #     time.sleep(0.05)

    # app.root.deiconify()
    # splashscreen.destroy()
    # app.run()