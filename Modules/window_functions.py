#!python3.11

import glob
import os
import tkinter as tk
from Modules.image_class import MyImage

class Functions:
    def run(self) -> None:
        self.mainloop()

    def init_setting(self):
        self.real_image = MyImage()
        self.fft_image = MyImage()
        self.init_dir = os.getcwd()
        self.dir_name = os.getcwd()
        self.dir_name_rec = os.getcwd()
        self.rec_fol = True

    def read_image_list(self, dir_name):
        image_list = glob.glob(dir_name + "\*")
        image_list = [os.path.basename(pathname) for pathname in image_list]
        image_list2 = []
        for file in image_list:
            data_path = dir_name + "\\" + file
            imtype = self.get_datatypes(data_path)
            if imtype[0] == "folder":
                pass
            elif imtype[0] == "else":
                pass
            else:
                image_list2.append(file)
        return image_list2

    def get_datatypes(self, data_path):
        data_type = os.path.splitext(data_path)
        if data_type[1] == ".bmp":
            return ["bmp"]
        elif data_type[1] == ".txt":
            return ["txt"]
        elif data_type[1] == ".SM4":
            return self.datatypes(data_path)
        elif os.path.isdir(data_type[0]):
            return ["folder"]
        else:
            return ["else"]
        
    def record_fol_function(self):
        if self.rec_fol:
            self.dir_name_rec = self.dir_name
            self.rec_fol_name.delete(0, tk.END)
            self.rec_fol_name.insert(tk.END, self.dir_name_rec)

    def reflesh_image_list(self):
        self.image_list = self.read_image_list(self.dir_name)
        self.choice["values"] = self.image_list
        if len(self.image_list) > 0:
            self.choice.current(0)
            self.button_imopen["state"] = tk.NORMAL
            self.data_path = self.dir_name + "\\" + self.choice.get()
            self.imtype_list = self.get_datatypes(self.data_path)
            self.imtype_choice["values"] = self.imtype_list
            self.imtype_choice.current(0)
        else:
            self.button_imopen["state"] = tk.DISABLED