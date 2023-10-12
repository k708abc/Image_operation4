import tkinter.ttk as ttk
import tkinter as tk
import cv2
import numpy as np
from Modules.image_class import MyImage


def start_setting_drift(self):
    self.image_ref1 = MyImage()
    self.image_ref2 = MyImage()
    self.ref1_xreal = 0
    self.ref1_yreal = 0
    self.ref2_xreal = 0
    self.ref2_yreal = 0
    self.dx = 0
    self.dy = 0
    self.shift_x = 0
    self.shift_y = 0
    self.magnitude = 1


def prepare_widdgets(self):
    create_frame_ref_choise(self)
    create_frame_others(self)


def create_frame_ref_choise(self):
    self.frame_ref_choise = ttk.Frame(self.two_image_window)
    create_widgets_ref_choise(self)
    create_layout_ref_choise(self)
    self.frame_ref_choise.pack()


def create_widgets_ref_choise(self):
    # ref1
    self.var_cb_image_first = tk.StringVar()
    self.cb_first_image = ttk.Combobox(
        self.frame_ref_choise,
        textvariable=self.var_cb_image_first,
        values=self.image_list.images,
        width=40,
    )
    self.cb_first_image.bind(
        "<<ComboboxSelected>>", lambda event, arg=self: ref1_selected(event, arg)
    )
    if len(self.image_list.images) > 0:
        self.cb_first_image.current(0)
    #
    self.cblabel_ref1 = tk.Label(self.frame_ref_choise, text="Reference 1")
    #
    self.var_ref1_imtypes = tk.StringVar()
    self.imtype_ref1_choise = ttk.Combobox(
        self.frame_ref_choise,
        textvariable=self.var_ref1_imtypes,
        width=40,
    )
    if len(self.image_list.types) > 0:
        self.imtype_ref1_choise["values"] = self.image_list.types[0]
        self.imtype_ref1_choise.current(0)
    #
    self.button_ref1_open = tk.Button(
        self.frame_ref_choise, text="Open", command=lambda: ref1_open(self), width=10
    )
    #
    self.label_ref1_size = tk.Label(self.frame_ref_choise, text="Size (nm)")
    self.ref1_size_entry = ttk.Entry(self.frame_ref_choise, width=7)
    self.ref1_size_entry.insert(tk.END, "0")
    self.ref1_size_entry.bind("<Return>", lambda event, arg=self: size_bind(event, arg))
    #
    # ref2
    self.var_cb_image_second = tk.StringVar()
    self.cb_second_image = ttk.Combobox(
        self.frame_ref_choise,
        textvariable=self.var_cb_image_second,
        values=self.image_list.images,
        width=40,
    )
    if len(self.image_list.images) > 0:
        self.cb_second_image.current(0)
    #
    self.cblabel_ref2 = tk.Label(self.frame_ref_choise, text="Reference 2")
    #
    self.var_ref2_imtypes = tk.StringVar()
    self.imtype_ref2_choise = ttk.Combobox(
        self.frame_ref_choise,
        textvariable=self.var_ref2_imtypes,
        width=40,
    )
    if len(self.image_list.types) > 0:
        self.imtype_ref2_choise["values"] = self.image_list.types[0]
        self.imtype_ref2_choise.current(0)
    #
    self.cb_second_image.bind(
        "<<ComboboxSelected>>", lambda event, arg=self: ref2_selected(event, arg)
    )
    #
    self.button_ref2_open = tk.Button(
        self.frame_ref_choise, text="Open", command=lambda: ref2_open(self), width=10
    )
    #
    self.label_ref2_size = tk.Label(self.frame_ref_choise, text="Size (nm)")

    self.ref2_size_entry = ttk.Entry(self.frame_ref_choise, width=7)
    self.ref2_size_entry.insert(tk.END, "0")
    self.ref2_size_entry.bind("<Return>", lambda event, arg=self: size_bind(event, arg))
    #


def create_layout_ref_choise(self):
    self.cb_first_image.grid(columnspan=2, row=0, column=1, **self.padWE)
    self.cblabel_ref1.grid(row=0, column=0, **self.padWE)
    self.imtype_ref1_choise.grid(columnspan=2, row=1, column=1, **self.padWE)
    self.button_ref1_open.grid(
        rowspan=2, row=0, column=3, sticky=tk.N + tk.S, padx=15, pady=2
    )

    self.label_ref1_size.grid(row=2, column=1, **self.padWE)
    self.ref1_size_entry.grid(row=2, column=2, **self.padWE)

    #
    self.cb_second_image.grid(columnspan=2, row=4, column=1, **self.padWE)
    self.cblabel_ref2.grid(row=4, column=0, **self.padWE)
    self.imtype_ref2_choise.grid(columnspan=2, row=5, column=1, **self.padWE)
    self.button_ref2_open.grid(
        rowspan=2, row=4, column=3, sticky=tk.N + tk.S, padx=15, pady=2
    )

    self.label_ref2_size.grid(row=6, column=1, **self.padWE)
    self.ref2_size_entry.grid(row=6, column=2, **self.padWE)


