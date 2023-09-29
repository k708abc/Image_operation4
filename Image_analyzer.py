#!python3.11

import tkinter as tk
from Modules.preference_window import Window
from Modules.window_layouts import Layouts
from Modules.window_events import Events
from Modules.window_functions import Functions

class App(
    Window,
    Layouts,
    Events,
    Functions,
):
    def __init__(self, master):
        super().__init__(master)

if __name__ == "__main__":
    print("Last update: 28 th Sep. 2023 by N. Kawakami")
    application = tk.Tk()
    app = App(application)
    app.run()
