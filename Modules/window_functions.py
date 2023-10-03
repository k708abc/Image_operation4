#!python3.11


import os
import tkinter as tk
from Modules.image_class import MyImage, ImageList
from Modules.process_classes import ImOpen


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
        self.real_shown = True
        self.processes = [ImOpen()]
        self.processes_FFT = [ImOpen()]

        self.FFT_params = []
        self.manage_bool = False

    def val_reset(self, name):
        if name == "Smoothing":
            self.smooth_entry.delete(0, tk.END)
            self.smooth_entry.insert(tk.END, 0)
        elif name == "Median":
            self.median_entry.delete(0, tk.END)
            self.median_entry.insert(tk.END, 0)
        """
        elif prev_process == "set_contrast":
            self.upper_set_entry.delete(0, tk.END)
            self.upper_set_entry.insert(tk.END, 100)
            self.lower_set_entry.delete(0, tk.END)
            self.lower_set_entry.insert(tk.END, 0)

        elif prev_process == "drift":
            self.drift_dx.delete(0, tk.END)
            self.drift_dx.insert(tk.END, 0)
            self.drift_dy.delete(0, tk.END)
            self.drift_dy.insert(tk.END, 0)
            self.drift_bool.set(False)

        elif prev_process == "rescale":
            self.rescale_all.delete(0, tk.END)
            self.rescale_all.insert(tk.END, 1)
            self.rescale_x.delete(0, tk.END)
            self.rescale_x.insert(tk.END, 1)
            self.rescale_y.delete(0, tk.END)
            self.rescale_y.insert(tk.END, 1)

        elif prev_process == "cut":
            self.cut_entry.delete(0, tk.END)
            self.cut_entry.insert(tk.END, 0)

        elif prev_process == "int_change":
            self.int_cb.current(0)

        elif prev_process == "gamma":
            self.int_entry.delete(0, tk.END)
            self.int_entry.insert(tk.END, 0)

        elif prev_process == "edge_det":
            self.edge_cb.current(0)
            self.edge_entry.delete(0, tk.END)
            self.edge_entry.insert(tk.END, 3)
            self.mulor_bool.set(False)

        elif prev_process == "square":
            self.square_bool.set(False)

        elif prev_process == "oddize":
            self.oddize_bool.set(False)

        elif prev_process == "ave_sub":
            self.average_bool.set(False)

        elif prev_process == "mirror":
            self.mirror_bool.set(False)

        elif prev_process == "ignore_neg":
            self.ignore_neg_bool.set(False)

        elif prev_process == "FFT":
            pass

        elif prev_process == "Symm":
            self.method_symmetrize_cb.current(0)

        elif prev_process == "Rot":
            self.symm_angle_entry.delete(0, tk.END)
            self.symm_angle_entry.insert(tk.END, 0)
        elif prev_process == "reset":
            pass
        self.update_mag()
        self.size_update()
        """