def create_frame_others(self):
    self.frame_others = ttk.Frame(self.two_image_window)
    create_widgets_others(self)
    create_layout_others(self)
    self.frame_others.pack()


def create_widgets_others(self):
    self.magnify_drift_text = tk.Label(self.frame_others, text="Enlarge")
    self.magnify_drift_entry = ttk.Entry(self.frame_others, width=7)
    self.magnify_drift_entry.insert(tk.END, "1")
    self.magnify_drift_entry.bind(
        "<Return>", lambda event, arg=self: magnify_drift_bind(event, arg)
    )
    #
    self.button_diff = ttk.Button(
        self.frame_others, text="Difference", command=lambda: apply_diff(self)
    )
    self.button_corr = ttk.Button(
        self.frame_others, text="Correlation", command=lambda: apply_corr(self)
    )

    #

    self.label_diff = tk.Label(self.frame_others, text="(dx, dy) = (0.0, 0.0)")
    self.label_corr = tk.Label(self.frame_others, text="(dx, dy) = (0.0, 0.0)")
    #

    self.button_close = ttk.Button(
        self.frame_others, text="Close", command=lambda: close_drift_fix(self)
    )


def create_layout_others(self):
    self.magnify_drift_text.grid(row=0, column=0, **self.padWE)
    self.magnify_drift_entry.grid(row=0, column=1, **self.padWE)
    self.button_diff.grid(row=1, column=0, sticky=tk.N + tk.S, padx=15, pady=2)
    self.button_corr.grid(row=2, column=0, sticky=tk.N + tk.S, padx=15, pady=2)
    self.label_diff.grid(row=1, column=1, **self.padWE)
    self.label_corr.grid(row=2, column=1, **self.padWE)

    self.button_close.grid(
        rowspan=2, row=1, column=3, sticky=tk.N + tk.S, padx=15, pady=2
    )


def ref1_selected(event, self):
    self.imtype_ref1_choise["values"] = self.image_list.types[
        self.cb_first_image.current()
    ]
    self.imtype_ref1_choise.current(0)


def ref1_open(self):
    self.image_ref1.open_bool = True
    self.corr_calculated = False
    self.image_ref1.mouse_on = True
    self.image_ref1.image_name = "Reference 1"
    read_ref1(self)
    self.image_ref1.show_image()


def ref2_selected(event, self):
    self.imtype_ref2_choise["values"] = self.image_list.types[
        self.cb_second_image.current()
    ]
    self.imtype_ref2_choise.current(0)


def ref2_open(self):
    self.image_ref2.open_bool = True
    self.corr_calculated = False
    self.image_ref2.mouse_on = True
    self.image_ref2.image_name = "Reference 2"
    read_ref2(self)
    self.image_ref2.show_image()


def read_ref1(self):
    self.image_ref1.data_path = (
        self.image_list.dir_name + "\\" + self.cb_first_image.get()
    )
    self.image_ref1.channel_val = self.imtype_ref1_choise.current()
    self.image_ref1.read_image()
    #
    self.ref1_size_entry.delete(0, tk.END)
    self.ref1_size_entry.insert(tk.END, self.image_ref1.x_size_or)
    self.image_ref1.image_mod = image_resize(self, self.image_ref1.image_mod)


def read_ref2(self):
    self.image_ref2.data_path = (
        self.image_list.dir_name + "\\" + self.cb_second_image.get()
    )
    self.image_ref2.channel_val = self.imtype_ref2_choise.current()
    self.image_ref2.read_image()
    #
    self.ref2_size_entry.delete(0, tk.END)
    self.ref2_size_entry.insert(tk.END, self.image_ref2.x_size_or)
    self.image_ref2.image_mod = image_resize(self, self.image_ref2.image_mod)


def image_resize(self, image):
    height, width = image.shape[0], image.shape[1]
    width_x = int(width * self.magnitude)
    height_y = int(height * self.magnitude)
    image_re = cv2.resize(image, (width_x, height_y))
    return image_re


