import cv2
import os
import matplotlib.pyplot as plt


class Recording:
    def folder_check(self, folder):
        if os.path.isdir(folder):
            pass
        else:
            os.makedirs(folder)

    def recording_text(self):
        if self.dirdiv_bool.get():
            fol_add = "textIm_" + self.record_plus.get() + "\\"
            self.folder_check(self.dir_name_rec + "\\" + fol_add)
            txt_name = (
                self.dir_name_rec
                + "\\"
                + fol_add
                + self.record.get()
                + self.record_plus.get()
                + ".txt"
            )
        else:
            txt_name = (
                self.dir_name_rec
                + "\\"
                + self.record.get()
                + self.record_plus.get()
                + ".txt"
            )
        with open(txt_name, mode="w") as f:
            f.write(self.record.get() + self.record_plus.get() + "\n")
            f.write("Image_name:" + "\t" + self.real_image.data_path + "\n")
            f.write("Channel:" + "\t" + self.real_image.channel_name + "\n\n")
            f.write("Orizinal_size_X:" + "\t" + str(self.real_image.x_size_or) + "\n")
            f.write("Orizinal_size_Y:" + "\t" + str(self.real_image.y_size_or) + "\n")

            if self.real_shown:
                f.write(
                    "Current_size_X:" + "\t" + str(self.real_image.x_current) + "\n"
                )
                f.write(
                    "Current_size_Y:" + "\t" + str(self.real_image.x_current) + "\n"
                )
                f.write(
                    "Pixcel_X" + "\t" + str(self.real_image.image_show.shape[1]) + "\n"
                )
                f.write(
                    "Pixcel_Y" + "\t" + str(self.real_image.image_show.shape[0]) + "\n"
                )
                f.write("data_type:" + "\t" + "Real" + "\n")
            else:
                f.write("Current_size_X:" + "\t" + str(self.fft_image.x_current) + "\n")
                f.write("Current_size_Y:" + "\t" + str(self.fft_image.x_current) + "\n")
                f.write(
                    "Pixcel_X" + "\t" + str(self.fft_image.image_show.shape[1]) + "\n"
                )
                f.write(
                    "Pixcel_Y" + "\t" + str(self.fft_image.image_show.shape[0]) + "\n"
                )
                f.write("data_type:" + "\t" + "FFT" + "\n")
            f.write("STM_bias:" + "\t" + str(self.real_image.bias) + "\n\n")
            #
            f.write("Data:" + "\n")
            if self.real_shown:
                for row in self.real_image.image_mod:
                    for values in row:
                        f.write(str(values) + "\t")
                    f.write("\n")
            else:
                for row in self.fft_image.image_mod:
                    for values in row:
                        f.write(str(values) + "\t")
                    f.write("\n")

        if self.dirdiv_bool.get():
            fol_add = "Process_" + self.record_plus.get() + "\\"
            self.folder_check(self.dir_name_rec + "\\" + fol_add)
            txt_name = (
                self.dir_name_rec
                + "\\"
                + fol_add
                + self.record.get()
                + self.record_plus.get()
                + "_process.txt"
            )
        else:
            txt_name = (
                self.dir_name_rec
                + "\\"
                + self.record.get()
                + self.record_plus.get()
                + "_process.txt"
            )
        with open(txt_name, mode="w") as f:
            f.write("Process_record" + "\n")
            f.write(self.record.get() + self.record_plus.get() + "\n")
            f.write("Image_name:" + "\t" + self.image_name + "\n")
            f.write("Name_tag:" + "\t" + self.record_plus.get() + "\n\n")
            f.write("Real_params:" + "\n")
            for pro in self.processes:
                f.write(pro.rec())
            f.write("\n")

            if self.fft_func.image is not None:
                f.write(self.fft_func.rec(self.real_shown))
                for pro in self.processes_FFT:
                    f.write(pro.rec())

    def rec_image(self):
        if self.dirdiv_bool.get():
            fol_add = "BMP_" + self.record_plus.get() + "\\"
            self.folder_check(self.dir_name_rec + "\\" + fol_add)
            img_name = (
                self.dir_name_rec
                + "\\"
                + fol_add
                + self.record.get()
                + self.record_plus.get()
                + ".bmp"
            )
        else:
            img_name = (
                self.dir_name_rec
                + "\\"
                + self.record.get()
                + self.record_plus.get()
                + ".bmp"
            )
        if self.real_shown:
            cv2.imwrite(img_name, self.real_image.image_show)
        else:
            cv2.imwrite(img_name, self.fft_image.image_show)

    def rec_profile(self):
        if self.dirdiv_bool.get():
            fol_add = "Prof_" + self.record_plus.get() + "\\"
            self.folder_check(self.dir_name_rec + "\\" + fol_add)
            img_name = (
                self.dir_name_rec
                + "\\"
                + fol_add
                + self.record.get()
                + self.record_plus.get()
                + ".png"
            )
            txt_name = (
                self.dir_name_rec
                + "\\"
                + fol_add
                + self.record.get()
                + self.record_plus.get()
                + ".txt"
            )
        else:
            img_name = (
                self.dir_name_rec
                + "\\"
                + self.record.get()
                + self.record_plus.get()
                + ".png"
            )
            txt_name = (
                self.dir_name_rec
                + "\\"
                + self.record.get()
                + self.record_plus.get()
                + ".txt"
            )
        plt.savefig(img_name, format="png")
        if self.real_shown:
            x = self.real_image.axis_x
            y = self.real_image.profile
        else:
            x = self.fft_image.axis_x
            y = self.fft_image.profile
        with open(txt_name, mode="w") as f:
            f.write("Profiling record" + "\n")
            f.write("Image_name:" + "\t" + self.real_image.data_path + "\n")
            f.write("Channel:" + "\t" + self.real_image.channel_name + "\n\n")
            f.write("x" + "\t" + "y" + "\n")
            for xval, yval in zip(x, y):
                f.write(str(xval) + "\t" + str(yval) + "\n")
