#!python3.11
import numpy as np
import os
from spym.io import rhksm4
from PIL import Image
import cv2
import glob
import math


class ImageList:
    dir_name = None
    images = None
    types = None

    def formlist(self):
        image_list = [
            os.path.basename(pathname) for pathname in glob.glob(self.dir_name + "\*")
        ]
        self.images = []
        self.types = []
        for file in image_list:
            data_path = self.dir_name + "\\" + file
            data_type = os.path.splitext(data_path)
            if data_type[1] == ".bmp":
                self.images.append(file)
                self.types.append(["bmp"])
            elif data_type[1] == ".txt":
                check = self.check_text(file)
                if check:
                    self.images.append(file)
                    self.types.append(["txt"])
            elif data_type[1] == ".SM4":
                self.images.append(file)
                self.types.append(self.datatypes(data_path))
            else:
                pass

    def check_text(self, data_path):
        with open(data_path) as f:
            lines = f.readlines()
            for line in lines:
                values = line.split()
                if "Data:" in values:
                    return True
        return False

    def datatypes(self, data_path):
        sm4data = rhksm4.load(data_path)
        data_type_list = []
        data_num = 0
        while True:
            try:
                data = sm4data[data_num]
                data_type_list.append(
                    data.attrs["RHK_Label"] + "(" + data.attrs["RHK_ScanTypeName"] + ")"
                )
                data_num += 1
            except:
                break
        return data_type_list


