#!python3.12

import tkinter.ttk as ttk
import tkinter as tk
import cv2
import numpy as np
import math
from Modules.image_class import MyImage, FFT
from Modules.process_classes import Rescale


def initial_setting_dfft(self):
    self.drift_fix_fft_open = True
    self.image_drift_real = MyImage()
    self.image_drift_fft = MyImage()
    self.fft_drift = FFT()
    self.rescale_dfft = Rescale()
    self.image_drift_real.image_name = "Drift fix"
    self.image_drift_fft.image_name = "Drift fix"
    self.image_drift_real.line_on = True
    self.image_drift_fft.line_on = True
    self.image_drift_real.open_bool = True
    self.image_drift_fft.open_bool = True
    self.image_open_dfft = True
    self.dfft_FFT = True
    self.prev_mag = 1
    read_image_dfft(self)
    update_dfft(self)
    reset_arrow_dfft(self)
    show_image_dfft(self)


def prepare_widgets(self):
    create_frame_ref_choice_dfft(self)
    create_frame_fft_dfft(self)
    create_frame_magnification_dfft(self)
    create_frame_size_dfft(self)
    create_frame_set_vector(self)
    create_frame_params_dfft(self)
    create_frame_buttons_dfft(self)
    create_flame_comment_dfft(self)


def create_frame_ref_choice_dfft(self):
    self.frame_choice_dfft = ttk.Frame(self.fft_fix_window)
    create_widgets_choice_dfft(self)
    create_layout_choice_dfft(self)
    self.frame_choice_dfft.pack()


def create_widgets_choice_dfft(self):
    # reference
    self.var_cb_choice_dfft = tk.StringVar()
    self.cb_choice_dfft = ttk.Combobox(
        self.frame_choice_dfft,
        textvariable=self.var_cb_choice_dfft,
        values=self.image_list.images,
        width=40,
    )
    if len(self.image_list.images) > 0:
        self.cb_choice_dfft.current(self.choice.current())
    self.cb_choice_dfft.bind(
        "<<ComboboxSelected>>", lambda event, arg=self: ref_selected_dfft(event, arg)
    )
    #
    self.cblabel_ref_dfft = tk.Label(self.frame_choice_dfft, text="Reference")
    #
    self.var_imtypes_dfft = tk.StringVar()
    self.cb_imtype_dfft = ttk.Combobox(
        self.frame_choice_dfft,
        textvariable=self.var_imtypes_dfft,
        width=40,
    )
    if len(self.image_list.types) > 0:
        self.cb_imtype_dfft["values"] = self.image_list.types[self.choice.current()]
        self.cb_imtype_dfft.current(self.imtype_choice.current())
    self.imtype_dfft_text = ttk.Label(self.frame_choice_dfft, text="Image type")
    #
    self.button_dfft_open = tk.Button(
        self.frame_choice_dfft,
        text="Open",
        command=lambda: read_dfft_clicked(self),
        width=10,
    )
    self.button_dfft_open["state"] = tk.NORMAL


def create_layout_choice_dfft(self):
    self.cb_choice_dfft.grid(row=0, column=1, **self.padWE)
    self.cblabel_ref_dfft.grid(row=0, column=0, **self.padWE)
    self.cb_imtype_dfft.grid(row=1, column=1, **self.padWE)
    self.imtype_dfft_text.grid(row=1, column=0, **self.padWE)
    self.button_dfft_open.grid(
        rowspan=2, row=0, column=2, sticky=tk.N + tk.S, padx=15, pady=2
    )


def create_frame_fft_dfft(self):
    self.frame_fft_dfft = ttk.Frame(self.fft_fix_window)
    create_widgets_fft_dfft(self)
    create_layout_fft_dfft(self)
    self.frame_fft_dfft.pack()


