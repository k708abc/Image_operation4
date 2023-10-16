#!python3.11
import numpy as np
import matplotlib.pyplot as plt
import os
from spym.io import rhksm4
from PIL import Image
import cv2
import glob
import math
from skimage.filters import window
from skimage.measure import profile_line


class ImageList:
    dir_name = None
    images = []
    types = []

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
                check = self.check_text(data_path)
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
    x_pix_or = None
    y_pix_or = None
    x_size_or = None
    y_size_or = None
    data_type = "Real"
    upper = 255
    lower = 0
    data_path = None
    channel_name = None
    channel_val = None
    x_mag = 1
    y_mag = 1
    open_bool = False
    max_contrast = 255
    min_contrast = 0
    color_num = 0
    bias = None
    image_name = "Target"
    mouse_on = False
    mouse_x = 0
    mouse_y = 0
    line_on = False
    line_method = None
    line_points = []
    profiling_bool = False
    drag1 = False
    drag2 = False

    @property
    def x_current(self):
        return self.x_size_or * self.x_mag

    @property
    def y_current(self):
        return self.y_size_or * self.y_mag

    def initialize(self):
        self.upper = 255
        self.lower = 0
        self.x_mag = 1
        self.y_mag = 1

    def mag_update(self, val):
        self.x_mag = val[0]
        self.y_mag = val[1]

    def read_image(self):
        self.image_or, self.params = self.get_image_values()
        self.x_size_or = self.params[0]
        self.y_size_or = self.params[1]
        self.bias = self.params[2]
        self.y_pix_or, self.x_pix_or = self.image_or.shape[:2]
        self.open_bool = True
        self.image_mod = np.copy(self.image_or)
        self.default_contrast()

    def default_contrast(self):
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
        sm4data_im = sm4data_set[self.channel_val]
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

    def show_image(
        self,
    ):
        if self.open_bool:
            self.contrast_adjust()
            self.contrast_change()
            self.color_change()
            if self.line_on:
                self.draw_line()
            if self.mouse_on:
                cv2.namedWindow(self.image_name)
                cv2.setMouseCallback(self.image_name, self.mouse_event_point)
                self.draw_point()
            elif self.profiling_bool:
                self.get_profile()
                self.draw_line()
                cv2.namedWindow(self.image_name)
                cv2.setMouseCallback(self.image_name, self.mouse_event_line)
            cv2.imshow(self.image_name, self.image_show)

    def draw_point(self):
        self.color_change()
        self.image_show = cv2.circle(
            self.image_show, (self.mouse_x, self.mouse_y), 2, (0, 0, 255), -1
        )

    def mouse_event_point(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            self.mouse_x = x
            self.mouse_y = y
            self.draw_point()
            cv2.imshow(self.image_name, self.image_show)

    def mouse_event_line(self, event, x, y, flags, param):
        height, width = self.image_mod.shape[:2]
        if x < 0:
            x = 0
        if x >= width:
            x = width - 1
        if y < 0:
            y = 0
        if y >= height:
            y = height - 1
        if event == cv2.EVENT_LBUTTONDOWN:
            dis1 = (x - self.line_points[0][0][0]) ** 2 + (
                y - self.line_points[0][0][1]
            ) ** 2
            dis2 = (x - self.line_points[0][1][0]) ** 2 + (
                y - self.line_points[0][1][1]
            ) ** 2
            if dis1 <= dis2 and dis1 < 20:
                self.drag1 = True
                self.drag2 = False

            elif dis2 < dis1 and dis2 < 20:
                self.drag2 = True
                self.drag1 = False

        if event == cv2.EVENT_LBUTTONUP:
            if self.drag1:
                self.line_points[0][0][0] = x
                self.line_points[0][0][1] = y
                self.drag1 = False
            elif self.drag2:
                self.line_points[0][1][0] = x
                self.line_points[0][1][1] = y
                self.drag2 = False
            self.show_image()

        if self.drag1:
            self.line_points[0][0][0] = x
            self.line_points[0][0][1] = y
            self.draw_line()
            cv2.imshow(self.image_name, self.image_show)
        elif self.drag2:
            self.line_points[0][1][0] = x
            self.line_points[0][1][1] = y
            self.draw_line()
            cv2.imshow(self.image_name, self.image_show)

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
        self.color_change()
        height, width = self.image_show.shape[:2]
        color_line = (0, 0, 255)
        if self.line_method is None:
            pass
        elif self.line_method == "XY":
            cv2.line(
                self.image_show,
                (0, int(height / 2)),
                (int(width), int(height / 2)),
                color_line,
                1,
            )
            cv2.line(
                self.image_show,
                (int(width / 2), 0),
                (int(width / 2), int(height)),
                color_line,
                1,
            )
        elif self.line_method == "X":
            cv2.line(
                self.image_show,
                (0, int(height / 2)),
                (int(width), int(height / 2)),
                color_line,
                1,
            )

        elif self.line_method == "Six_fold":
            cv2.line(
                self.image_show,
                (0, int(height / 2)),
                (int(width), int(height / 2)),
                color_line,
                1,
            )
            cv2.line(
                self.image_show,
                (int(width / 2 - width / 2 / math.sqrt(3)), 0),
                (int(width / 2 + width / 2 / math.sqrt(3)), height),
                color_line,
                1,
            )
            cv2.line(
                self.image_show,
                (int(width / 2 + width / 2 / math.sqrt(3)), 0),
                (int(width / 2 - width / 2 / math.sqrt(3)), height),
                color_line,
                1,
            )
        color_line = [(0, 0, 255), (0, 255, 0)]
        for i, points in enumerate(self.line_points):
            cv2.arrowedLine(
                self.image_show,
                (points[0][0], points[0][1]),
                (points[1][0], points[1][1]),
                color_line[i],
                1,
            )
            cv2.drawMarker(
                self.image_show,
                (points[0][0], points[0][1]),
                color_line[i],
                markerType=cv2.MARKER_TILTED_CROSS,
                markerSize=15,
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

    def des_image(self):
        cv2.destroyWindow(self.image_name)
        self.open_bool = False

    def get_profile(self):
        _, width = self.image_show.shape[:2]
        start = (self.line_points[0][0][1], self.line_points[0][0][0])
        end = (self.line_points[0][1][1], self.line_points[0][1][0])
        length = (
            math.sqrt(
                (self.line_points[0][0][1] - self.line_points[0][1][1]) ** 2
                + (self.line_points[0][0][0] - self.line_points[0][1][0]) ** 2
            )
            / width
            * self.x_current
        )
        self.profile = profile_line(self.image_mod, start, end, linewidth=2)
        self.axis_x = np.linspace(0, length, len(self.profile))
        plt.clf()
        plt.plot(self.axis_x, self.profile)
        if self.data_type == "Real":
            plt.xlabel("Distance (nm)")
            plt.ylabel("Height (arb. unit))")
        else:
            plt.xlabel("Distance (nm-1)")
            plt.ylabel("Intensiy (arb. unit))")
        plt.tight_layout()
        plt.show(block=False)


class FFT:
    image = None
    method = "Sqrt"
    window_func = "None"
    image_mod = None
    method_table = ["Linear", "Sqrt", "Log"]
    window_table = ["None", "hann", "hamming", "blackman"]
    size_real_x = None
    size_real_y = None
    x_size = None
    y_size = None

    def datatype_change(self, image):
        maximum = np.max(image)
        minimum = np.min(image)
        image_mod = (image - minimum) / (maximum - minimum) * 255
        return image_mod.astype(np.uint8)

    def subtraction(self, image):
        minimum = np.min(image)
        return image - minimum

    def apply_window(self, image):
        if self.window_func == "None":
            target = self.subtraction(image)
        else:
            wimage = image * window(self.window_func, image.shape)
            target = self.subtraction(wimage)
        return target

    def fft_processing(self, w_image):
        fimage_or = np.fft.fft2(w_image)
        fimage_or = np.fft.fftshift(fimage_or)
        fimage_or = np.abs(fimage_or)
        return fimage_or

    def fft_scaling(self, image):
        if self.method == "Linear":
            fimage = image
        elif self.method == "Log":
            fimage = np.log(image, out=np.zeros_like(image), where=(image != 0))
        elif self.method == "Sqrt":
            fimage = np.sqrt(image)
        return fimage

    def cut_center(self, image):
        width, height = image.shape[1], image.shape[0]
        image_mod = np.copy(image)
        if width % 2 == 0:
            center_x = int(width / 2)
            center_y = int(height / 2)
        else:
            center_x = int((width - 1) / 2)
            center_y = int((height - 1) / 2)
        #
        value = (
            image_mod[center_y - 2][center_x - 2]
            + image_mod[center_y - 2][center_x + 2]
            + image_mod[center_y + 2][center_x - 2]
            + image_mod[center_y + 2][center_x + 2]
        ) / 4
        #
        image_mod[center_y - 1][center_x - 1] = value
        image_mod[center_y - 1][center_x] = value
        image_mod[center_y - 1][center_x + 1] = value
        image_mod[center_y][center_x - 1] = value
        image_mod[center_y][center_x] = value
        image_mod[center_y][center_x + 1] = value
        image_mod[center_y + 1][center_x - 1] = value
        image_mod[center_y + 1][center_x] = value
        image_mod[center_y + 1][center_x + 1] = value
        return image_mod

    def run(self):
        image_mod = self.datatype_change(self.image)
        w_image = self.apply_window(image_mod)
        fft_image = self.fft_processing(w_image)
        fft_image = self.fft_scaling(fft_image)
        fft_image = fft_image.astype(np.float32)
        fft_image = self.cut_center(fft_image)
        self.cal_fft_size()
        return fft_image

    def cal_fft_size(self):
        height, width = self.image.shape[:2]
        self.x_size = 1 / self.size_real_x * width
        self.y_size = 1 / self.size_real_y * height

    def rec(self, real_shown):
        if real_shown is True:
            txt = (
                "FFT_params:"
                + "\t"
                + self.method
                + "\t"
                + self.window_func
                + "\t"
                + "False"
                + "\n"
            )
        else:
            txt = (
                "FFT_params:"
                + "\t"
                + self.method
                + "\t"
                + self.window_func
                + "\t"
                + "True"
                + "\n"
            )
        return txt

    def read(self, values):
        self.window_func = values[2]
        self.method = values[1]
