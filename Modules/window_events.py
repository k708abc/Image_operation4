#!python3.11

import tkinter as tk
import numpy as np
import os
from tkinter import filedialog
import pathlib

class Events:
    def fol_choice_clicked(self):
        abs_pass = pathlib.Path(filedialog.askdirectory(initialdir=self.dir_name))
        if abs_pass == pathlib.Path("."):
            return
        self.dir_name = os.path.relpath(abs_pass, self.init_dir)
        self.fol_name.delete(0, tk.END)
        self.fol_name.insert(tk.END, self.dir_name)
        self.record_fol_function()
        self.reflesh_image_list()
        self.master.update()

    def choice_selected(self, event):
        self.data_path = self.dir_name + "\\" + self.choice.get()
        self.imtype_list = self.get_datatypes(self.data_path)
        self.button_imopen["state"] = tk.NORMAL
        self.imtype_choice["values"] = self.imtype_list
        self.imtype_choice.current(0)
        self.master.update()

    def image_open_clicked(self):
        if self.image_check():
            if self.real_image.open_bool is False:
                self.fft_button["state"] = tk.NORMAL
                self.record_button["state"] = tk.NORMAL
                self.drift_button["state"] = tk.NORMAL
            self.image_open()
            # self.run_process()
            self.real_image.show_image()

    def image_check(self):
        data_path_check = self.dir_name + "\\" + self.choice.get()
        channel_type_check = self.imtype_choice.current()
        data_type = os.path.splitext(data_path_check)
        if data_type[1] in [".SM4", ".bmp"]:
            self.data_path_op = data_path_check
            self.channel_type_op = channel_type_check
            return True
        elif data_type[1] == ".txt":
            data, _ = self.txt_getdata(data_path_check)
            if data is False:
                return False
            else:
                self.data_path_op = data_path_check
                self.channel_type_op = channel_type_check
                return True
        else:
            return False
        
    def image_open(self):
        self.real_image.data_path = self.data_path_op
        self.real_image.channel_name = self.channel_type_op
        self.real_image.read_image()
        #self.process_function()
        #self.update_after_show()







    def rec_fol_choice_clicked(self):
        pass



    def upper_value_change(self, *args):
        pass

    def lower_value_change(self, *args):
        pass

    def default_function(self):
        pass

    def auto_set_function(self):
        pass

    def set_default_function(self):
        pass

    def cb_color_selected(self, event):
        pass

    def smooth_change(self, event):
        pass

    def median_change(self, event):
        pass

    def drift_check_func(self):
        pass

    def drift_val_change(self, event):
        pass

    def drift_function(self):
        pass

    def rescale(self, event):
        pass

    def cut_image(self, event):
        pass

    def int_cb_selected(self, event):
        pass

    def int_gamma_change(self, event):
        pass

    def edge_cb_selected(self, event):
        pass

    def edge_range_change(self, event):
        pass

    def mulor_check_change(self):
        pass

    def square_image(self):
        pass

    def oddize_image(self):
        pass

    def average_image(self):
        pass

    def mirror_image(self):
        pass

    def ignore_neg_image(self):
        pass

    def original_size_changed(self, event):
        self.current_size_update()

    def fft_function(self):
        pass

    def cb_method_selected(self, event):
        pass

    def cb_window_selected(self, event):
        pass

    def cb_line_selected(self, event):
        pass

    def cb_symmetrize_selected(self, event):
        pass

    def symm_angle_return(self, event):
        pass

    def symm_angle_up(self, event):
        pass

    def symm_angle_down(self, event):
        pass

    def draw_line_checked(self):
        pass

    def record_name_changed(self, event):
        pass

    def record_function(self):
        pass

    def close_function(self):
        pass

    def process_window(self):
        pass

    def rec_text(self):
        pass