def create_widgets_fft_dfft(self):
    self.fft_button_dfft = tk.Button(
        self.frame_fft_dfft,
        text="FFT→\rReal",
        command=lambda: fft_function_dfft(self),
        width=10,
    )
    #
    self.var_method_fft_dfft = tk.StringVar()
    self.method_fft_cb_dfft = ttk.Combobox(
        self.frame_fft_dfft,
        textvariable=self.var_method_fft_dfft,
        values=self.method_fft_table,
    )
    self.method_fft_cb_dfft.bind(
        "<<ComboboxSelected>>",
        lambda event, arg=self: cb_method_selected_dfft(event, arg),
    )
    self.method_fft_cb_dfft.current(self.method_fft_cb.current())
    self.method_text_dfft = ttk.Label(self.frame_fft_dfft, text="Method")
    #
    self.var_window_dfft = tk.StringVar()
    self.window_cb_dfft = ttk.Combobox(
        self.frame_fft_dfft, textvariable=self.var_window_dfft, values=self.window_table
    )
    self.window_cb_dfft.bind(
        "<<ComboboxSelected>>",
        lambda event, arg=self: cb_window_selected_dfft(event, arg),
    )
    self.window_cb_dfft.current(self.window_cb.current())
    self.window_text_dfft = ttk.Label(self.frame_fft_dfft, text="Window")


def create_layout_fft_dfft(self):
    self.fft_button_dfft.grid(rowspan=2, row=0, column=2, sticky=tk.N + tk.S)
    self.method_text_dfft.grid(row=0, column=0, **self.padWE)
    self.method_fft_cb_dfft.grid(row=0, column=1, **self.padWE)
    self.window_text_dfft.grid(row=1, column=0, **self.padWE)
    self.window_cb_dfft.grid(row=1, column=1, **self.padWE)


def create_frame_magnification_dfft(self):
    self.frame_mag_dfft = ttk.Frame(self.fft_fix_window)
    create_widgets_mag_dfft(self)
    create_layout_mag_dfft(self)
    self.frame_mag_dfft.pack()


def create_widgets_mag_dfft(self):
    self.label_dfft_mag = tk.Label(self.frame_mag_dfft, text="Magnification")
    self.dfft_mag_entry = ttk.Entry(self.frame_mag_dfft, width=7)
    self.dfft_mag_entry.bind("<Return>", lambda event, arg=self: mag_bind(event, arg))
    self.dfft_mag_entry.insert(tk.END, "1")


def create_layout_mag_dfft(self):
    self.label_dfft_mag.grid(row=0, column=0, **self.padWE)
    self.dfft_mag_entry.grid(row=0, column=1, **self.padWE)


def create_frame_size_dfft(self):
    self.frame_size_dfft = ttk.Frame(self.fft_fix_window)
    create_widgets_size_dfft(self)
    create_layout_size_dfft(self)
    self.frame_size_dfft.pack()


def create_widgets_size_dfft(self):
    self.label_dfft_size_x = tk.Label(self.frame_size_dfft, text="Size x (nm)")
    self.dfft_size_x_entry = ttk.Entry(self.frame_size_dfft, width=7)
    self.dfft_size_x_entry.insert(tk.END, "30")
    self.dfft_size_x_entry.bind(
        "<Return>", lambda event, arg=self: size_bind(event, arg)
    )
    #
    self.label_dfft_size_y = tk.Label(self.frame_size_dfft, text="Size y (nm)")
    self.dfft_size_y_entry = ttk.Entry(self.frame_size_dfft, width=7)
    self.dfft_size_y_entry.insert(tk.END, "30")
    self.dfft_size_y_entry.bind(
        "<Return>", lambda event, arg=self: size_bind(event, arg)
    )
    #
    self.label_dfft_size_x_FFT = tk.Label(self.frame_size_dfft, text="Size kx (nm-1)")
    self.dfft_size_x_FFT = tk.Label(self.frame_size_dfft, text="0")
    #
    self.label_dfft_size_y_FFT = tk.Label(self.frame_size_dfft, text="Size ky (nm-1)")
    self.dfft_size_y_FFT = tk.Label(self.frame_size_dfft, text="0")


def create_layout_size_dfft(self):
    self.label_dfft_size_x.grid(row=0, column=0, **self.padWE)
    self.dfft_size_x_entry.grid(row=0, column=1, **self.padWE)
    self.label_dfft_size_y.grid(row=0, column=2, **self.padWE)
    self.dfft_size_y_entry.grid(row=0, column=3, **self.padWE)
    self.label_dfft_size_x_FFT.grid(row=1, column=0, **self.padWE)
    self.dfft_size_x_FFT.grid(row=1, column=1, **self.padWE)
    self.label_dfft_size_y_FFT.grid(row=1, column=2, **self.padWE)
    self.dfft_size_y_FFT.grid(row=1, column=3, **self.padWE)


