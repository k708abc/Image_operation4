import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import glob
import os
from tkinter import filedialog
import pathlib


class P_window:
    def manage_process(self):
        self.manage_bool = True
        # self.FFT_params_form = True
        self.manage_process_window = tk.Toplevel()
        self.manage_process_window.geometry("720x440")
        self.manage_process_window.title("Applied processes")
        self.create_frame_header()
        self.create_frame_datalist()
        self.create_widgets_buttons_manaage()
        self.create_widgets_comment()
        self.create_layouts_manage()
        self.manage_process_window.protocol("WM_DELETE_WINDOW", self.callback)

    def callback(self):
        self.manage_process_window.destroy()
        self.manage_bool = False

    def manage_init_setting(self):
        self.num_process = len(self.processes) + len(self.processes_FFT)
        self.num_process_real = len(self.processes) - 1

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _no_mousewheel(self, event):
        pass

    def create_frame_header(self):
        self.canvas_index = tk.Canvas(
            self.manage_process_window, width=720, height=20, bg="white"
        )
        self.frame_list_index = tk.Frame(self.canvas_index, bg="white")
        self.form_canvas_header()
        self.create_widgets_header()
        self.create_layout_header()

    def form_canvas_header(self):
        self.canvas_index.grid(row=0, column=0, columnspan=5)
        self.canvas_index.create_window(
            (0, 0),
            window=self.frame_list_index,
            anchor=tk.NW,
            width=self.canvas_index.cget("width"),
        )

    def create_widgets_header(self):
        self.header_func = tk.Label(
            self.frame_list_index, width=30, text="Function", background="white"
        )
        self.header_vals = tk.Label(
            self.frame_list_index, width=30, text="Values", background="white"
        )

    def create_layout_header(self):
        self.header_func.grid(row=0, column=1, padx=1, pady=0, ipadx=0, ipady=0)
        self.header_vals.grid(row=0, column=2, padx=1, pady=0, ipadx=0, ipady=0)

    def create_frame_datalist(self):
        self.FFT_bool = False
        self.manage_init_setting()
        self.canvas = tk.Canvas(self.manage_process_window, width=720, bg="white")
        self.frame_list = tk.Frame(self.canvas, bg="white")
        self.form_canvas_datalist()
        self.create_widgets_datalist()

    def form_canvas_datalist(self):
        self.canvas.grid(
            row=1, rowspan=max(1, self.num_process), column=0, columnspan=5
        )
        #
        vbar = tk.ttk.Scrollbar(self.manage_process_window, orient=tk.VERTICAL)
        vbar.grid(row=1, rowspan=1000, column=5, sticky="ns")
        #
        vbar.config(command=self.canvas.yview)
        #
        self.canvas.config(yscrollcommand=vbar.set)
        #
        sc_hgt = int(150 / 6 * (self.num_process))
        self.canvas.config(scrollregion=(0, 0, 500, sc_hgt))
        #
        if self.num_process >= 8:
            self.frame_list.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.frame_list.bind_all("<MouseWheel>", self._no_mousewheel)
        self.canvas.create_window(
            (0, 0),
            window=self.frame_list,
            anchor=tk.NW,
            width=self.canvas.cget("width"),
        )

    def button_function(self, text, bool, num):
        def inner_function():
            if bool.get():
                bool.set(False)
                text.set("OFF")
                self.processes[num][-1] = False

            else:
                bool.set(True)
                text.set("ON")
                self.processes[num][-1] = True
            self.switch_bool = True

        return inner_function

    def button_function_FFT(self, text, bool, num):
        def inner_function():
            if bool.get():
                bool.set(False)
                text.set("OFF")
                self.processes_FFT[num][-1] = False
            else:
                bool.set(True)
                text.set("ON")
                self.processes_FFT[num][-1] = True
            self.switch_bool = True

        return inner_function

    def create_widgets_datalist(self):
        self.manage_init_setting()
        self.check_list = []
        self.check_list_FFT = []
        self.process_manage = []
        self.process_manage_FFT = []
        color = "#FFCDE2"
        real_text = tk.Label(
            self.frame_list, width=10, text="Real image", background=color
        )
        real_text.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        #
        for i in range(len(self.processes)):
            # color set
            if i % 2 == 0:
                color = "#cdfff7"  # blue
            else:
                color = "white"
            # checkbox
            check_bln = tk.BooleanVar()
            check_bln.set(False)
            c1 = tk.Checkbutton(
                self.frame_list,
                variable=check_bln,
                width=3,
                text="",
                background="white",
            )
            c1.grid(row=i + 3, column=0, padx=0, pady=0, ipadx=0, ipady=0)
            self.check_list.append(check_bln)
            # process name
            process_name = tk.Label(
                self.frame_list, width=18, text=self.processes[i][0], background=color
            )
            process_name.grid(row=i + 3, column=1, padx=1, pady=0, ipadx=0, ipady=0)

            # on_off switch
            sw_bool = tk.BooleanVar()
            sw_text = tk.StringVar()
            if type(self.processes[i][-1]) != bool:
                sw_bool.set(True)
                sw_text.set("ON")
            else:
                if self.processes[i][-1]:
                    sw_bool.set(True)
                    sw_text.set("ON")
                else:
                    sw_bool.set(False)
                    sw_text.set("OFF")
            func = self.button_function(sw_text, sw_bool, i)
            sw_button = tk.Button(
                self.frame_list,
                textvariable=sw_text,
                command=func,
                width=3,
            )
            sw_button.grid(row=i + 3, column=10, padx=1, pady=0, ipadx=0, ipady=0)
            #
            process_temp = self.get_process_list(self.processes[i], color, i + 1)
            process_temp.append(sw_bool)
            self.process_manage.append(process_temp)
        #
        color = "#FFCDE2"
        FFT_text = tk.Label(
            self.frame_list, width=10, text="FFT image", background=color
        )
        FFT_text.grid(
            row=self.num_process_real + 3, column=0, padx=0, pady=0, ipadx=0, ipady=0
        )
        #
        if self.FFT_params != []:
            self.FFT_params_form = False
            FFT_method_text = tk.Label(
                self.frame_list, width=10, text="Method", background=color
            )
            self.FFT_method_var = tk.StringVar()
            FFT_method_cb = ttk.Combobox(
                self.frame_list,
                textvariable=self.FFT_method_var,
                width=12,
                values=self.method_fft_table,
            )
            FFT_method_cb.set(self.FFT_params[1])
            #
            FFT_window_text = tk.Label(
                self.frame_list, width=10, text="Window", background=color
            )
            self.FFT_window_var = tk.StringVar()
            FFT_window_cb = ttk.Combobox(
                self.frame_list,
                textvariable=self.FFT_window_var,
                width=12,
                values=self.window_table,
            )
            FFT_window_cb.set(self.FFT_params[2])

            #

            FFT_method_text.grid(
                row=self.num_process_real + 3,
                column=1,
                padx=0,
                pady=0,
                ipadx=0,
                ipady=0,
            )
            FFT_method_cb.grid(
                row=self.num_process_real + 3,
                column=2,
                padx=0,
                pady=0,
                ipadx=0,
                ipady=0,
            )
            FFT_window_text.grid(
                row=self.num_process_real + 3,
                column=3,
                padx=0,
                pady=0,
                ipadx=0,
                ipady=0,
            )
            FFT_window_cb.grid(
                row=self.num_process_real + 3,
                column=4,
                padx=0,
                pady=0,
                ipadx=0,
                ipady=0,
            )
        for i in range(len(self.processes_FFT)):
            # color set
            if i % 2 == 0:
                color = "#cdfff7"  # blue
            else:
                color = "white"
            # checkbox
            check_bln = tk.BooleanVar()
            check_bln.set(False)
            c1 = tk.Checkbutton(
                self.frame_list,
                variable=check_bln,
                width=3,
                text="",
                background="white",
            )
            c1.grid(
                row=i + self.num_process_real + 4,
                column=0,
                padx=0,
                pady=0,
                ipadx=0,
                ipady=0,
            )
            self.check_list_FFT.append(check_bln)
            # image name
            process_name = tk.Label(
                self.frame_list,
                width=18,
                text=self.processes_FFT[i][0],
                background=color,
            )
            process_name.grid(
                row=i + self.num_process_real + 4,
                column=1,
                padx=1,
                pady=0,
                ipadx=0,
                ipady=0,
            )
            #
            sw_bool_FFT = tk.BooleanVar()
            sw_text_FFT = tk.StringVar()
            if self.processes_FFT[i][-1]:
                sw_bool_FFT.set(True)
                sw_text_FFT.set("ON")
            else:
                sw_bool_FFT.set(False)
                sw_text_FFT.set("OFF")
            func = self.button_function_FFT(sw_text_FFT, sw_bool_FFT, i)
            sw_button_FFT = tk.Button(
                self.frame_list,
                textvariable=sw_text_FFT,
                command=func,
                width=3,
            )
            sw_button_FFT.grid(
                row=i + self.num_process_real + 4,
                column=10,
                padx=1,
                pady=0,
                ipadx=0,
                ipady=0,
            )
            process_temp = self.get_process_list(
                self.processes_FFT[i], color, i + self.num_process_real + 2
            )
            process_temp.append(sw_bool_FFT)
            self.process_manage_FFT.append(process_temp)

    def get_process_list(self, process, color, num):
        #
        if process[0] == "smoothing":
            smoothvar = StringVar()
            smooth_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=smoothvar
            )
            smooth_entry.insert(tk.END, process[1])
            smooth_text = tk.Label(
                self.frame_list, width=8, text="value", background=color
            )
            smooth_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            smooth_entry.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            return ["smoothing", smoothvar]

        elif process[0] == "median":
            medianvar = StringVar()
            median_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=medianvar
            )
            median_entry.insert(tk.END, process[1])
            median_text = tk.Label(
                self.frame_list, width=8, text="value", background=color
            )
            median_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            median_entry.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            return ["median", medianvar]

        elif process[0] == "set_contrast":
            upper_var = StringVar()
            upper_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=upper_var
            )
            upper_entry.insert(tk.END, process[1])
            upper_text = tk.Label(
                self.frame_list, width=8, text="Upper", background=color
            )
            #
            lower_var = StringVar()
            lower_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=lower_var
            )
            lower_entry.insert(tk.END, process[2])
            lower_text = tk.Label(
                self.frame_list, width=8, text="Lower", background=color
            )
            #
            upper_entry.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            upper_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            lower_entry.grid(row=num + 2, column=5, padx=1, pady=0, ipadx=0, ipady=0)
            lower_text.grid(row=num + 2, column=4, padx=1, pady=0, ipadx=0, ipady=0)

            return ["set_contrast", upper_var, lower_var]

        elif process[0] == "drift":
            driftx_var = StringVar()
            driftx_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=driftx_var
            )
            driftx_entry.insert(tk.END, process[1])
            #
            drifty_var = StringVar()
            drifty_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=drifty_var
            )
            drifty_entry.insert(tk.END, process[2])
            #
            driftx_text = tk.Label(self.frame_list, width=8, text="v", background=color)
            drifty_text = tk.Label(self.frame_list, width=8, text="w", background=color)

            driftx_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            driftx_entry.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            drifty_text.grid(row=num + 2, column=4, padx=1, pady=0, ipadx=0, ipady=0)
            drifty_entry.grid(row=num + 2, column=5, padx=1, pady=0, ipadx=0, ipady=0)
            return ["drift", driftx_var, drifty_var]

        elif process[0] == "rescale":
            rescale_all_var = StringVar()
            rescale_all_entry = tk.Entry(
                self.frame_list,
                width=8,
                background=color,
                textvariable=rescale_all_var,
            )
            rescale_all_entry.insert(tk.END, process[1])
            #
            rescale_x_var = StringVar()
            rescale_x_entry = tk.Entry(
                self.frame_list,
                width=8,
                background=color,
                textvariable=rescale_x_var,
            )
            rescale_x_entry.insert(tk.END, process[2])
            #
            rescale_y_var = StringVar()
            rescale_y_entry = tk.Entry(
                self.frame_list,
                width=8,
                background=color,
                textvariable=rescale_y_var,
            )
            rescale_y_entry.insert(tk.END, process[3])
            #
            rescale_all_text = tk.Label(
                self.frame_list, width=8, text="All", background=color
            )
            rescale_x_text = tk.Label(
                self.frame_list, width=8, text="X", background=color
            )
            rescale_y_text = tk.Label(
                self.frame_list, width=8, text="Y", background=color
            )
            #
            rescale_all_text.grid(
                row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0
            )
            rescale_all_entry.grid(
                row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0
            )
            rescale_x_text.grid(row=num + 2, column=4, padx=1, pady=0, ipadx=0, ipady=0)
            rescale_x_entry.grid(
                row=num + 2, column=5, padx=1, pady=0, ipadx=0, ipady=0
            )
            rescale_y_text.grid(row=num + 2, column=6, padx=1, pady=0, ipadx=0, ipady=0)
            rescale_y_entry.grid(
                row=num + 2, column=7, padx=1, pady=0, ipadx=0, ipady=0
            )
            return [
                "rescale",
                rescale_all_var,
                rescale_x_var,
                rescale_y_var,
            ]

        elif process[0] == "cut":
            cutvar = StringVar()
            cut_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=cutvar
            )
            cut_entry.insert(tk.END, process[1])
            cut_text = tk.Label(
                self.frame_list, width=8, text="value", background=color
            )
            cut_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            cut_entry.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            return ["cut", cutvar]

        elif process[0] == "int_change":
            int_var = tk.StringVar()
            int_cb = ttk.Combobox(
                self.frame_list,
                textvariable=int_var,
                width=12,
                values=self.int_methods,
            )
            int_cb.current(self.int_methods.index(process[1]))
            int_text = tk.Label(
                self.frame_list, width=8, text="Method", background=color
            )
            int_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            int_cb.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            return ["int_change", int_var]

        elif process[0] == "gamma":
            gammavar = StringVar()
            gamma_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=gammavar
            )
            gamma_entry.insert(tk.END, process[1])
            gamma_text = tk.Label(
                self.frame_list, width=8, text="value", background=color
            )
            gamma_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            gamma_entry.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            return ["gamma", gammavar]

        elif process[0] == "edge_det":
            edge_var = tk.StringVar()
            edge_cb = ttk.Combobox(
                self.frame_list,
                textvariable=edge_var,
                width=12,
                values=self.edge_methods,
            )
            edge_cb.set(process[1])
            edge_text = tk.Label(
                self.frame_list, width=8, text="Method", background=color
            )
            #
            edge_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            edge_cb.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            #
            edge_range_var = StringVar()
            edge_range_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=edge_range_var
            )
            edge_range_entry.insert(tk.END, process[2])
            edge_range_text = tk.Label(
                self.frame_list, width=8, text="Range", background=color
            )
            #
            edge_xor_var = tk.BooleanVar()
            edge_xor_var.set(process[3])
            xor_check = tk.Checkbutton(
                self.frame_list,
                variable=edge_xor_var,
                text="x original",
            )

            #
            edge_range_text.grid(
                row=num + 2, column=4, padx=1, pady=0, ipadx=0, ipady=0
            )
            edge_range_entry.grid(
                row=num + 2, column=5, padx=1, pady=0, ipadx=0, ipady=0
            )
            xor_check.grid(row=num + 2, column=6, padx=1, pady=0, ipadx=0, ipady=0)
            return ["edge_det", edge_var, edge_range_var, edge_xor_var]

        elif process[0] == "square":
            return ["square"]

        elif process[0] == "oddize":
            return ["oddize"]

        elif process[0] == "ave_sub":
            return ["ave_sub"]

        elif process[0] == "mirror":
            return ["mirror"]

        elif process[0] == "ignore_neg":
            return ["ignore_neg"]

        elif process[0] == "FFT":
            pass

        elif process[0] == "Symm":
            symm_var = tk.StringVar()
            sym_cb = ttk.Combobox(
                self.frame_list,
                textvariable=symm_var,
                width=12,
                values=self.method_symmetrize_table,
            )
            sym_cb.current(self.method_symmetrize_table.index(process[1]))
            symm_text = tk.Label(
                self.frame_list, width=8, text="Method", background=color
            )
            symm_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            sym_cb.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)

            return ["Symm", symm_var]

        elif process[0] == "Rot":
            rotvar = StringVar()
            rot_entry = tk.Entry(
                self.frame_list, width=8, background=color, textvariable=rotvar
            )
            rot_entry.insert(tk.END, process[1])
            rot_text = tk.Label(
                self.frame_list, width=8, text="value", background=color
            )
            rot_text.grid(row=num + 2, column=2, padx=1, pady=0, ipadx=0, ipady=0)
            rot_entry.grid(row=num + 2, column=3, padx=1, pady=0, ipadx=0, ipady=0)
            return ["Rot", rotvar]

    def create_widgets_buttons_manaage(self):
        self.reflesh_btn = tk.Button(
            self.manage_process_window,
            text="Run process",
            command=self.reload_process,
            height=2,
            width=30,
        )
        self.del_checked_btn = tk.Button(
            self.manage_process_window,
            text="Delete checked",
            command=self.delete_checked,
            height=2,
            width=30,
        )
        self.del_all_btn = tk.Button(
            self.manage_process_window,
            text="Delete all",
            command=self.delete_all,
            height=2,
            width=30,
        )
        self.read_process_btn = tk.Button(
            self.manage_process_window,
            text="Read process",
            command=self.read_process_clicked,
            height=1,
            width=30,
        )
        self.read_process_btn["state"] = tk.DISABLED

        self.run_all_btn = tk.Button(
            self.manage_process_window,
            text="Run all process",
            command=self.run_all,
            height=1,
            width=15,
        )
        self.read_process_btn["state"] = tk.DISABLED
        #
        self.allim_bool = tk.BooleanVar()
        self.allim_bool.set(False)
        self.allim_check = tk.Checkbutton(
            self.manage_process_window,
            variable=self.allim_bool,
            text="For all images",
        )
        """
        self.perform_process_btn = tk.Button(
            self.manage_process_window,
            text="Run process",
            command=self.perform_process,
            height=3,
            width=20,
        )
        """
        #
        self.dir_name_process = self.dir_name
        self.process_list = self.read_process_list(self.dir_name_process)
        #
        self.pro_fol_name = ttk.Entry(self.manage_process_window, width=55)
        self.button_profolchoice = tk.Button(
            self.manage_process_window,
            text="Process folder choice",
            command=self.pro_fol_choice_clicked,
            width=30,
        )

        self.fol_choice_text_process = ttk.Label(
            self.manage_process_window, text="Folder"
        )

        #
        self.var_images_process = tk.StringVar()
        self.choice_process = ttk.Combobox(
            self.manage_process_window,
            textvariable=self.var_images_process,
            values=self.process_list,
            width=52,
        )
        self.choice_text_process = ttk.Label(
            self.manage_process_window, text="Process file"
        )
        if len(self.process_list) > 0:
            self.read_process_btn["state"] = tk.NORMAL
            self.choice_process.current(0)

    def create_widgets_comment(self):
        self.comment_label = ttk.Label(self.manage_process_window, text="Comment")
        self.comment = ttk.Label(self.manage_process_window, text="----")

    def create_layouts_manage(self):
        self.reflesh_btn.place(x=470, y=300)
        self.del_checked_btn.place(x=20, y=300)
        self.del_all_btn.place(x=245, y=300)
        #
        self.read_process_btn.place(x=470, y=375)
        self.run_all_btn.place(x=470, y=405)
        self.allim_check.place(x=600, y=405)
        # self.perform_process_btn.place(x=500, y=300)
        # self.fol_choice_process.place(x=120, y=365)

        self.pro_fol_name.place(x=120, y=348)
        self.button_profolchoice.place(x=470, y=345)
        self.fol_choice_text_process.place(x=20, y=348)
        self.choice_process.place(x=120, y=378)
        self.choice_text_process.place(x=20, y=378)
        #
        self.comment_label.place(x=20, y=405)
        self.comment.place(x=120, y=405)

    def delete_all(self):
        self.processes = []
        self.processes_FFT = []
        self.create_frame_datalist()
        self.val_reset(self.prev_process)
        self.prev_process = "reset"
        self.run_process()
        self.show_image()

    def read_process_clicked(self):
        data_path = self.dir_name_process + "\\" + self.choice_process.get()
        _ = self.read_process(data_path)

    def read_process(self, data_path, update=True):
        self.processes = []
        self.processes_FFT = []
        FFT_bool = True
        if os.path.isfile(data_path):
            with open(data_path) as f:
                lines = f.readlines()
                readcheck = False
                readchack_FFT = False
                for i, line in enumerate(lines):
                    values = line.split()
                    if i == 0:
                        if "Process_record" not in values:
                            return False
                    process = []
                    for i in values:
                        if i == "True":
                            process.append(True)
                        elif i == "False":
                            process.append(False)
                        else:
                            process.append(i)

                    if "FFT_params:" in values:
                        FFT_bool = False
                        self.FFT_params = [values[i] for i in (1, 2, 3)]
                        if values[4] == "ON":
                            self.im_type_real = False

                        elif values[4] == "OFF":
                            self.im_type_real = True
                            self.fft_button["text"] = "Real\r →FFT"
                            self.setting_real()

                    elif readcheck:
                        if process != []:
                            self.processes.append(process)
                    elif readchack_FFT:
                        if process != []:
                            self.processes_FFT.append(process)
                    if "Real_params:" in values:
                        readcheck = True
                    if "FFT_params:" in values:
                        readcheck = False
                        readchack_FFT = True
                    if "Name_tag:" in values:
                        self.record_plus.delete(0, tk.END)
                        self.record_plus.insert(tk.END, values[1])
                        self.name_change = True
            if FFT_bool:
                self.im_type_real = True
                self.fft_button["text"] = "Real\r →FFT"
                self.setting_real()
            if update:
                self.create_frame_datalist()
            # self.rewrite_process()
            if self.im_select:
                self.run_process()
                self.show_image()
            return True
        else:
            return False

    def delete_checked(self):
        for i, chk in enumerate(self.check_list):
            if chk.get():
                self.processes[i] = None
        self.processes = [pro for pro in self.processes if pro is not None]
        for i, chk in enumerate(self.check_list_FFT):
            if chk.get():
                self.processes_FFT[i] = None
        self.processes_FFT = [pro for pro in self.processes_FFT if pro is not None]
        self.create_frame_datalist()
        self.rewrite_process()
        if self.im_select:
            self.val_reset(self.prev_process)
            self.run_process()
            self.show_image()
        self.prev_process = "reset"

    def reload_process(self):
        self.reflesh_btn["state"] = "disable"
        self.rewrite_process()
        self.create_frame_datalist()
        if self.im_select:
            self.new_process = "Reload"
            self.process_function()
            self.val_reset(self.prev_process)
            self.run_process()
            self.show_image()
            self.prev_process = "Reload"
        self.reflesh_btn["state"] = "normal"

    def rewrite_process(self):
        for i, pro in enumerate(self.process_manage):
            self.processes[i] = self.replace_process(pro)

        if self.FFT_params != []:
            self.FFT_params[1] = self.FFT_method_var.get()
            self.FFT_params[2] = self.FFT_window_var.get()
        for i, pro in enumerate(self.process_manage_FFT):
            self.processes_FFT[i] = self.replace_process(pro)

    def run_all_exe(self):
        self.prev_rec = False
        for process in self.process_list:
            data_path = self.dir_name_process + "\\" + process
            judge = self.read_process(data_path, update=False)
            if judge:
                self.record_function()

    def run_all(self):
        self.comment["text"] = "Running... "
        if self.allim_bool.get():
            choise_num = self.imtype_choice.current()
            for i in range(len(self.image_list)):
                self.choice.current(i)
                self.imtype_choice.current(choise_num)
                self.image_open_clicked()
                self.run_all_exe()
        else:
            if self.im_select:
                self.run_all_exe()
        self.comment["text"] = "Run all finished"

    def replace_process(self, process):
        if process[0] == "smoothing":
            return [process[0], process[1].get(), process[-1].get()]
        elif process[0] == "median":
            return [process[0], process[1].get(), process[-1].get()]
        elif process[0] == "set_contrast":
            return [process[0], process[1].get(), process[2].get(), process[-1].get()]
        elif process[0] == "drift":
            return [process[0], process[1].get(), process[2].get(), process[-1].get()]
        elif process[0] == "rescale":
            return [
                process[0],
                process[1].get(),
                process[2].get(),
                process[3].get(),
                process[-1].get(),
            ]
        elif process[0] == "cut":
            return [process[0], process[1].get(), process[-1].get()]
        elif process[0] == "int_change":
            return [process[0], process[1].get(), process[-1].get()]
        elif process[0] == "gamma":
            return [process[0], process[1].get(), process[-1].get()]
        elif process[0] == "edge_det":
            return [
                process[0],
                process[1].get(),
                process[2].get(),
                process[3].get(),
                process[-1].get(),
            ]
        elif process[0] == "square":
            return [process[0], process[-1].get()]
        elif process[0] == "oddize":
            return [process[0], process[-1].get()]
        elif process[0] == "ave_sub":
            return [process[0], process[-1].get()]
        elif process[0] == "mirror":
            return [process[0], process[-1].get()]
        elif process[0] == "ignore_neg":
            return [process[0], process[-1].get()]
        elif process[0] == "Symm":
            return [process[0], process[1].get(), process[-1].get()]
        elif process[0] == "Rot":
            return [process[0], process[1].get(), process[-1].get()]

    def pro_fol_choice_clicked(self):
        abs_pass = pathlib.Path(
            filedialog.askdirectory(initialdir=self.dir_name_process)
        )
        if abs_pass == pathlib.Path("."):
            return
        self.dir_name_process = os.path.relpath(abs_pass, self.init_dir)
        self.pro_fol_name.delete(0, tk.END)
        self.pro_fol_name.insert(tk.END, self.dir_name_process)
        self.reflesh_process_list()
        self.manage_process_window.update()

    def read_process_list(self, dir_name):
        process_list = glob.glob(dir_name + "\*")
        process_list = [os.path.basename(pathname) for pathname in process_list]
        process_list2 = [file for file in process_list if "process.txt" in file]
        return process_list2

    def reflesh_process_list(self):
        self.process_list = self.read_process_list(self.dir_name_process)
        self.choice_process["values"] = self.process_list
        if len(self.process_list) > 0:
            self.choice_process.current(0)
            self.read_process_btn["state"] = tk.NORMAL

    def update_process_w(self):
        self.create_frame_datalist()
