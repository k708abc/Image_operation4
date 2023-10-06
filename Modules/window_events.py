#!python3.11

import tkinter as tk
import numpy as np
import os
from tkinter import filedialog
import pathlib
from Modules.process_classes import (
    Smoothing,
    Median,
    Drift,
    Rescale,
    Cut,
    Intensity,
    Gamma,
    Edge,
    Square,
    Odd,
    Average,
    Mirror,
    Ignore_neg,
    Symm,
    Angle,
)
from Modules.drift_fix_windows import drift_two_images
from Modules.drift_fix_fft import drift_fft


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
            self.dir_name_rec = self.image_list.dir_name
            self.rec_fol_name.delete(0, tk.END)
            self.rec_fol_name.insert(tk.END, self.dir_name_rec)

    def fol_choice_clicked(self):
        abs_pass = pathlib.Path(filedialog.askdirectory(initialdir=self.dir_name))
        if abs_pass == pathlib.Path("."):
            return
        fol_dir = os.path.relpath(abs_pass, self.init_dir)
        self.images_update(fol_dir)
        self.fol_name.delete(0, tk.END)
        self.fol_name.insert(tk.END, fol_dir)
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
        self.run_process()
        self.real_image.show_image()

    def image_open(self):
        self.real_image.data_path = self.image_list.dir_name + "\\" + self.choice.get()
        self.real_image.channel_name = self.imtype_choice.current()
        self.real_image.read_image()
        self.run_process()
        self.update_after_show()

    def cb_color_selected(self, event):
        if self.real_shown:
            self.real_image.color_num = self.colormap_table.index(self.cb_color.get())
            self.real_image.show_image()
        else:
            self.fft_image.color_num = self.colormap_table.index(self.cb_color.get())
            self.fft_image.show_image()

    def upper_value_change(self, *args):
        if self.real_shown:
            self.real_image.upper = int(self.upper_val.get())
            self.real_image.show_image()
        else:
            self.fft_image.upper = int(self.upper_val.get())
            self.fft_image.show_image()

    def lower_value_change(self, *args):
        if self.real_shown:
            self.real_image.lower = int(self.lower_val.get())
            self.real_image.show_image()
        else:
            self.fft_image.lower = int(self.lower_val.get())
            self.fft_image.show_image()

    def default_function(self):
        self.upper_val.set(255)
        self.lower_val.set(0)
        if self.real_shown:
            self.real_image.back_default()
            self.real_image.show_image()
        else:
            self.fft_image.back_default()
            self.fft_image.show_image()

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
            self.fft_image.line_method = self.method_line_cb.get()
            self.fft_image.show_image()

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
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

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
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def drift_process(self, process_list):
        if process_list[-1].name == "Drift":
            process_list[-1].x = float(self.drift_dx.get())
            process_list[-1].y = float(self.drift_dy.get())
        else:
            self.val_reset(process_list[-1].name)
            val = Drift()
            val.x = float(self.drift_dx.get())
            val.y = float(self.drift_dy.get())
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def drift_val_change(self, event):
        if self.real_shown:
            self.processes = self.drift_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.dfift_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def drift_function(self):
        if self.drift_cb.current() == 0:
            # two images
            drift_two_images(self)
        elif self.drift_cb.current() == 1:
            # fft
            drift_fft(self)

    def rescale_process(self, process_list):
        if process_list[-1].name == "Rescale":
            process_list[-1].all = float(self.rescale_all.get())
            process_list[-1].x = float(self.rescale_x.get())
            process_list[-1].y = float(self.rescale_y.get())
        else:
            self.val_reset(process_list[-1].name)
            val = Rescale()
            val.all = float(self.rescale_all.get())
            val.x = float(self.rescale_x.get())
            val.y = float(self.rescale_y.get())
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def rescale(self, event):
        if self.real_shown:
            self.processes = self.rescale_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.rescale_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def cut_process(self, process_list):
        if process_list[-1].name == "Cut":
            process_list[-1].ratio = float(self.cut_entry.get())
        else:
            self.val_reset(process_list[-1].name)
            val = Cut()
            val.ratio = float(self.cut_entry.get())
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def cut_image(self, event):
        if self.real_shown:
            self.processes = self.cut_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.cut_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def int_process(self, process_list):
        if process_list[-1].name == "Intensity":
            process_list[-1].method = self.int_cb.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Intensity()
            val.method = self.int_cb.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def int_cb_selected(self, event):
        if self.real_shown:
            self.processes = self.int_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.int_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def gamma_process(self, process_list):
        if process_list[-1].name == "Gamma":
            process_list[-1].val = float(self.int_entry.get())
        else:
            self.val_reset(process_list[-1].name)
            val = Gamma()
            val.val = float(self.int_entry.get())
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def int_gamma_change(self, event):
        if self.real_shown:
            self.processes = self.gamma_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.gamma_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def edge_process(self, process_list):
        if process_list[-1].name == "Edge":
            process_list[-1].method = self.edge_cb.get()
            process_list[-1].const = self.edge_entry.get()
            process_list[-1].mul_or = self.mulor_bool.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Edge()
            val.method = self.edge_cb.get()
            val.const = self.edge_entry.get()
            val.mul_or = self.mulor_bool.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def edge_change(self, event=None):
        if self.real_shown:
            self.processes = self.edge_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.edge_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def symm_process(self, process_list):
        if process_list[-1].name == "Symmetrize":
            process_list[-1].method = self.method_symmetrize_cb.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Symm()
            val.method = self.method_symmetrize_cb.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def cb_symmetrize_selected(self, event):
        if self.real_shown:
            self.processes = self.symm_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.symm_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def angle_process(self, process_list):
        if process_list[-1].name == "Angle":
            process_list[-1].angle = float(self.symm_angle_entry.get())
        else:
            self.val_reset(process_list[-1].name)
            val = Angle()
            val.angle = float(self.symm_angle_entry.get())
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def angle_return(self, event=None):
        if self.real_shown:
            self.processes = self.angle_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.angle_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def angle_up(self, event):
        angle = float(self.symm_angle_entry.get()) + 1
        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(tk.END, angle)
        self.angle_return()

    def angle_down(self, event):
        angle = float(self.symm_angle_entry.get()) - 1
        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(tk.END, angle)
        self.angle_return()

    def square_process(self, process_list):
        if process_list[-1].name == "Squarize":
            process_list[-1].on = self.square_bool.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Square()
            val.on = self.square_bool.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def square_image(self):
        if self.real_shown:
            self.processes = self.square_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.square_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def odd_process(self, process_list):
        if process_list[-1].name == "Oddize":
            process_list[-1].on = self.oddize_bool.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Odd()
            val.on = self.oddize_bool.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def oddize_image(self):
        if self.real_shown:
            self.processes = self.odd_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.odd_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def ave_process(self, process_list):
        if process_list[-1].name == "Ave. sub.":
            process_list[-1].on = self.average_bool.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Average()
            val.on = self.average_bool.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def average_image(self):
        if self.real_shown:
            self.processes = self.ave_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.ave_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def mirror_process(self, process_list):
        if process_list[-1].name == "mirror":
            process_list[-1].on = self.mirror_bool.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Mirror()
            val.on = self.mirror_bool.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def mirror_image(self):
        if self.real_shown:
            self.processes = self.mirror_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.mirror_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def igneg_process(self, process_list):
        if process_list[-1].name == "ignore neg.":
            process_list[-1].on = self.ignore_neg_bool.get()
        else:
            self.val_reset(process_list[-1].name)
            val = Ignore_neg()
            val.on = self.ignore_neg_bool.get()
            val.image = process_list[-1].run()
            process_list.append(val)
        return process_list

    def ignore_neg_image(self):
        if self.real_shown:
            self.processes = self.igneg_process(self.processes)
            self.real_image.image_mod = self.processes[-1].run()
            self.real_image.show_image()
        else:
            self.processes_FFT = self.igneg_process(self.processes_FFT)
            self.fft_image.image_mod = self.processes_FFT[-1].run()
            self.fft_image.show_image()
        if self.manage_bool:
            self.update_process_w()

    def original_size_changed(self, event):
        self.current_size_update()

    def fft_process(self):
        pass

    def fft_clicked(self):
        if self.real_shown:
            self.real_shown = False
            self.fft_image.open_bool = True
        else:
            self.real_shown = True
        self.fft_func.method = self.method_fft_cb.get()
        self.fft_func.window_func = self.window_cb.get()
        self.run_process()

    def cb_method_selected(self, event):
        self.fft_func.method = self.method_fft_cb.get()
        self.run_process()

    def cb_window_selected(self, event):
        self.fft_func.window = self.window_cb.get()
        self.run_process()

    def rec_fol_choice_clicked(self):
        self.rec_fol = False
        abs_pass = pathlib.Path(filedialog.askdirectory(initialdir=self.dir_name_rec))
        if abs_pass == pathlib.Path("."):
            return
        self.dir_name_rec = os.path.relpath(abs_pass, self.init_dir)
        self.rec_fol_name.delete(0, tk.END)
        self.rec_fol_name.insert(tk.END, self.dir_name_rec)

    def record_name_changed(self, event):
        self.name_change = True

    def record_function(self):
        self.rec_text()
        self.rec_image()

    def close_function(self):
        self.quit()

    def process_window(self):
        if self.manage_bool is False:
            self.manage_process()

    def rec_text(self):
        self.run_process()
        self.show_image()
        self.recording_text()