def create_frame_set_vector(self):
    self.frame_set_vector = ttk.Frame(self.fft_fix_window)
    create_widgets_set_vector(self)
    create_layout_set_vector(self)
    self.frame_set_vector.pack()


def create_widgets_set_vector(self):
    self.vec1_label = ttk.Label(self.frame_set_vector, text="Vector 1")
    self.vec1_px_label = ttk.Label(self.frame_set_vector, text="px")
    #
    self.vec1_py_label = ttk.Label(self.frame_set_vector, text="py")
    #
    self.dfft_k1_label = ttk.Label(self.frame_set_vector, text="0 nm-1")
    self.dfft_k1_angle_label = ttk.Label(self.frame_set_vector, text="0 °")
    self.dfft_r1_label = ttk.Label(self.frame_set_vector, text="0 nm")
    self.dfft_r1_angle_label = ttk.Label(self.frame_set_vector, text="0 °")
    self.FFT_label_k1 = ttk.Label(self.frame_set_vector, text="FFT")
    self.FFT_label_r1 = ttk.Label(self.frame_set_vector, text="Real")
    #
    self.vec2_label = ttk.Label(self.frame_set_vector, text="Vector 2")
    self.vec2_px_label = ttk.Label(self.frame_set_vector, text="px")
    #
    self.dfft_k2_label = ttk.Label(self.frame_set_vector, text="0 nm-1")
    self.dfft_k2_angle_label = ttk.Label(self.frame_set_vector, text="0 °")
    self.dfft_r2_label = ttk.Label(self.frame_set_vector, text="0 nm")
    self.dfft_r2_angle_label = ttk.Label(self.frame_set_vector, text="0 °")
    self.FFT_label_k2 = ttk.Label(self.frame_set_vector, text="FFT")
    self.FFT_label_r2 = ttk.Label(self.frame_set_vector, text="Real")


def create_layout_set_vector(self):
    self.vec1_label.grid(row=0, column=0, **self.padWE)
    self.vec1_px_label.grid(row=0, column=1, **self.padWE)
    # self.vec1_px_entry.grid(row=0, column=2, **self.padWE)
    self.vec1_py_label.grid(row=0, column=3, **self.padWE)
    # self.vec1_py_entry.grid(row=0, column=4, **self.padWE)
    self.FFT_label_k1.grid(row=1, column=1, **self.padWE)
    self.dfft_k1_label.grid(row=1, column=2, **self.padWE)
    self.dfft_k1_angle_label.grid(row=1, column=3, **self.padWE)
    self.FFT_label_r1.grid(row=2, column=1, **self.padWE)
    self.dfft_r1_label.grid(row=2, column=2, **self.padWE)
    self.dfft_r1_angle_label.grid(row=2, column=3, **self.padWE)
    #
    self.vec2_label.grid(row=3, column=0, **self.padWE)
    self.vec2_px_label.grid(row=3, column=1, **self.padWE)
    # self.vec2_px_entry.grid(row=3, column=2, **self.padWE)
    self.vec2_py_label.grid(row=3, column=3, **self.padWE)
    # self.vec2_py_entry.grid(row=3, column=4, **self.padWE)
    self.FFT_label_k2.grid(row=4, column=1, **self.padWE)
    #
    self.dfft_k2_label.grid(row=4, column=2, **self.padWE)
    self.dfft_k2_angle_label.grid(row=4, column=3, **self.padWE)
    self.FFT_label_r2.grid(row=5, column=1, **self.padWE)
    self.dfft_r2_label.grid(row=5, column=2, **self.padWE)
    self.dfft_r2_angle_label.grid(row=5, column=3, **self.padWE)


def create_frame_params_dfft(self):
    self.frame_params_dfft = ttk.Frame(self.fft_fix_window)
    create_widgets_params_dfft(self)
    create_layout_params_dfft(self)
    self.frame_params_dfft.pack()


def create_widgets_params_dfft(self):
    self.dfft_ratio_label = ttk.Label(self.frame_params_dfft, text="Ratio (v2/v1)")
    self.dfft_dif_angle_label = ttk.Label(self.frame_params_dfft, text="Diff. angle")
    self.dfft_ratio_val = ttk.Label(self.frame_params_dfft, text="0")
    self.dfft_dif_angle_val = ttk.Label(self.frame_params_dfft, text="0 °")
    #
    self.dfft_set_ratio_label = ttk.Label(self.frame_params_dfft, text="Set ratio")
    self.dfft_set_dif_angle_label = ttk.Label(self.frame_params_dfft, text="Set angle")
    self.dfft_set_ratio_entry = ttk.Entry(self.frame_params_dfft, width=7)
    self.dfft_set_ratio_entry.insert(tk.END, "1")
    self.dfft_set_angle_entry = ttk.Entry(self.frame_params_dfft, width=7)
    self.dfft_set_angle_entry.insert(tk.END, "60")


