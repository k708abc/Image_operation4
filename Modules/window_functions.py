#!python3.11


import os
import tkinter as tk
from Modules.image_class import MyImage, ImageList, FFT
from Modules.process_classes import ImOpen
import numpy as np


class Functions:
    def run(self) -> None:
        self.mainloop()

    def init_setting(self):
        self.real_image = MyImage()
        self.fft_image = MyImage()
        self.fft_func = FFT()
        self.image_list = ImageList()
        self.init_dir = os.getcwd()
        self.dir_name = os.getcwd()
        self.dir_name_rec = os.getcwd()
        self.rec_fol = True
        self.real_shown = True
        self.processes = [ImOpen()]
        self.processes_FFT = [ImOpen()]
        self.manage_bool = False
        self.name_change = False
        self.bias_change = False

    def record_name_base(self):
        if self.name_change is False:
            self.image_name = self.choice.get()
            self.channel_type = self.imtype_choice.current()
            self.rec_name = (
                self.image_name.replace(
                    os.path.splitext(self.real_image.data_path)[1], ""
                )
                + "_"
                + str(self.channel_type)
            )
            self.record.delete(0, tk.END)
            self.record.insert(tk.END, self.rec_name)

    def check_name(self):
        if self.record_plus.get() not in ("_processed", "_FFT", "---"):
            self.name_change = True

    def record_name_real(self):
        self.check_name()
        if self.name_change is False:
            self.record_plus.delete(0, tk.END)
            self.record_plus.insert(tk.END, "_processed")

    def record_name_fft(self):
        self.check_name()
        if self.name_change is False:
            self.record_plus.delete(0, tk.END)
            self.record_plus.insert(tk.END, "_FFT")

    def update_after_show(self):
        self.record_name_base()
        self.record_name_real()
        self.original_x.delete(0, tk.END)
        self.original_x.insert(tk.END, self.real_image.params[0])
        self.original_y.delete(0, tk.END)
        self.original_y.insert(tk.END, self.real_image.params[1])
        self.orpix_x["text"] = "(" + str(self.real_image.x_or) + " px)"
        self.orpix_y["text"] = "(" + str(self.real_image.y_or) + " px)"
        if self.bias_change:
            self.bias.delete(0, tk.END)
            self.bias.insert(tk.END, round(self.real_image.params[2] * 1000, 2))
        self.bias_change = False

    def val_reset(self, name):
        if name == "Smoothing":
            self.smooth_entry.delete(0, tk.END)
            self.smooth_entry.insert(tk.END, 0)
        elif name == "Median":
            self.median_entry.delete(0, tk.END)
            self.median_entry.insert(tk.END, 0)
        elif name == "Drift":
            self.drift_dx.delete(0, tk.END)
            self.drift_dx.insert(tk.END, 0)
            self.drift_dy.delete(0, tk.END)
            self.drift_dy.insert(tk.END, 0)

        elif name == "Rescale":
            self.rescale_all.delete(0, tk.END)
            self.rescale_all.insert(tk.END, 1)
            self.rescale_x.delete(0, tk.END)
            self.rescale_x.insert(tk.END, 1)
            self.rescale_y.delete(0, tk.END)
            self.rescale_y.insert(tk.END, 1)

        elif name == "Cut":
            self.cut_entry.delete(0, tk.END)
            self.cut_entry.insert(tk.END, 0)

        elif name == "Intensity":
            self.int_cb.current(0)

        elif name == "Gamma":
            self.int_entry.delete(0, tk.END)
            self.int_entry.insert(tk.END, 0)

        elif name == "Edge":
            self.edge_cb.current(0)
            self.edge_entry.delete(0, tk.END)
            self.edge_entry.insert(tk.END, 3)
            self.mulor_bool.set(False)

        elif name == "Symmetrize":
            self.method_symmetrize_cb.current(0)

        elif name == "Angle":
            self.angle_entry.delete(0, tk.END)
            self.angle_entry.insert(tk.END, 0)

        elif name == "Squarize":
            self.square_bool.set(False)

        elif name == "Oddize":
            self.oddize_bool.set(False)

        elif name == "Ave. sub.":
            self.average_bool.set(False)

        elif name == "Mirror":
            self.mirror_bool.set(False)

        elif name == "Ignore neg.":
            self.ignore_neg_bool.set(False)

        """
        elif prev_process == "set_contrast":
            self.upper_set_entry.delete(0, tk.END)
            self.upper_set_entry.insert(tk.END, 100)
            self.lower_set_entry.delete(0, tk.END)
            self.lower_set_entry.insert(tk.END, 0)

        elif prev_process == "FFT":
            pass

        elif prev_process == "reset":
            pass
        self.update_mag()
        self.size_update()
        """

    def run_process(self):
        image = self.real_image.image_or
        for pro in self.processes:
            if pro.switch:
                pro.image = np.copy(image)
                image = pro.run()
        self.real_image.image_mod = np.copy(image)
        self.real_image.show_image()

        if self.real_shown is False:
            self.fft_func.image = self.real_image.image_mod
            image = self.fft_func.run()
            self.fft_image.image_or = np.copy(image)
            for pro in self.processes_FFT:
                if pro.switch:
                    pro.image = np.copy(image)
                    image = pro.run()
            self.fft_image.image_mod = np.copy(image)
            self.fft_image.default_contrast()
            self.fft_image.show_image()
