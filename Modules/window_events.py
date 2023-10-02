#!python3.11

import tkinter as tk
import numpy as np
import os
from tkinter import filedialog
import pathlib
from Modules.process_classes import Smoothing, Median


class Events:
    def images_update(self, dir_name):
        self.image_list.dir_name = dir_name
        self.image_list.formlist()
        self.choice["values"] = self.image_list.images
        if len(self.image_list.images) > 0:
            self.choice.current(0)
            self.button_imopen["state"] = tk.NORMAL
            self.imtype_choice["values"] = self.image_list.types[0]
            self.imtype_choice.current(0)
        else:
            self.button_imopen["state"] = tk.DISABLED

    def record_fol_function(self):
        if self.rec_fol:
            self.dir_name_rec = self.dir_name
            self.rec_fol_name.delete(0, tk.END)
            self.rec_fol_name.insert(tk.END, self.dir_name_rec)

    def fol_choice_clicked(self):
        abs_pass = pathlib.Path(filedialog.askdirectory(initialdir=self.dir_name))
        if abs_pass == pathlib.Path("."):
            return
        self.images_update(os.path.relpath(abs_pass, self.init_dir))
        self.fol_name.delete(0, tk.END)
        self.fol_name.insert(tk.END, self.dir_name)
        self.record_fol_function()
        self.master.update()

    def choice_selected(self, event):
        self.button_imopen["state"] = tk.NORMAL
        self.imtype_choice["values"] = self.image_list.types[self.choice.current()]
        self.imtype_choice.current(0)
        self.master.update()

    def image_open_clicked(self):
        if self.real_image.open_bool is False:
            self.fft_button["state"] = tk.NORMAL
            self.record_button["state"] = tk.NORMAL
            self.drift_button["state"] = tk.NORMAL
        self.image_open()
        self.processes[0].image = np.copy(self.real_image.image_or)
        # self.run_process()
        self.real_image.show_image()

    def image_open(self):
        self.real_image.data_path = self.image_list.dir_name + "\\" + self.choice.get()
        self.real_image.channel_name = self.imtype_choice.current()
        self.real_image.read_image()
        # self.process_function()
        # self.update_after_show()

    def cb_color_selected(self, event):
        if self.real_shown:
            self.real_image.color_num = self.colormap_table.index(self.cb_color.get())
            self.real_image.show_image()
        else:
            self.FFT_image.color_num = self.colormap_table.index(self.cb_color.get())
            self.FFT_image.show_image()

    def upper_value_change(self, *args):
        if self.real_shown:
            self.real_image.upper = int(self.upper_val.get())
            self.real_image.show_image()
        else:
            self.FFT_image.upper = int(self.upper_val.get())
            self.FFT_image.show_image()

    def lower_value_change(self, *args):
        if self.real_shown:
            self.real_image.lower = int(self.lower_val.get())
            self.real_image.show_image()
        else:
            self.FFT_image.lower = int(self.lower_val.get())
            self.FFT_image.show_image()

    def default_function(self):
        self.upper_val.set(255)
        self.lower_val.set(0)
        if self.real_shown:
            self.real_image.back_default()
            self.real_image.show_image()
        else:
            self.FFT_image.back_default()
            self.FFT_image.show_image()

    def auto_set_function(self):
        pass

    def set_default_function(self):
        if self.real_shown:
            self.real_image.set_default()
        else:
            self.FFT_image.set_default()
        self.upper_val.set(255)
        self.lower_val.set(0)

    def cb_line_selected(self, event):
        if self.real_shown:
            self.real_image.line_method = self.method_line_cb.get()
            self.real_image.show_image()
        else:
            self.FFT_image.line_method = self.method_line_cb.get()
            self.FFT_image.show_image()

    def smooth_process(self, process_list):
        if process_list[-1].name == "Smoothing":
            process_list[-1].range = float(self.smooth_entry.get())
        else:
            self.val_reset(process_list[-1].name)
            val = Smoothing()
            val.range = float(self.smooth_entry.get())
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def smooth_change(self, event):
        if self.smooth_entry.get() == "":
            self.smooth_entry.insert(tk.END, "0")
        if self.real_shown:
            self.processes = self.smooth_process(self.processes)
            self.real_image.image_mod = np.copy(self.processes[-1].run())
            self.real_image.show_image()
        else:
            self.processes_FFT = self.smooth_process(self.processes_FFT)
            self.FFT_image.image_mod = np.copy(self.processes[-1].run())
            self.FFT_image.show_image()

    def median_process(self, process_list):
        if process_list[-1].name == "Median":
            process_list[-1].range = float(self.median_entry.get())
        else:
            self.val_reset(process_list[-1].name)
            val = Median()
            val.range = float(self.median_entry.get())
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def median_change(self, event):
        if self.median_entry.get() == "":
            self.median_entry.insert(tk.END, "0")
        if self.real_shown:
            self.processes = self.median_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.median_process(self.processes_FFT)
            self.FFT_image.image_mod = self.processes[-1].run()
            self.FFT_image.show_image()

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
        if self.manage_bool is False:
            self.manage_process()

    def rec_text(self):
        pass

    def rec_fol_choice_clicked(self):
        pass