def create_layout_params_dfft(self):
    self.dfft_ratio_label.grid(row=0, column=2, **self.padWE)
    self.dfft_dif_angle_label.grid(row=1, column=2, **self.padWE)
    self.dfft_ratio_val.grid(row=0, column=3, **self.padWE)
    self.dfft_dif_angle_val.grid(row=1, column=3, **self.padWE)
    #
    self.dfft_set_ratio_label.grid(row=0, column=0, **self.padWE)
    self.dfft_set_ratio_entry.grid(row=0, column=1, **self.padWE)
    self.dfft_set_dif_angle_label.grid(row=1, column=0, **self.padWE)
    self.dfft_set_angle_entry.grid(row=1, column=1, **self.padWE)


def create_frame_buttons_dfft(self):
    self.frame_buttons_dfft = ttk.Frame(self.fft_fix_window)
    create_widgets_buttons_dfft(self)
    create_layout_buttons_dfft(self)
    self.frame_buttons_dfft.pack()


def create_widgets_buttons_dfft(self):
    self.button_dfft_calculate = tk.Button(
        self.frame_buttons_dfft,
        text="Calculate",
        command=lambda: calculate_dfft(self),
        width=10,
    )
    self.button_dfft_calculate["state"] = tk.NORMAL
    #
    self.button_dfft_reset = tk.Button(
        self.frame_buttons_dfft,
        text="Reset",
        command=lambda: reset_dfft(self),
        width=10,
    )
    self.button_dfft_reset["state"] = tk.NORMAL
    #
    self.button_dfft_close = tk.Button(
        self.frame_buttons_dfft,
        text="Close",
        command=lambda: close_dfft(self),
        width=10,
    )
    self.button_dfft_close["state"] = tk.NORMAL


def create_layout_buttons_dfft(self):
    self.button_dfft_calculate.grid(row=0, column=0, **self.padWE)
    self.button_dfft_reset.grid(row=0, column=1, **self.padWE)
    self.button_dfft_close.grid(row=0, column=2, **self.padWE)


def create_flame_comment_dfft(self):
    self.frame_comment_dfft = ttk.Frame(self.fft_fix_window)
    create_widgets_comment_dfft(self)
    create_layout_comment_dfft(self)
    self.frame_comment_dfft.pack()


def create_widgets_comment_dfft(self):
    self.dfft_val_check_label = ttk.Label(self.frame_comment_dfft, text="\n")


def create_layout_comment_dfft(self):
    self.dfft_val_check_label.grid(row=0, column=0, **self.padWE)


def ref_selected_dfft(event, self):
    self.cb_imtype_dfft["values"] = self.image_list.types[self.cb_choice_dfft.current()]
    self.cb_imtype_dfft.current(0)


def dfft_1up_bind(event, self):
    val = int(self.vec1_py_entry.get()) + 1
    self.vec1_py_entry.delete(0, tk.END)
    self.vec1_py_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[0][1][1] = val
    show_image_dfft(self)


def dfft_1down_bind(event, self):
    val = int(self.vec1_py_entry.get()) - 1
    self.vec1_py_entry.delete(0, tk.END)
    self.vec1_py_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[0][1][1] = val
    show_image_dfft(self)


def dfft_1right_bind(event, self):
    val = int(self.vec1_px_entry.get()) + 1
    self.vec1_px_entry.delete(0, tk.END)
    self.vec1_px_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[0][1][0] = val
    show_image_dfft(self)


def dfft_1left_bind(event, self):
    val = int(self.vec1_px_entry.get()) - 1
    self.vec1_px_entry.delete(0, tk.END)
    self.vec1_px_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[0][1][0] = val
    show_image_dfft(self)


def dfft_1return_bind(event, self):
    self.image_drift_fft.line_points[0][1][0] = int(self.vec1_px_entry.get())
    self.image_drift_fft.line_points[0][1][1] = int(self.vec1_py_entry.get())
    show_image_dfft(self)


