#!python3.11

import tkinter as tk
import tkinter.ttk as ttk


class Window(ttk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, padding=2)
        master.title("Image analyzer")
        self.init_setting()
        self.create_frame_image_choise()
        self.create_frame_contrast()
        self.create_frame_cb()
        self.create_frame_drift()
        self.create_frame_rescale()
        self.create_frame_cut()
        self.create_frame_intensity()
        self.create_frame_edge()
        self.create_frame_sym()
        self.create_frame_checks()
        self.create_frame_size()
        self.create_frame_bias()
        self.create_frame_fft()
        self.create_frame_record()
        self.create_frame_buttons()
        self.master = master

    def create_frame_image_choise(self):
        self.frame_image_choice = ttk.Frame()
        self.create_widgets_choice()
        self.create_layout_choice()
        self.frame_image_choice.pack()

    def create_widgets_choice(self):
        self.fol_choice_text = ttk.Label(self.frame_image_choice, text="Folder")
        self.fol_name = ttk.Entry(self.frame_image_choice, width=20)
        self.button_folchoice = tk.Button(
            self.frame_image_choice,
            text="Folder choice",
            command=self.fol_choice_clicked,
            width=10,
        )
        #
        self.var_images = tk.StringVar()
        self.choice = ttk.Combobox(
            self.frame_image_choice,
            textvariable=self.var_images,
            values=[],
            width=57,
        )
        self.choice.bind("<<ComboboxSelected>>", self.choice_selected)
        self.choice_text = ttk.Label(self.frame_image_choice, text="Image")
        #
        self.var_imtypes = tk.StringVar()
        self.imtype_choice = ttk.Combobox(
            self.frame_image_choice,
            textvariable=self.var_imtypes,
            values=[],
            width=57,
        )
        self.imtype_text = ttk.Label(self.frame_image_choice, text="Image type")
        #
        self.button_imopen = tk.Button(
            self.frame_image_choice,
            text="Open",
            command=self.image_open_clicked,
            width=10,
        )
        self.images_update(self.dir_name)

    def create_frame_contrast(self):
        self.frame_contrast = ttk.Frame()
        self.create_widgets_contrast()
        self.create_layout_contrast()
        self.frame_contrast.pack()

    def create_widgets_contrast(self):
        self.upper_val = tk.DoubleVar()
        self.def_max = 255
        self.upper_val.set(self.def_max)
        self.upper_val.trace("w", self.upper_value_change)
        self.scale_upper = ttk.Scale(
            self.frame_contrast,
            variable=self.upper_val,
            orient=tk.HORIZONTAL,
            length=300,
            from_=-50,
            to=300,
        )
        #
        self.lower_val = tk.DoubleVar()
        self.def_min = 0
        self.lower_val.set(self.def_min)
        self.lower_val.trace("w", self.lower_value_change)
        self.scale_lower = ttk.Scale(
            self.frame_contrast,
            variable=self.lower_val,
            orient=tk.HORIZONTAL,
            length=300,
            from_=-50,
            to=300,
        )
        #
        self.upper_text = ttk.Label(self.frame_contrast, text="Upper")
        self.lower_text = ttk.Label(self.frame_contrast, text="lower")
        self.default_button = tk.Button(
            self.frame_contrast,
            text="Back to \rDefault",
            command=self.default_function,
            width=10,
        )
        #
        self.set_as_default_button = tk.Button(
            self.frame_contrast,
            text="Set as \rDefault",
            command=self.set_default_function,
            width=10,
        )
        #
        self.autoset_text = ttk.Label(self.frame_contrast, text="Auto set")
        self.upper_set_text = ttk.Label(self.frame_contrast, text="Upper (%)")
        self.lower_set_text = ttk.Label(self.frame_contrast, text="lower (%)")
        #
        self.upper_set_entry = ttk.Entry(self.frame_contrast, width=7)
        self.upper_set_entry.insert(tk.END, "100")
        self.lower_set_entry = ttk.Entry(self.frame_contrast, width=7)
        self.lower_set_entry.insert(tk.END, "0")
        #
        self.auto_set_button = tk.Button(
            self.frame_contrast,
            text="Auto Set",
            command=self.auto_set_function,
            width=10,
        )

    def create_frame_cb(self):
        self.frame_cb = ttk.Frame()
        self.create_widgets_cb()
        self.create_layout_cb()
        self.frame_cb.pack()

    def create_widgets_cb(self):
        self.var_cb_color = tk.StringVar()
        self.colormap_table = [
            "gray",
            "AUTUMN",
            "BONE ",
            "JET",
            "WINTER",
            "RAINBOW",
            "OCEAN",
            "SUMMER",
            "SPRING",
            "COOL",
            "HSV",
            "PINK",
            "HOT",
            "PALULA",
            "MAGNA",
            "INFERNO",
            "PLASMA",
            "VIRDIS",
            "CIVIDIS",
            "TWILIGHT",
            "TWILIGHT_SHIFTED",
        ]
        self.cb_color = ttk.Combobox(
            self.frame_cb,
            textvariable=self.var_cb_color,
            values=self.colormap_table,
        )

        self.cb_color.bind("<<ComboboxSelected>>", self.cb_color_selected)
        self.cb_color_text = ttk.Label(self.frame_cb, text="Color")
        self.cb_color.current(0)
        #
        self.smooth_entry = ttk.Entry(self.frame_cb, width=5)
        self.smooth_entry.insert(tk.END, "0")
        self.smooth_entry.bind("<Return>", self.smooth_change)
        self.cb_smooth_text = ttk.Label(self.frame_cb, text="Smoothing")
        self.cb_smooth_unit = ttk.Label(self.frame_cb, text="pixel")
        #
        self.median_entry = ttk.Entry(self.frame_cb, width=5)
        self.median_entry.insert(tk.END, "0")
        self.median_entry.bind("<Return>", self.median_change)
        self.cb_median_text = ttk.Label(self.frame_cb, text="Median")
        self.cb_median_unit = ttk.Label(self.frame_cb, text="pixel")

    def create_frame_drift(self):
        self.frame_drift = ttk.Frame()
        self.create_widgets_drift()
        self.create_layout_drift()
        self.frame_drift.pack()

    def create_widgets_drift(self):
        self.drift_dx_text = ttk.Label(self.frame_drift, text="v (nm/scan)")
        self.drift_dx = ttk.Entry(self.frame_drift, width=7)
        self.drift_dx.insert(tk.END, "0")
        self.drift_dx.bind("<Return>", self.drift_val_change)
        #
        self.drift_dy_text = ttk.Label(self.frame_drift, text="w (nm/scan)")
        self.drift_dy = ttk.Entry(self.frame_drift, width=7)
        self.drift_dy.insert(tk.END, "0")
        self.drift_dy.bind("<Return>", self.drift_val_change)

        self.var_drift = tk.StringVar()
        self.drift_methods = ["Two_images", "FFT"]
        self.drift_cb = ttk.Combobox(
            self.frame_drift,
            textvariable=self.var_drift,
            values=self.drift_methods,
        )
        self.drift_cb.current(0)

        self.drift_button = tk.Button(
            self.frame_drift, text="Calculate", command=self.drift_function, width=10
        )

    def create_frame_rescale(self):
        self.frame_rescale = ttk.Frame()
        self.create_widgets_rescale()
        self.create_layout_rescale()
        self.frame_rescale.pack()

    def create_widgets_rescale(self):
        self.rescale_text = ttk.Label(self.frame_rescale, text="Rescale All")
        self.rescale_label_x = ttk.Label(self.frame_rescale, text="X")
        self.rescale_label_y = ttk.Label(self.frame_rescale, text="Y")
        self.rescale_all = ttk.Entry(self.frame_rescale, width=7)
        self.rescale_all.insert(tk.END, "1")
        self.rescale_all.bind("<Return>", self.rescale)
        self.rescale_x = ttk.Entry(self.frame_rescale, width=7)
        self.rescale_x.insert(tk.END, "1")
        self.rescale_x.bind("<Return>", self.rescale)
        self.rescale_y = ttk.Entry(self.frame_rescale, width=7)
        self.rescale_y.insert(tk.END, "1")
        self.rescale_y.bind("<Return>", self.rescale)

    def create_frame_cut(self):
        self.frame_cut = ttk.Frame()
        self.create_widgets_cut()
        self.create_layout_cut()
        self.frame_cut.pack()

    def create_widgets_cut(self):
        self.cut_text = ttk.Label(self.frame_cut, text="Cut image (%)")
        self.cut_entry = ttk.Entry(self.frame_cut, width=7)
        self.cut_entry.insert(tk.END, "0")
        self.cut_entry.bind("<Return>", self.cut_image)

    def create_frame_intensity(self):
        self.frame_int = ttk.Frame()
        self.create_widgets_int()
        self.create_layout_int()
        self.frame_int.pack()

    def create_widgets_int(self):
        self.int_text = ttk.Label(self.frame_int, text="Intensity adjust")
        self.var_int = tk.StringVar()
        self.int_methods = ["Normal", "Log", "Sqrt"]
        self.int_cb = ttk.Combobox(
            self.frame_int,
            textvariable=self.var_int,
            values=self.int_methods,
        )
        self.int_cb.current(0)
        self.int_cb.bind("<<ComboboxSelected>>", self.int_cb_selected)
        self.int_gamma = ttk.Label(self.frame_int, text="Gamma")

        self.int_entry = ttk.Entry(self.frame_int, width=7)
        self.int_entry.insert(tk.END, "1")
        self.int_entry.bind("<Return>", self.int_gamma_change)

    def create_frame_edge(self):
        self.frame_edge = ttk.Frame()
        self.create_widgets_edge()
        self.create_layout_edge()
        self.frame_edge.pack()

    def create_widgets_edge(self):
        self.edge_text = ttk.Label(self.frame_edge, text="Edge detection")
        self.var_edge = tk.StringVar()
        self.edge_methods = [
            "None",
            "Sobel_x",
            "Sobel_y",
            "Laplacian",
            "Curvature",
        ]
        self.edge_cb = ttk.Combobox(
            self.frame_edge,
            textvariable=self.var_edge,
            values=self.edge_methods,
        )
        self.edge_cb.current(0)
        self.edge_cb.bind("<<ComboboxSelected>>", self.edge_change)

        self.edge_range = ttk.Label(self.frame_edge, text="constant")

        self.edge_entry = ttk.Entry(self.frame_edge, width=7)
        self.edge_entry.insert(tk.END, "3")
        self.edge_entry.bind("<Return>", self.edge_change)
        #
        self.mulor_bool = tk.BooleanVar()
        self.mulor_bool.set(False)
        self.mulor_check = tk.Checkbutton(
            self.frame_edge,
            variable=self.mulor_bool,
            text="x original",
            command=self.edge_change,
        )

    def create_frame_sym(self):
        self.frame_sym = ttk.Frame()
        self.create_widgets_symmetrize()
        self.create_layout_sym()
        self.create_widgets_line()
        self.create_layout_line()
        self.frame_sym.pack()

    def create_widgets_symmetrize(self):
        self.sym_text = ttk.Label(self.frame_sym, text="Symmetrize")
        self.var_method_symmetrize = tk.StringVar()
        self.method_symmetrize_table = [
            "None",
            "mirror_X",
            "mirror_XY",
            "six_fold",
            "six_fold+mirror",
        ]
        self.method_symmetrize_cb = ttk.Combobox(
            self.frame_sym,
            textvariable=self.var_method_symmetrize,
            values=self.method_symmetrize_table,
        )
        self.method_symmetrize_cb.bind(
            "<<ComboboxSelected>>", self.cb_symmetrize_selected
        )
        self.method_symmetrize_cb.current(0)
        #
        self.symm_angle_entry = tk.Entry(self.frame_sym, text="Rotation angle", width=7)
        self.symm_angle_entry.delete(0, tk.END)
        self.symm_angle_entry.insert(tk.END, 0)
        self.symm_angle_entry.bind("<Return>", self.symm_angle_return)
        self.symm_angle_entry.bind("<Up>", self.symm_angle_up)
        self.symm_angle_entry.bind("<Down>", self.symm_angle_down)
        #
        self.symm_angle_text = tk.Label(self.frame_sym, text="Rotation")
        #

    def create_widgets_line(self):
        self.line_text = ttk.Label(self.frame_sym, text="Draw symmetric line")
        self.var_method_line = tk.StringVar()
        self.method_line_table = [
            "None",
            "X",
            "XY",
            "Six_fold",
        ]
        self.method_line_cb = ttk.Combobox(
            self.frame_sym,
            textvariable=self.var_method_line,
            values=self.method_line_table,
        )
        self.method_line_cb.bind("<<ComboboxSelected>>", self.cb_line_selected)
        self.method_line_cb.current(0)

    def create_frame_checks(self):
        self.frame_square = ttk.Frame()
        self.create_widgets_checks()
        self.create_layout_checks()
        self.frame_square.pack()

    def create_widgets_checks(self):
        self.square_bool = tk.BooleanVar()
        self.square_bool.set(False)
        self.square_check = tk.Checkbutton(
            self.frame_square,
            variable=self.square_bool,
            text="Squareize",
            command=self.square_image,
        )
        #
        self.oddize_bool = tk.BooleanVar()
        self.oddize_bool.set(False)
        self.oddize_check = tk.Checkbutton(
            self.frame_square,
            variable=self.oddize_bool,
            text="Odd pixels",
            command=self.oddize_image,
        )
        #
        self.average_bool = tk.BooleanVar()
        self.average_bool.set(False)
        self.average_check = tk.Checkbutton(
            self.frame_square,
            variable=self.average_bool,
            text="Average subtraction",
            command=self.average_image,
        )
        #
        self.mirror_bool = tk.BooleanVar()
        self.mirror_bool.set(False)
        self.mirror_check = tk.Checkbutton(
            self.frame_square,
            variable=self.mirror_bool,
            text="Mirror",
            command=self.mirror_image,
        )
        #
        self.ignore_neg_bool = tk.BooleanVar()
        self.ignore_neg_bool.set(False)
        self.ignore_neg_check = tk.Checkbutton(
            self.frame_square,
            variable=self.ignore_neg_bool,
            text="Ignore neg.",
            command=self.ignore_neg_image,
        )

    def create_frame_size(self):
        self.frame_size = ttk.Frame()
        self.create_widgets_size()
        self.create_layout_size()
        self.frame_size.pack()

    def create_widgets_size(self):
        self.original_size_text = ttk.Label(self.frame_size, text="Original size (nm)")
        self.current_size_text = ttk.Label(self.frame_size, text="Current size (nm)")
        self.original_x_text = ttk.Label(self.frame_size, text="x")
        self.current_x_text = ttk.Label(self.frame_size, text="x")
        self.original_y_text = ttk.Label(self.frame_size, text="y")
        self.current_y_text = ttk.Label(self.frame_size, text="y")
        #
        self.original_x = ttk.Entry(self.frame_size, width=7)
        self.original_x.insert(tk.END, "30")
        self.original_x.bind("<Return>", self.original_size_changed)
        #
        self.orpix_x = ttk.Label(self.frame_size, text="(- px)")
        #
        self.original_y = ttk.Entry(self.frame_size, width=7)
        self.original_y.insert(tk.END, "30")
        self.original_y.bind("<Return>", self.original_size_changed)
        #
        self.orpix_y = ttk.Label(self.frame_size, text="(- px)")
        #
        self.current_x = ttk.Label(self.frame_size, text="30")
        self.current_y = ttk.Label(self.frame_size, text="30")
        self.current_pxx = ttk.Label(self.frame_size, text="(- px)")
        self.current_pxy = ttk.Label(self.frame_size, text="(- px)")

    def create_frame_bias(self):
        self.frame_bias = ttk.Frame()
        self.create_widgets_bias()
        self.create_layout_bias()
        self.frame_bias.pack()

    def create_widgets_bias(self):
        self.bias_text = ttk.Label(self.frame_bias, text="STM bias (mV)")
        self.bias = ttk.Entry(self.frame_bias, width=7)
        self.bias.insert(tk.END, "0")

    def create_frame_fft(self):
        self.frame_fft = ttk.Frame()
        self.create_widgets_fft()
        self.create_layout_fft()
        self.frame_fft.pack()

    def create_widgets_fft(self):
        self.fft_button = tk.Button(
            self.frame_fft, text="Real → FFT", command=self.fft_function, width=30
        )
        #
        self.var_method_fft = tk.StringVar()
        self.method_fft_table = ["Linear", "Sqrt", "Log"]
        self.method_fft_cb = ttk.Combobox(
            self.frame_fft,
            textvariable=self.var_method_fft,
            values=self.method_fft_table,
        )
        self.method_fft_cb.bind("<<ComboboxSelected>>", self.cb_method_selected)
        self.method_fft_cb.current(1)
        self.method_text = ttk.Label(self.frame_fft, text="Intensity")
        #
        self.var_window = tk.StringVar()
        self.window_table = ["None", "Hann", "Hamming", "Blackman"]
        self.window_cb = ttk.Combobox(
            self.frame_fft, textvariable=self.var_window, values=self.window_table
        )
        self.window_cb.bind("<<ComboboxSelected>>", self.cb_window_selected)
        self.window_cb.current(0)
        self.window_text = ttk.Label(self.frame_fft, text="Window")
        #

    def create_frame_record(self):
        self.frame_record = ttk.Frame()
        self.create_widgets_record()
        self.create_layout_record()
        self.frame_record.pack()

    def create_widgets_record(self):
        self.rec_fol_name = ttk.Entry(self.frame_record, width=20)
        self.button_recfolchoice = tk.Button(
            self.frame_record,
            text="Rec. folder choice",
            command=self.rec_fol_choice_clicked,
            width=10,
        )

        self.fol_choice_text_record = ttk.Label(self.frame_record, text="Record folder")
        self.record_text = ttk.Label(self.frame_record, text="Record")
        self.record = ttk.Entry(self.frame_record, width=40)
        self.record.insert(tk.END, "---")
        self.record.bind("<Return>", self.record_name_changed)
        self.record_plus = ttk.Entry(self.frame_record, width=20)
        self.record_plus.insert(tk.END, "---")
        self.record_plus.bind("<Return>", self.record_name_changed)
        #
        self.dirdiv_bool = tk.BooleanVar()
        self.dirdiv_bool.set(True)
        self.dirdiv_check = tk.Checkbutton(
            self.frame_record,
            variable=self.dirdiv_bool,
            text="Divide folder",
        )

    def create_frame_buttons(self):
        self.frame_buttons = ttk.Frame()
        self.create_widgets_buttons()
        self.create_layout_buttons()
        self.frame_buttons.pack()

    def create_widgets_buttons(self):
        self.record_button = tk.Button(
            self.frame_buttons,
            text="Record",
            command=self.record_function,
            width=18,
            height=2,
        )
        self.close_button = tk.Button(
            self.frame_buttons,
            text="Close",
            command=self.close_function,
            width=18,
            height=2,
        )
        self.process_button = tk.Button(
            self.frame_buttons,
            text="Process",
            command=self.process_window,
            width=18,
            height=2,
        )
