#!python3.11

import tkinter as tk
from Modules.preference_window import Window
from Modules.window_layouts import Layouts
from Modules.window_events import Events
from Modules.window_functions import Functions
from Modules.process_window import P_window


class App(Window, Layouts, Events, Functions, P_window):
    def __init__(self, master):
        super().__init__(master)


if __name__ == "__main__":
    print("Last update: 2 nd Oct. 2023 by N. Kawakami")
    application = tk.Tk()
    app = App(application)
    app.run()