def dfft_2up_bind(event, self):
    val = int(self.vec2_py_entry.get()) + 1
    self.vec2_py_entry.delete(0, tk.END)
    self.vec2_py_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[1][1][1] = val
    show_image_dfft(self)


def dfft_2down_bind(event, self):
    val = int(self.vec2_py_entry.get()) - 1
    self.vec2_py_entry.delete(0, tk.END)
    self.vec2_py_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[1][1][1] = val
    show_image_dfft(self)


def dfft_2right_bind(event, self):
    val = int(self.vec2_px_entry.get()) + 1
    self.vec2_px_entry.delete(0, tk.END)
    self.vec2_px_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[1][1][0] = val
    show_image_dfft(self)


def dfft_2left_bind(event, self):
    val = int(self.vec2_px_entry.get()) - 1
    self.vec2_px_entry.delete(0, tk.END)
    self.vec2_px_entry.insert(tk.END, val)
    self.image_drift_fft.line_points[1][1][0] = val
    show_image_dfft(self)


def dfft_2return_bind(event, self):
    self.image_drift_fft.line_points[1][1][0] = int(self.vec2_px_entry.get())
    self.image_drift_fft.line_points[1][1][1] = int(self.vec2_py_entry.get())
    show_image_dfft(self)


def read_dfft_clicked(self):
    read_image_dfft(self)
    update_dfft(self)
    show_image_dfft(self)


def read_image_dfft(self):
    self.image_drift_real.open_bool = True
    self.image_drift_real.data_path = (
        self.image_list.dir_name + "\\" + self.cb_choice_dfft.get()
    )
    self.image_drift_real.channel_val = self.cb_imtype_dfft.current()
    self.image_drift_real.read_image()
    self.dfft_size_x_entry.delete(0, tk.END)
    self.dfft_size_x_entry.insert(tk.END, self.image_drift_real.x_size_or)
    self.dfft_size_y_entry.delete(0, tk.END)
    self.dfft_size_y_entry.insert(tk.END, self.image_drift_real.y_size_or)


def update_dfft(self):
    self.fft_drift.method = self.method_fft_cb_dfft.get()
    self.fft_drift.window_func = self.window_cb_dfft.get()
    self.fft_drift.image = self.image_drift_real.image_mod
    self.fft_drift.size_real_x = self.real_image.x_current
    self.fft_drift.size_real_y = self.real_image.y_current
    image = self.fft_drift.run()
    self.image_drift_fft.image_or = np.copy(image)
    self.image_drift_fft.image_mod = np.copy(image)
    self.image_drift_fft.x_size_or = self.fft_drift.x_size
    self.image_drift_fft.y_size_or = self.fft_drift.y_size
    self.dfft_size_x_FFT["text"] = str(round(self.fft_drift.x_size, 2))
    self.dfft_size_y_FFT["text"] = str(round(self.fft_drift.y_size, 2))
    self.drift_val_change()


def show_image_dfft(self):
    if self.dfft_FFT:
        self.rescale_dfft.image = self.image_drift_fft.image_or
        self.image_drift_fft.image_mod = self.rescale_dfft.run()
        self.image_drift_fft.show_image()
    else:
        self.rescale_dfft.image = self.image_drift_real.image_or
        self.image_drift_real.image_mod = self.rescale_dfft.run()
        self.image_drift_real.show_image()
    put_values_dfft(self)


def size_bind(event, self):
    self.image_drift_real.x_size_or = float(self.dfft_size_x_entry.get())
    self.image_drift_real.y_size_or = float(self.dfft_size_y_entry.get())
    update_dfft(self)


def fft_function_dfft(self):
    if self.dfft_FFT:
        self.dfft_FFT = False
        self.fft_button_dfft["text"] = "Real\r→FFT"

    else:
        self.dfft_FFT = True
        self.fft_button_dfft["text"] = "FFT→\rReal"
    show_image_dfft(self)


def cb_method_selected_dfft(event, self):
    update_dfft(self)
    show_image_dfft(self)


def cb_window_selected_dfft(event, self):
    update_dfft(self)
    show_image_dfft(self)


def reset_dfft(self):
    reset_arrow_dfft(self)
    show_image_dfft(self)


