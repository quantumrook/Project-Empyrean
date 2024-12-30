import time
import gui.windows.main_window as mw
import tkinter as tk

import cProfile
from pstats import Stats, SortKey

from gui.windows.splash_window import SplashScreen

if __name__ == "__main__":


    # with cProfile.Profile() as pr:
        # app = AtAGlance("park", "dark")
        # app.run()

        app = mw.MainWindow("park", "dark")
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
        app.run()

    # with open('profiling_stats.txt', "w") as stream:
    #     stats = Stats(pr, stream=stream)
    #     stats.strip_dirs()
    #     stats.sort_stats('time')
    #     stats.dump_stats('.prof_stats')
    #     stats.print_stats()