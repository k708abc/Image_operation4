#!python3.12

from typing import Dict
import tkinter as tk


class Layouts:
    padWE: Dict = dict(sticky=(tk.W, tk.E), padx=15, pady=2)

    def create_layout_choice(self) -> None:
        self.fol_choice_text.grid(row=0, column=0, **self.padWE)
        self.fol_name.grid(row=0, column=1, **self.padWE)
        self.button_folchoice.grid(row=0, column=2, **self.padWE)
        self.choice.grid(row=1, column=1, **self.padWE)
        self.choice_text.grid(row=1, column=0, **self.padWE)
        self.imtype_choice.grid(row=2, column=1, **self.padWE)
        self.imtype_text.grid(row=2, column=0, **self.padWE)
        self.button_imopen.grid(rowspan=2, row=1, column=2, sticky=tk.N + tk.S)

    def create_layout_contrast(self) -> None:
        self.upper_text.grid(row=0, column=0, **self.padWE)
        self.scale_upper.grid(columnspan=4, row=0, column=1, **self.padWE)
        self.lower_text.grid(row=1, column=0, **self.padWE)
        self.scale_lower.grid(columnspan=4, row=1, column=1, **self.padWE)
        self.default_button.grid(rowspan=2, row=0, column=5, sticky=tk.N + tk.S)
        self.set_as_default_button.grid(rowspan=2, row=0, column=6, sticky=tk.N + tk.S)
        self.autoset_text.grid(row=2, column=0, **self.padWE)
        self.upper_set_text.grid(row=2, column=3, **self.padWE)
        self.lower_set_text.grid(row=2, column=1, **self.padWE)
        self.upper_set_entry.grid(row=2, column=4, **self.padWE)
        self.lower_set_entry.grid(row=2, column=2, **self.padWE)
        self.auto_set_button.grid(columnspan=2, row=2, column=5, **self.padWE)

    def create_layout_cb(self):
        self.cb_color_text.grid(row=0, column=0, **self.padWE)
        self.cb_color.grid(columnspan=3, row=0, column=1, **self.padWE)
        self.cb_smooth_text.grid(row=1, column=0, **self.padWE)
        self.smooth_entry.grid(row=1, column=1, **self.padWE)
        self.cb_smooth_unit.grid(row=1, column=2, **self.padWE)
        self.cb_median_text.grid(row=1, column=3, **self.padWE)
        self.median_entry.grid(row=1, column=4, **self.padWE)
        self.cb_median_unit.grid(row=1, column=5, **self.padWE)

    def create_layout_drift(self):
        self.drift_text.grid(row=0, column=0, **self.padWE)
        self.drift_dx_text.grid(row=0, column=1, **self.padWE)
        self.drift_dx.grid(row=0, column=2, **self.padWE)
        self.drift_dy_text.grid(row=0, column=3, **self.padWE)
        self.drift_dy.grid(row=0, column=4, **self.padWE)
        self.drift_cb.grid(columnspan=2, row=1, column=1, **self.padWE)
        self.drift_button.grid(columnspan=2, row=1, column=3, **self.padWE)

    def create_layout_rescale(self):
        self.rescale_text.grid(row=0, column=0, **self.padWE)
        self.rescale_all.grid(row=0, column=1, **self.padWE)
        self.rescale_label_x.grid(row=0, column=2, **self.padWE)
        self.rescale_x.grid(row=0, column=3, **self.padWE)
        self.rescale_label_y.grid(row=0, column=4, **self.padWE)
        self.rescale_y.grid(row=0, column=5, **self.padWE)

    def create_layout_cut(self):
        self.cut_text.grid(row=0, column=0, **self.padWE)
        self.cut_entry.grid(row=0, column=1, **self.padWE)

    def create_layout_int(self):
        self.int_text.grid(row=0, column=0, **self.padWE)
        self.int_cb.grid(row=0, column=1, **self.padWE)
        self.int_gamma.grid(row=0, column=2, **self.padWE)
        self.int_entry.grid(row=0, column=3, **self.padWE)

    def create_layout_edge(self):
        self.edge_text.grid(row=0, column=0, **self.padWE)
        self.edge_cb.grid(row=0, column=1, **self.padWE)
        self.edge_range.grid(row=0, column=2, **self.padWE)
        self.edge_entry.grid(row=0, column=3, **self.padWE)
        self.mulor_check.grid(row=0, column=4, **self.padWE)

    def create_layout_sym(self):
        self.sym_text.grid(row=0, column=0, **self.padWE)
        self.method_symmetrize_cb.grid(row=0, column=1, **self.padWE)
        self.angle_text.grid(row=0, column=3, **self.padWE)
        self.angle_entry.grid(row=0, column=4, **self.padWE)

    def create_layout_line(self):
        self.line_text.grid(row=1, column=0, **self.padWE)
        self.method_line_cb.grid(row=1, column=1, **self.padWE)

    def create_layout_checks(self):
        self.square_check.grid(row=0, column=0, **self.padWE)
        self.oddize_check.grid(row=0, column=1, **self.padWE)
        self.average_check.grid(row=0, column=2, **self.padWE)
        self.mirror_check.grid(row=1, column=0, **self.padWE)
        self.ignore_neg_check.grid(row=1, column=1, **self.padWE)

    def create_layout_size(self):
        self.original_size_text.grid(row=0, column=0, **self.padWE)
        self.original_x_text.grid(row=0, column=1, **self.padWE)
        self.original_x.grid(row=0, column=2, **self.padWE)
        self.orpix_x.grid(row=0, column=3, **self.padWE)
        self.original_y_text.grid(row=0, column=4, **self.padWE)
        self.original_y.grid(row=0, column=5, **self.padWE)
        self.orpix_y.grid(row=0, column=6, **self.padWE)
        self.current_size_text.grid(row=1, column=0, **self.padWE)
        self.current_x_text.grid(row=1, column=1, **self.padWE)
        self.current_x.grid(row=1, column=2, **self.padWE)
        self.current_pxx.grid(row=1, column=3, **self.padWE)
        self.current_y_text.grid(row=1, column=4, **self.padWE)
        self.current_y.grid(row=1, column=5, **self.padWE)
        self.current_pxy.grid(row=1, column=6, **self.padWE)

    def create_layout_bias(self):
        self.bias_text.grid(row=0, column=0, **self.padWE)
        self.bias.grid(row=0, column=1, **self.padWE)

    def create_layout_fft(self):
        self.fft_button.grid(
            columnspan=3, rowspan=2, row=0, column=0, sticky=tk.N + tk.S
        )
        self.method_text.grid(row=0, column=3, **self.padWE)
        self.method_fft_cb.grid(row=0, column=4, **self.padWE)
        self.window_text.grid(row=1, column=3, **self.padWE)
        self.window_cb.grid(row=1, column=4, **self.padWE)

    def create_layout_profile(self):
        self.profile_button.grid(
            columnspan=2, rowspan=2, row=0, column=0, sticky=tk.N + tk.S
        )

    def create_layout_record(self):
        self.fol_choice_text_record.grid(row=0, column=0, **self.padWE)
        self.rec_fol_name.grid(columnspan=2, row=0, column=1, **self.padWE)
        self.button_recfolchoice.grid(row=0, column=3, **self.padWE)
        #
        self.record_text.grid(row=1, column=0, **self.padWE)
        self.record.grid(columnspan=2, row=1, column=1, **self.padWE)
        self.record_plus.grid(row=1, column=3, **self.padWE)
        self.dirdiv_check.grid(row=2, column=3, **self.padWE)

    def create_layout_buttons(self):
        self.record_button.grid(row=0, column=0, **self.padWE)
        self.close_button.grid(row=0, column=1, **self.padWE)
        self.process_button.grid(row=0, column=2, **self.padWE)