def close_dfft(self):
    try:
        cv2.destroyWindow("Arrow")
    except:
        pass
    self.drift_fix_fft_open = False
    self.fft_fix_window.destroy()


def reset_arrow_dfft(self):
    fft_x, fft_y = self.image_drift_fft.image_mod.shape[:2]
    fft_center_x = int(fft_x / 2)
    fft_center_y = int(fft_y / 2)
    fft_x1 = int(fft_x / 4 * 3)
    fft_y1 = int(fft_y / 2)
    fft_x2 = int(fft_x / 4 * 3)
    fft_y2 = int(fft_y / 4)
    self.image_drift_fft.line_points = np.array(
        [
            [[fft_center_x, fft_center_y], [fft_x1, fft_y1]],
            [[fft_center_x, fft_center_y], [fft_x2, fft_y2]],
        ],
    )
    self.image_drift_fft.line_points_active([[False, True], [False, True]])
    show_image_dfft(self)


def mag_bind(event, self):
    self.rescale_dfft.all = float(self.dfft_mag_entry.get())
    self.image_drift_fft.line_points = (
        self.image_drift_fft.line_points * self.rescale_dfft.all / self.prev_mag
    )
    self.prev_mag = float(self.dfft_mag_entry.get())
    show_image_dfft(self)


def convert_FFT_real(FFT_x1, FFT_y1, FFT_x2, FFT_y2):
    # unit vector in real space
    """
    xr1 = 2 * math.pi / (FFT_x1 * FFT_y2 - FFT_y1 * FFT_x2) * FFT_y2
    yr1 = -2 * math.pi / (FFT_x1 * FFT_y2 - FFT_y1 * FFT_x2) * FFT_x2
    xr2 = 2 * math.pi / (FFT_x2 * FFT_y1 - FFT_y2 * FFT_x1) * FFT_y1
    yr2 = -2 * math.pi / (FFT_x2 * FFT_y1 - FFT_y2 * FFT_x1) * FFT_x1

    """
    xr1 = 1 / (FFT_x1 * FFT_y2 - FFT_y1 * FFT_x2) * FFT_y2
    yr1 = -1 / (FFT_x1 * FFT_y2 - FFT_y1 * FFT_x2) * FFT_x2
    xr2 = 1 / (FFT_x2 * FFT_y1 - FFT_y2 * FFT_x1) * FFT_y1
    yr2 = -1 / (FFT_x2 * FFT_y1 - FFT_y2 * FFT_x1) * FFT_x1
    return xr1, yr1, xr2, yr2


