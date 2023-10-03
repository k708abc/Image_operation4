import tkinter.ttk as ttk
import tkinter as tk
import cv2
import numpy as np


def start_setting_drift(self):

    self.ref_1_selected = False
    self.ref_2_selected = False
    self.ref1_x = 0
    self.ref1_y = 0
    self.ref2_x = 0
    self.ref2_y = 0
    self.ref1_xreal = 0
    self.ref1_yreal = 0
    self.ref2_xreal = 0
    self.ref2_yreal = 0
    self.dx = 0
    self.dy = 0
    self.shift_x = 0
    self.shift_y = 0
    self.color = (0, 0, 255)
    self.thickness = 2
    self.magnitude = 1
    self.corr_calculated = False


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
        values=self.image_list,
        width=40,
    )
    self.cb_first_image.bind(
        "<<ComboboxSelected>>", lambda event, arg=self: ref1_selected(event, arg)
    )
    #
    self.cblabel_ref1 = tk.Label(self.frame_ref_choise, text="Reference 1")
    #
    self.imtype_list_ref1 = []
    self.var_ref1_imtypes = tk.StringVar()
    self.imtype_ref1_choise = ttk.Combobox(
        self.frame_ref_choise,
        textvariable=self.var_ref1_imtypes,
        values=self.imtype_list_ref1,
        width=40,
    )
    #
    self.button_ref1_open = tk.Button(
        self.frame_ref_choise, text="Open", command=lambda: ref1_open(self), width=10
    )
    self.button_ref1_open["state"] = tk.DISABLED
    #
    self.ref1_pixcel = tk.Label(self.frame_ref_choise, text="Pixcel: ")
    self.label_ref1 = tk.Label(
        self.frame_ref_choise, text="(x, y) = " + "(" + "0" + ", " + "0" + ")"
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
        values=self.image_list,
        width=40,
    )

    #
    self.cblabel_ref2 = tk.Label(self.frame_ref_choise, text="Reference 2")
    #
    self.imtype_list_ref2 = []
    self.var_ref2_imtypes = tk.StringVar()
    self.imtype_ref2_choise = ttk.Combobox(
        self.frame_ref_choise,
        textvariable=self.var_ref2_imtypes,
        values=self.imtype_list_ref2,
        width=40,
    )
    self.cb_second_image.bind(
        "<<ComboboxSelected>>", lambda event, arg=self: ref2_selected(event, arg)
    )
    #
    self.button_ref2_open = tk.Button(
        self.frame_ref_choise, text="Open", command=lambda: ref2_open(self), width=10
    )
    self.button_ref2_open["state"] = tk.DISABLED
    #
    self.ref2_pixcel = tk.Label(self.frame_ref_choise, text="Pixcel: ")
    self.label_ref2 = tk.Label(
        self.frame_ref_choise, text="(x, y) = " + "(" + "0" + ", " + "0" + ")"
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

    self.ref1_pixcel.grid(row=3, column=1, **self.padWE)
    self.label_ref1.grid(row=3, column=2, **self.padWE)

    #
    self.cb_second_image.grid(columnspan=2, row=4, column=1, **self.padWE)
    self.cblabel_ref2.grid(row=4, column=0, **self.padWE)
    self.imtype_ref2_choise.grid(columnspan=2, row=5, column=1, **self.padWE)
    self.button_ref2_open.grid(
        rowspan=2, row=4, column=3, sticky=tk.N + tk.S, padx=15, pady=2
    )

    self.label_ref2_size.grid(row=6, column=1, **self.padWE)
    self.ref2_size_entry.grid(row=6, column=2, **self.padWE)
    self.ref2_pixcel.grid(row=7, column=1, **self.padWE)
    self.label_ref2.grid(row=7, column=2, **self.padWE)


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
    self.bln_diff = tk.BooleanVar()
    self.bln_diff.set(True)
    self.chk_diff = tk.Checkbutton(
        self.frame_others,
        variable=self.bln_diff,
        text="Difference",
        command=lambda: chk_diff_clicked(self),
    )
    #
    self.bln_corr = tk.BooleanVar()
    self.bln_corr.set(False)
    self.chk_corr = tk.Checkbutton(
        self.frame_others,
        variable=self.bln_corr,
        text="Correlate",
        command=lambda: chk_corr_clicked(self),
    )
    self.label_diff = tk.Label(self.frame_others, text="(dx, dy) = (0.0, 0.0)")
    self.label_corr = tk.Label(self.frame_others, text="(dx, dy) = (0.0, 0.0)")
    #
    self.button_apply = ttk.Button(
        self.frame_others, text="Apply", command=lambda: apply_drift_fix(self)
    )
    self.button_close = ttk.Button(
        self.frame_others, text="Close", command=lambda: close_drift_fix(self)
    )


def create_layout_others(self):
    self.magnify_drift_text.grid(row=0, column=0, **self.padWE)
    self.magnify_drift_entry.grid(row=0, column=1, **self.padWE)
    self.chk_diff.grid(row=1, column=0, **self.padWE)
    self.chk_corr.grid(row=2, column=0, **self.padWE)
    self.label_diff.grid(row=1, column=1, **self.padWE)
    self.label_corr.grid(row=2, column=1, **self.padWE)
    self.button_apply.grid(
        rowspan=2, row=1, column=2, sticky=tk.N + tk.S, padx=15, pady=2
    )
    self.button_close.grid(
        rowspan=2, row=1, column=3, sticky=tk.N + tk.S, padx=15, pady=2
    )


def ref1_selected(event, self):
    self.button_ref1_open["state"] = tk.NORMAL
    self.data_path = self.dir_name + "\\" + self.cb_first_image.get()
    self.imtype_list_ref1 = self.get_datatypes(self.data_path)
    self.imtype_ref1_choise["values"] = self.imtype_list_ref1
    self.imtype_ref1_choise.current(0)
    self.two_image_window.update()


def ref1_open(self):
    self.ref_1_selected = True
    self.corr_calculated = False
    cv2.namedWindow("Reference 1")
    cv2.setMouseCallback("Reference 1", mouse_event_ref1, self)
    read_ref1(self)
    ref1_pixcels(self)
    show_ref1(self)
    if self.bln_corr.get():
        chk_corr_clicked(self)


def ref2_selected(event, self):
    self.button_ref2_open["state"] = tk.NORMAL
    self.data_path = self.dir_name + "\\" + self.cb_second_image.get()
    self.imtype_list_ref2 = self.get_datatypes(self.data_path)
    self.imtype_ref2_choise["values"] = self.imtype_list_ref2
    self.imtype_ref2_choise.current(0)
    self.two_image_window.update()


def ref2_open(self):
    self.ref_2_selected = True
    self.corr_calculated = False
    cv2.namedWindow("Reference 2")
    cv2.setMouseCallback("Reference 2", mouse_event_ref2, self)
    read_ref2(self)
    ref2_pixcels(self)
    show_ref2(self)
    if self.bln_corr.get():
        chk_corr_clicked(self)


def read_ref1(self):
    self.data_path = self.dir_name + "\\" + self.cb_first_image.get()
    self.channel_type = self.imtype_ref1_choise.current()
    #
    self.image_ref1_or, self.ref1_params, _ = self.get_image_values(
        self.data_path, self.channel_type
    )
    self.image_ref1_or = (self.image_ref1_or - np.min(self.image_ref1_or)) / (
        np.max(self.image_ref1_or) - np.min(self.image_ref1_or)
    )

    self.image_ref1_or = cv2.cvtColor(
        self.image_ref1_or.astype(np.float32), cv2.COLOR_GRAY2BGR
    )
    self.ref1_size_entry.delete(0, tk.END)
    self.ref1_size_entry.insert(tk.END, self.ref1_params[0])
    self.image_ref1_re = image_resize(self, self.image_ref1_or)


def show_ref1(self):
    self.image_ref1 = np.copy(self.image_ref1_re)
    putcircle(self.image_ref1, self.thickness, self.ref1_x, self.ref1_y)
    cal_diff(self)
    cv2.imshow("Reference 1", self.image_ref1)


def read_ref2(self):
    self.data_path = self.dir_name + "\\" + self.cb_second_image.get()
    self.channel_type = self.imtype_ref2_choise.current()
    #
    self.image_ref2_or, self.ref2_params, _ = self.get_image_values(
        self.data_path, self.channel_type
    )
    self.image_ref2_or = (self.image_ref2_or - np.min(self.image_ref2_or)) / (
        np.max(self.image_ref2_or) - np.min(self.image_ref2_or)
    )
    self.image_ref2_or = cv2.cvtColor(
        self.image_ref2_or.astype(np.float32), cv2.COLOR_GRAY2BGR
    )
    self.ref2_size_entry.delete(0, tk.END)
    self.ref2_size_entry.insert(tk.END, self.ref2_params[0])
    self.image_ref2_re = image_resize(self, self.image_ref2_or)


def show_ref2(self):
    self.image_ref2 = np.copy(self.image_ref2_re)
    putcircle(self.image_ref2, self.thickness, self.ref2_x, self.ref2_y)
    cal_diff(self)
    cv2.imshow("Reference 2", self.image_ref2)


def putcircle(image, thickness, x, y):
    cv2.circle(image, (x, y), thickness, (0, 0, 255), -1)


def mouse_event_ref1(event, x, y, flags, self):
    if event == cv2.EVENT_LBUTTONUP:
        self.ref1_x = x
        self.ref1_y = y
        self.image_ref1 = np.copy(self.image_ref1_or)
        show_ref1(self)


def mouse_event_ref2(event, x, y, flags, self):
    if event == cv2.EVENT_LBUTTONUP:
        self.ref2_x = x
        self.ref2_y = y
        self.image_ref2 = np.copy(self.image_ref2_or)
        show_ref2(self)


def ref1_pixcels(self):
    self.ref1_pixcel["text"] = (
        "Pixcel: "
        + str(len(self.image_ref1_or[0]))
        + "×"
        + str(len(self.image_ref1_or))
    )


def ref2_pixcels(self):
    self.ref2_pixcel["text"] = (
        "Pixcel: "
        + str(len(self.image_ref2_or[0]))
        + "×"
        + str(len(self.image_ref2_or))
    )


def cal_diff(self):
    if self.ref_1_selected:
        self.ref1_xreal = (
            self.ref1_x / len(self.image_ref1[0]) * float(self.ref1_size_entry.get())
        )
        self.ref1_yreal = (
            self.ref1_y / len(self.image_ref1) * float(self.ref1_size_entry.get())
        )
        self.label_ref1["text"] = (
            "(x, y) = "
            + "("
            + str(round(self.ref1_xreal, 2))
            + ", "
            + str(round(self.ref1_yreal, 2))
            + ")"
        )
    #
    if self.ref_2_selected:
        self.ref2_xreal = (
            self.ref2_x / len(self.image_ref2[0]) * float(self.ref2_size_entry.get())
        )
        self.ref2_yreal = (
            self.ref2_y / len(self.image_ref2) * float(self.ref2_size_entry.get())
        )
        self.label_ref2["text"] = (
            "(x, y) = "
            + "("
            + str(round(self.ref2_xreal, 2))
            + ", "
            + str(round(self.ref2_yreal, 2))
            + ")"
        )
    self.dx = self.ref2_xreal - self.ref1_xreal
    self.dy = self.ref2_yreal - self.ref1_yreal
    self.label_diff["text"] = (
        "(dx, dy) = "
        + "("
        + str(round(self.dx, 2))
        + ", "
        + str(round(self.dy, 2))
        + ")"
    )
    self.two_image_window.update()


def image_resize(self, image):
    height, width = image.shape[0], image.shape[1]
    width_x = int(width * self.magnitude)
    height_y = int(height * self.magnitude)
    image_re = cv2.resize(image, (width_x, height_y))
    return image_re


def magnify_drift_bind(event, self):
    self.magnitude_new = float(self.magnify_drift_entry.get())
    self.ref1_x = int(self.ref1_x * self.magnitude_new / self.magnitude)
    self.ref1_y = int(self.ref1_y * self.magnitude_new / self.magnitude)
    self.ref2_x = int(self.ref2_x * self.magnitude_new / self.magnitude)
    self.ref2_y = int(self.ref2_y * self.magnitude_new / self.magnitude)
    self.magnitude = float(self.magnify_drift_entry.get())
    if self.ref_1_selected:
        self.image_ref1_re = image_resize(self, self.image_ref1_or)
        show_ref1(self)
        ref1_pixcels(self)
    if self.ref_2_selected:
        self.image_ref2_re = image_resize(self, self.image_ref2_or)
        show_ref2(self)
        ref2_pixcels(self)


def chk_diff_clicked(self):
    self.bln_corr.set(False)
    self.bln_diff.set(True)


def chk_corr_clicked(self):
    if self.ref_1_selected and self.ref_2_selected:
        if self.corr_calculated is False:
            self.corr_calculated = True
            get_corr(self)
            corr_val_update(self)
            self.two_image_window.update()

    self.bln_corr.set(True)
    self.bln_diff.set(False)


def apply_drift_fix(self):
    if self.bln_diff.get():
        update_original(self, self.dx, self.dy)
    else:
        update_original(self, self.shift_x, self.shift_y)


def cal_vw(self, dx, dy):
    N = self.image_ref1.shape[0]
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
    if self.drift_bool.get() is True:
        self.drift_check_func()


def close_drift_fix(self):
    if self.ref_1_selected:
        cv2.destroyWindow("Reference 1")
    if self.ref_2_selected:
        cv2.destroyWindow("Reference 2")
    self.two_image_window.destroy()


def get_corr(self):
    self.width_corr, self.height_corr, _ = self.image_ref1_or.shape
    image_dst = self.image_ref1_or[
        int(self.height_corr / 4) : int(self.height_corr * 3 / 4),
        int(self.width_corr / 4) : int(self.width_corr * 3 / 4),
    ]
    corr = cv2.matchTemplate(self.image_ref2_or, image_dst, cv2.TM_CCORR_NORMED)
    self.i_rec, self.k_rec = np.unravel_index(np.argmax(corr), corr.shape)


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
