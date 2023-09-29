#!python3.11


import os
import tkinter as tk
from Modules.image_class import MyImage, ImageList

class Functions:
    def run(self) -> None:
        self.mainloop()

    def init_setting(self):
        self.real_image = MyImage()
        self.fft_image = MyImage()
        self.image_list = ImageList()
        self.init_dir = os.getcwd()
        self.dir_name = os.getcwd()
        self.dir_name_rec = os.getcwd()
        self.rec_fol = True