def get_polar(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta


def put_values_dfft(self):
    fft_x, fft_y = self.image_drift_fft.image_mod.shape[:2]
    center_x = fft_x / 2
    center_y = fft_y / 2
    vec1_x = (
        (int(self.vec1_px_entry.get()) - center_x)
        / fft_x
        * self.image_drift_fft.x_current
    )
    vec1_y = (
        (center_y - int(self.vec1_py_entry.get()))
        / fft_y
        * self.image_drift_fft.y_current
    )
    vec2_x = (
        (int(self.vec2_px_entry.get()) - center_x)
        / fft_x
        * self.image_drift_fft.x_current
    )
    vec2_y = (
        (center_y - int(self.vec2_py_entry.get()))
        / fft_y
        * self.image_drift_fft.y_current
    )
    #
    r1, theta1 = get_polar(vec1_x, vec1_y)
    r2, theta2 = get_polar(vec2_x, vec2_y)
    #
    self.x1_real, self.y1_real, self.x2_real, self.y2_real = convert_FFT_real(
        vec1_x, vec1_y, vec2_x, vec2_y
    )
    #
    r1_real, theta1_real = get_polar(self.x1_real, self.y1_real)
    r2_real, theta2_real = get_polar(self.x2_real, self.y2_real)
    #
    self.dfft_k1_label["text"] = str(round(r1, 2)) + " nm-1"
    self.dfft_k1_angle_label["text"] = str(round(-theta1 / math.pi * 180, 2)) + " °"
    self.dfft_k2_label["text"] = str(round(r2, 2)) + " nm-1"
    self.dfft_k2_angle_label["text"] = str(round(-theta2 / math.pi * 180, 2)) + " °"
    #
    self.dfft_r1_label["text"] = str(round(r1_real, 2)) + " nm"
    self.dfft_r1_angle_label["text"] = (
        str(round(-theta1_real / math.pi * 180, 2)) + " °"
    )
    self.dfft_r2_label["text"] = str(round(r2_real, 2)) + " nm"
    self.dfft_r2_angle_label["text"] = (
        str(round(-theta2_real / math.pi * 180, 2)) + " °"
    )
    #
    self.dfft_ratio_val["text"] = str(round(r2_real / r1_real, 2))
    self.dfft_dif_angle_val["text"] = str(
        round((theta2_real - theta1_real) / math.pi * 180, 2)
    )


def drift_fft(self):
    self.fft_fix_window = tk.Toplevel()
    self.fft_fix_window.title("Drift fix (FFT)")
    prepare_widgets(self)
    initial_setting_dfft(self)
    self.fft_fix_window.protocol("WM_DELETE_WINDOW", lambda: close_dfft(self))


def get_theta(v, w, self):
    L = float(self.dfft_size_x_entry.get())
    a = self.x1_real
    b = self.y1_real
    c = self.x2_real
    d = self.y2_real

    av1x = a + b / L * v
    av1y = b + b / L * w
    av2x = c + d / L * v
    av2y = d + d / L * w

    atheta1 = math.atan2(av1y, av1x)
    atheta2 = math.atan2(av2y, av2x)

    dtheta = abs(-atheta1 + atheta2)
    otheta = float(self.dfft_set_angle_entry.get())

    theta_diff = abs(dtheta * 180 / math.pi - otheta)

    return theta_diff


def calculate_drift_dfft(self):
    L = float(self.dfft_size_y_entry.get())
    a = self.x1_real
    b = self.y1_real
    c = self.x2_real
    d = self.y2_real
    r = float(self.dfft_set_ratio_entry.get())
    k = math.cos(math.radians(float(self.dfft_set_angle_entry.get())))

    v = (k * r * (b * c + a * d) - r**2 * a * b - c * d) / (
        r**2 * b**2 - 2 * k * r * b * d + d**2
    )
    sqrt = (
        -(v**2)
        + 2 * (c * d - r**2 * a * b) * v / (r**2 * b**2 - d**2)
        + (c**2 - r**2 * a**2) / (r**2 * b**2 - d**2)
    )
    w1 = -math.sqrt(sqrt) - 1
    w2 = math.sqrt(sqrt) - 1

    v = L * v
    w1 = L * w1
    w2 = L * w2

    the1 = get_theta(v, w1, self)
    the2 = get_theta(v, w2, self)

    if the1 < the2:
        w = w1
    else:
        w = w2
    fix_check(v, w, self)
    return v, w


def fix_check(v, w, self):
    L = float(self.dfft_size_y_entry.get())
    fft_x, fft_y = self.image_drift_fft.image_mod.shape[:2]
    v11 = 1 + v / 2 / fft_y / L
    v12 = v / L
    v21 = w / 2 / fft_y
    v22 = 1 + w / L
    n_vec1 = [
        self.x1_real * v11 + self.y1_real * v12,
        self.x1_real * v21 + self.y1_real * v22,
    ]
    n_vec2 = [
        self.x2_real * v11 + self.y2_real * v12,
        self.x2_real * v21 + self.y2_real * v22,
    ]
    abs_v1 = math.sqrt(n_vec1[0] ** 2 + n_vec1[1] ** 2)
    abs_v2 = math.sqrt(n_vec2[0] ** 2 + n_vec2[1] ** 2)

    ratio = abs_v2 / abs_v1
    angle = (
        math.acos((n_vec1[0] * n_vec2[0] + n_vec1[1] * n_vec2[1]) / abs_v1 / abs_v2)
        / math.pi
        * 180
    )
    self.dfft_val_check_label["text"] = (
        "Calculated value: "
        + "\t"
        + "v = "
        + str(round(v, 3))
        + ", "
        + "w = "
        + str(round(w, 3))
        + "\n"
        + "Correction check: "
        + "Ratio: "
        + str(round(ratio, 3))
        + ", "
        + "Angle: "
        + str(round(angle, 3))
    )


def calculate_dfft(self):
    self.v, self.w = calculate_drift_dfft(self)
    self.drift_dx.delete(0, tk.END)
    self.drift_dx.insert(tk.END, round(self.v, 2))
    self.drift_dy.delete(0, tk.END)
    self.drift_dy.insert(tk.END, round(self.w, 2))
    self.drift_val_change()