def magnify_drift_bind(event, self):
    self.magnitude_new = float(self.magnify_drift_entry.get())
    self.image_ref1.mouse_x = int(
        self.image_ref1.mouse_x * self.magnitude_new / self.magnitude
    )
    self.image_ref1.mouse_y = int(
        self.image_ref1.mouse_y * self.magnitude_new / self.magnitude
    )
    self.image_ref2.mouse_x = int(
        self.image_ref2.mouse_x * self.magnitude_new / self.magnitude
    )
    self.image_ref2.mouse_y = int(
        self.image_ref2.mouse_y * self.magnitude_new / self.magnitude
    )

    self.magnitude = float(self.magnify_drift_entry.get())
    if self.image_ref1.open_bool:
        self.image_ref1.image_mod = image_resize(self, self.image_ref1.image_mod)
        self.image_ref1.show_image()
    if self.image_ref2.open_bool:
        self.image_ref2.image_mod = image_resize(self, self.image_ref2.image_mod)
        self.image_ref2.show_image()


def cal_diff(self):
    if self.image_ref1.open_bool:
        height, width = self.image_ref1.image_mod.shape[:2]
        self.ref1_xreal = (
            self.image_ref1.mouse_x / width * float(self.ref1_size_entry.get())
        )
        self.ref1_yreal = (
            self.image_ref1.mouse_y / height * float(self.ref1_size_entry.get())
        )
    #
    if self.image_ref2.open_bool:
        height, width = self.image_ref2.image_mod.shape[:2]
        self.ref2_xreal = (
            self.image_ref2.mouse_x / width * float(self.ref2_size_entry.get())
        )
        self.ref2_yreal = (
            self.image_ref2.mouse_y / height * float(self.ref2_size_entry.get())
        )
    self.dx = self.ref2_xreal - self.ref1_xreal
    self.dy = self.ref2_yreal - self.ref1_yreal


def apply_diff(self):
    cal_diff(self)
    self.label_diff["text"] = (
        "(dx, dy) = "
        + "("
        + str(round(self.dx, 2))
        + ", "
        + str(round(self.dy, 2))
        + ")"
    )
    update_original(self, self.dx, self.dy)


def apply_corr(self):
    if self.image_ref1.open_bool and self.image_ref2.open_bool:
        self.width_corr, self.height_corr = self.image_ref1.image_show.shape[:2]
        image_dst = self.image_ref1.image_show[
            int(self.height_corr / 4) : int(self.height_corr * 3 / 4),
            int(self.width_corr / 4) : int(self.width_corr * 3 / 4),
        ]
        corr = cv2.matchTemplate(
            self.image_ref2.image_show, image_dst, cv2.TM_CCORR_NORMED
        )
        self.i_rec, self.k_rec = np.unravel_index(np.argmax(corr), corr.shape)
        corr_val_update(self)
        update_original(self, self.shift_x, self.shift_y)


def cal_vw(self, dx, dy):
    N = self.image_ref1.image_show.shape[0]
    L = float(self.ref1_size_entry.get())
    v = -dx / (1 + dx / 2 / N / L + dy / L)
    w = -dy / (1 + dx / 2 / N / L + dy / L)
    return v, w


def update_original(self, dx, dy):
    v, w = cal_vw(self, dx, dy)
    self.drift_dx.delete(0, tk.END)
    self.drift_dx.insert(tk.END, round(v, 2))
    self.drift_dy.delete(0, tk.END)
    self.drift_dy.insert(tk.END, round(w, 2))
    # 画像のアップデート


def close_drift_fix(self):
    if self.image_ref1.open_bool:
        self.image_ref1.des_image()
    if self.image_ref2.open_bool:
        self.image_ref2.des_image()
    self.two_image_window.destroy()


def corr_val_update(self):
    size_x = float(self.ref1_size_entry.get())
    size_y = float(self.ref2_size_entry.get())
    self.shift_x = (
        (self.k_rec + int(self.width_corr / 4) - int(self.width_corr / 2))
        / self.height_corr
        * size_x
    )
    self.shift_y = (
        (self.i_rec + int(self.height_corr / 4) - int(self.height_corr / 2))
        / self.width_corr
        * size_y
    )
    self.label_corr["text"] = (
        "(dx, dy) = "
        + "("
        + str(round(self.shift_x, 2))
        + ", "
        + str(round(self.shift_y, 2))
        + ")"
    )


def size_bind(event, self):
    cal_diff(self)
    corr_val_update(self)


def drift_two_images(self):
    self.two_image_window = tk.Toplevel()
    self.two_image_window.title("Drift fix (Two images)")
    start_setting_drift(self)
    prepare_widdgets(self)
    self.two_image_window.protocol("WM_DELETE_WINDOW", lambda: close_drift_fix(self))
