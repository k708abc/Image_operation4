#!python3.11

import tkinter as tk
from Modules.preference_window import Window
from Modules.window_layouts import Layouts
from Modules.window_events import Events
from Modules.window_functions import Functions
from Modules.process_window import P_window
from Modules.recording_functions import Recording


class App(Window, Layouts, Events, Functions, P_window, Recording):
    def __init__(self, master):
        super().__init__(master)


if __name__ == "__main__":
    print("Last update: 9 th Oct. 2023 by N. Kawakami")
    application = tk.Tk()
    app = App(application)
    app.run()
    """
    メモ
    各機能の確認
    サイズ更新
    ラインプロファイル
    FFTでのドリフト更生　正確に
    各機能を個別ファイルにまとめる
    """
