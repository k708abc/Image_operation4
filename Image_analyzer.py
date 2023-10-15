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
    print("Last update: 14 th Oct. 2023 by N. Kawakami")
    application = tk.Tk()
    app = App(application)
    app.run()
    """
    メモ
    各機能の確認
    サイズ更新
    ラインプロファイル
        連続入力に対していちいち更新しないように
    FFTでのドリフト更生　正確に
    各機能を個別ファイルにまとめる
    ドリフト補正を画像に反映
    回転等での背景コントラスト
    #
    drift FFT
        real像への矢印表示
        計算結果があってない
        image type がへん
        デフォルトベクトルでエラー
        ベクトルを矢印に
        拡大時のベクトルの更新
        矢印に色

    """