class MyImage:
    image_or = None
    image_prev = None
    image_mod = None
    image_cad = None
    image_show = None
    x_or = None
    y_or = None
    upper = 255
    lower = 0
    data_path = None
    channel_name = None
    x_mag = 1
    y_mag = 1
    open_bool = False
    max_contrast = 255
    min_contrast = 0
    color_num = 0
    line_method = None

    def initialize(self):
        self.upper = 255
        self.lower = 0
        self.x_mag = 1
        self.y_mag = 1

    def read_image(self):
        self.image_or, self.scan_params = self.get_image_values()
        self.y_or, self.x_or = self.image_or.shape[:2]
        self.open_bool = True
        self.image_mod = np.copy(self.image_or)
        self.max_contrast = np.max(self.image_mod)
        self.min_contrast = np.min(self.image_mod)

    def get_image_values(self):
        data_type = os.path.splitext(self.data_path)
        if data_type[1] == ".SM4":
            data, scan_params = self.sm4_getdata()
        elif data_type[1] == ".bmp":
            data, scan_params = self.bmp_getdata()
        elif data_type[1] == ".txt":
            data, scan_params = self.txt_getdata()
        return data, scan_params

    def sm4_getdata(self):
        sm4data_set = rhksm4.load(self.data_path)
        sm4data_im = sm4data_set[self.channel_name]
        image_data = sm4data_im.data
        image_data = image_data.astype(np.float32)
        scan_params = [
            -round(
                sm4data_im.attrs["RHK_Xscale"]
                * sm4data_im.attrs["RHK_Xsize"]
                * 1000000000,
                1,
            ),
            -round(
                sm4data_im.attrs["RHK_Yscale"]
                * sm4data_im.attrs["RHK_Ysize"]
                * 1000000000,
                1,
            ),
            sm4data_im.attrs["RHK_Bias"],
        ]
        return image_data, scan_params

    def bmp_getdata(self):
        bmpdata_im = np.array(Image.open(self.data_path).convert("L"), dtype=np.float32)
        scan_params = [
            30,
            round(30 / bmpdata_im.shape[1] * bmpdata_im.shape[0], 2),
            0,
        ]
        return bmpdata_im, scan_params

    def txt_getdata(self):
        with open(self.data_path) as f:
            lines = f.readlines()
            read_check = False
            text_data = []
            for line in lines:
                values = line.split()
                if "Peaks:" in values:
                    read_check = False
                if read_check is True:
                    text_data.append([])
                    for val in values:
                        if val == "\n":
                            pass
                        else:
                            text_data[-1].append(float(val))

                if "Data:" in values:
                    read_check = True

                if "Current_size_X:" in values:
                    xsize = float(values[1])
                if "Current_size_Y:" in values:
                    ysize = float(values[1])
                if "STM_bias:" in values:
                    bias = float(values[1]) / 1000
        data_np = np.array(text_data, dtype=np.float32)
        if read_check:
            return data_np, [xsize, ysize, bias]
        else:
            return False, False

    def show_image(self):
        if self.open_bool:
            self.contrast_adjust()
            self.contrast_change()
            self.draw_line()
            self.color_change()
            # self.size_update()
            # self.pix_update()
            cv2.imshow("Target", self.image_show)

    def contrast_adjust(self):
        image = (
            (self.image_mod - self.min_contrast)
            / (self.max_contrast - self.min_contrast)
            * 255
        )
        image[image > 255] = 255
        image[image < 0] = 0
        self.image_cad = image.astype(np.uint8)

    def contrast_change(self):
        LUT = self.get_LUT()
        self.image_cad = cv2.LUT(self.image_cad, LUT)

    def get_LUT(self):
        LUT = np.zeros((256, 1), dtype="uint8")
        maximum = int(self.upper)
        minimum = int(self.lower)
        if maximum == minimum:
            for i in range(-50, 301):
                if i < maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 0
                elif i == maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = maximum
                else:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255
        elif maximum > minimum:
            diff = 255 / (maximum - minimum)
            k = 0
            for i in range(-50, 301):
                if i < minimum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 0
                elif i <= maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = int(diff * k)
                    k = k + 1
                else:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255
        else:
            diff = 255 / (maximum - minimum)
            k = 0
            for i in range(-50, 301):
                if i < maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255
                elif i <= minimum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255 + int(diff * k)
                    k = k + 1
                else:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 0
        return LUT

    def draw_line(self):
        height, width = self.image_cad.shape[:2]
        color_line = 255
        if self.line_method == None:
            pass
        elif self.line_method == "XY":
            cv2.line(
                self.image_cad,
                (0, int(height / 2)),
                (int(width), int(height / 2)),
                color_line,
                1,
            )
            cv2.line(
                self.image_cad,
                (int(width / 2), 0),
                (int(width / 2), int(height)),
                color_line,
                1,
            )
        elif self.line_method == "X":
            cv2.line(
                self.image_cad,
                (0, int(height / 2)),
                (int(width), int(height / 2)),
                color_line,
                1,
            )

        elif self.line_method == "Six_fold":
            cv2.line(
                self.image_cad,
                (0, int(height / 2)),
                (int(width), int(height / 2)),
                color_line,
                1,
            )
            cv2.line(
                self.image_cad,
                (int(width / 2 - width / 2 / math.sqrt(3)), 0),
                (int(width / 2 + width / 2 / math.sqrt(3)), height),
                color_line,
                1,
            )
            cv2.line(
                self.image_cad,
                (int(width / 2 + width / 2 / math.sqrt(3)), 0),
                (int(width / 2 - width / 2 / math.sqrt(3)), height),
                color_line,
                1,
            )

    def color_change(self):
        if self.color_num == 0:
            self.image_show = cv2.cvtColor(self.image_cad, cv2.COLOR_GRAY2BGR)
        else:
            self.image_show = cv2.applyColorMap(self.image_cad, self.color_num - 1)

    def set_default(self):
        if self.open_bool:
            self.max_contrast, self.min_contrast = (
                self.max_contrast - self.min_contrast
            ) / 255 * self.upper + self.min_contrast, (
                self.max_contrast - self.min_contrast
            ) / 255 * self.lower + self.min_contrast

    def back_default(self):
        if self.open_bool:
            self.max_contrast = np.max(self.image_mod)
            self.min_contrast = np.min(self.image_mod)
