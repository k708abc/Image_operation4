import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import glob
import os
from tkinter import filedialog
import pathlib
from Modules.process_classes import ImOpen
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
                self.processes[num].switch = False
            else:
                bool.set(True)
                text.set("ON")
                self.processes[num].switch = True

        return inner_function

    def button_function_FFT(self, text, bool, num):
        def inner_function():
            if bool.get():
                bool.set(False)
                text.set("OFF")
                self.processes_FFT[num].switch = False
            else:
                bool.set(True)
                text.set("ON")
                self.processes_FFT[num].switch = True

        return inner_function

    def list_form(self, process, start_val, type):
        check_list = []
        var_list = []
        switch_list = []
        for i in range(1, len(process)):
            var_list.append([])
            if (i + 1) % 2 == 0:
                color = "#cdfff7"  # blue
            else:
                color = "white"
            check_bln = tk.BooleanVar()
            check_bln.set(False)
            chk_btn = tk.Checkbutton(
                self.frame_list,
                variable=check_bln,
                width=3,
                text="",
                background="white",
            )
            chk_btn.grid(
                row=start_val + i + 1, column=0, padx=0, pady=0, ipadx=0, ipady=0
            )
            check_list.append(check_bln)
            # process name
            process_name = tk.Label(
                self.frame_list, width=18, text=process[i].name, background=color
            )
            process_name.grid(
                row=start_val + i + 1, column=1, padx=1, pady=0, ipadx=0, ipady=0
            )
            #
            clm = 2
            for pro_name, pro_type in zip(process[i].params, process[i].params_type):
                text = tk.Label(
                    self.frame_list, width=6, text=pro_name, background=color
                )
                text.grid(
                    row=start_val + i + 1, column=clm, padx=1, pady=0, ipadx=0, ipady=0
                )
                component = None
                if pro_type == "entry":
                    var = StringVar()
                    component = tk.Entry(
                        self.frame_list, width=5, background=color, textvariable=var
                    )
                    component.insert(tk.END, process[i].getval(pro_name))

                elif pro_type == "combo_box":
                    txt_var = process[i].get_list(pro_name)

                    var = tk.StringVar()
                    component = ttk.Combobox(
                        self.frame_list,
                        textvariable=var,
                        width=12,
                        values=txt_var,
                    )
                    component.set(process[i].getval(pro_name))
                elif pro_type == "check_box":
                    var = tk.BooleanVar()
                    var.set(process[i].getval(pro_name))
                    component = tk.Checkbutton(
                        self.frame_list,
                        variable=var,
                        text="",
                    )
                if component is not None:
                    component.grid(
                        row=start_val + i + 1,
                        column=clm + 1,
                        padx=1,
                        pady=0,
                        ipadx=0,
                        ipady=0,
                    )
                    var_list[-1].append(var)
                clm += 2

            # on_off switch
            sw_bool = tk.BooleanVar()
            sw_text = tk.StringVar()
            if process[i].switch:
                sw_bool.set(True)
                sw_text.set("ON")
            else:
                sw_bool.set(False)
                sw_text.set("OFF")
            if type == "Real":
                func = self.button_function(sw_text, sw_bool, i)
            else:
                func = self.button_function_FFT(sw_text, sw_bool, i)
            sw_button = tk.Button(
                self.frame_list,
                textvariable=sw_text,
                command=func,
                width=3,
            )
            sw_button.grid(
                row=start_val + i + 1, column=10, padx=1, pady=0, ipadx=0, ipady=0
            )
            #
            switch_list.append(sw_bool)
        return check_list, var_list, switch_list

    def create_widgets_datalist(self):
        self.manage_init_setting()
        self.check_list = []
        self.check_list_FFT = []
        self.var_list = []
        self.var_list_FFT = []
        self.swith_list = []
        self.swith_list_FFT = []
        color = "#FFCDE2"
        real_text = tk.Label(
            self.frame_list, width=10, text="Real image", background=color
        )
        real_text.grid(row=2, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        #
        list_num = 2
        self.check_list, self.var_list, self.swith_list = self.list_form(
            self.processes, list_num, "Real"
        )
        #
        list_num += self.num_process_real + 4
        color = "#FFCDE2"
        FFT_text = tk.Label(
            self.frame_list, width=10, text="FFT image", background=color
        )
        FFT_text.grid(row=list_num, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        #

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
        FFT_method_cb.set(self.fft_func.method)
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
        FFT_window_cb.set(self.fft_func.window_func)
        #
        FFT_method_text.grid(
            row=list_num,
            column=1,
            padx=0,
            pady=0,
            ipadx=0,
            ipady=0,
        )
        FFT_method_cb.grid(
            row=list_num,
            column=2,
            padx=0,
            pady=0,
            ipadx=0,
            ipady=0,
        )
        FFT_window_text.grid(
            row=list_num,
            column=3,
            padx=0,
            pady=0,
            ipadx=0,
            ipady=0,
        )
        FFT_window_cb.grid(
            row=list_num,
            column=4,
            padx=0,
            pady=0,
            ipadx=0,
            ipady=0,
        )

        list_num += 1
        self.check_list_FFT, self.var_list_FFT, self.swith_list_FFT = self.list_form(
            self.processes_FFT, list_num, "FFT"
        )

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
        self.pro_fol_name.place(x=120, y=348)
        self.button_profolchoice.place(x=470, y=345)
        self.fol_choice_text_process.place(x=20, y=348)
        self.choice_process.place(x=120, y=378)
        self.choice_text_process.place(x=20, y=378)
        #
        self.comment_label.place(x=20, y=405)
        self.comment.place(x=120, y=405)

    def delete_all(self):
        self.processes = [self.processes[0]]
        self.processes_FFT = [self.processes_FFT[0]]
        self.create_frame_datalist()
        self.run_process()

    def delete_checked(self):
        self.rewrite_process()
        for i, chk in enumerate(self.check_list):
            k = i + 1
            if chk.get():
                self.processes[k] = None
        self.processes = [pro for pro in self.processes if pro is not None]
        for i, chk in enumerate(self.check_list_FFT):
            k = i + 1
            if chk.get():
                self.processes_FFT[k] = None
        self.processes_FFT = [pro for pro in self.processes_FFT if pro is not None]
        self.create_frame_datalist()
        self.run_process()

    def reload_process(self):
        self.rewrite_process()
        self.create_frame_datalist()
        self.run_process()

    def rewrite_process(self):
        for i, vars in enumerate(self.var_list):
            params = [var.get() for var in vars]
            self.processes[i].rewrite(params)
        self.fft_func.method = self.FFT_method_var.get()
        self.fft_func.window_func = self.FFT_window_var.get()
        for i, vars in enumerate(self.var_list_FFT):
            params = [var.get() for var in vars]
            self.processes_FFT[i].rewrite(params)

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

    def reflesh_process_list(self):
        self.process_list = self.read_process_list(self.dir_name_process)
        self.choice_process["values"] = self.process_list
        if len(self.process_list) > 0:
            self.choice_process.current(0)
            self.read_process_btn["state"] = tk.NORMAL

    def read_process_list(self, dir_name):
        process_list = glob.glob(dir_name + "\*")
        process_list = [os.path.basename(pathname) for pathname in process_list]
        process_list2 = [file for file in process_list if "process.txt" in file]
        return process_list2

    def read_process_clicked(self):
        data_path = self.dir_name_process + "\\" + self.choice_process.get()
        _ = self.read_process(data_path)

    def read_process(self, data_path, update=True):
        self.processes = [ImOpen()]
        self.processes_FFT = [ImOpen()]
        if os.path.isfile(data_path):
            with open(data_path) as f:
                lines = f.readlines()
                readcheck_real = True
                readchack_FFT = False
                for i, line in enumerate(lines):
                    values = line.split()
                    if len(values) == 0:
                        continue
                    process = None
                    if i == 0:
                        if "Process_record" not in values:
                            return False
                    if "FFT_params:" in values:
                        self.fft_func.read(values)

                        if values[3] == "True":
                            self.real_shown = False
                        elif values[3] == "False":
                            self.real_shown = True
                            self.fft_button["text"] = "Real\r →FFT"
                            # self.setting_real()
                    if values[0] == "Smoothing":
                        process = Smoothing()
                    elif values[0] == "Median":
                        process = Median()
                    elif values[0] == "Drift":
                        process = Drift()
                    elif values[0] == "Rescale":
                        process = Rescale()
                    elif values[0] == "Cut":
                        process = Cut()
                    elif values[0] == "Intensity":
                        process = Intensity()
                    elif values[0] == "Gamma":
                        process = Gamma()
                    elif values[0] == "Edge":
                        process = Edge()
                    elif values[0] == "Symmetrize":
                        process = Symm()
                    elif values[0] == "Angle":
                        process = Angle()
                    elif values[0] == "Squarize":
                        process = Square()
                    elif values[0] == "Oddize":
                        process = Odd()
                    elif values[0] == "Ave. sub.":
                        process = Average()
                    elif values[0] == "Mirror":
                        process = Mirror()
                    elif values[0] == "Ignore neg.":
                        process = Ignore_neg()
                    if process is not None:
                        process.read(values)
                        if readcheck_real:
                            self.processes.append(process)
                        elif readchack_FFT:
                            self.processes_FFT.append(process)
                    if "Real_params:" in values:
                        readcheck_real = True
                    if "FFT_params:" in values:
                        readcheck_real = False
                        readchack_FFT = True
                    if "Name_tag:" in values:
                        self.record_plus.delete(0, tk.END)
                        self.record_plus.insert(tk.END, values[1])
                        self.name_change = True

            if update:
                self.create_frame_datalist()
            # self.rewrite_process()
            if self.real_image.open_bool:
                self.run_process()
                self.show_image()
            return True
        else:
            return False

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

    def update_process_w(self):
        self.create_frame_datalist()