#!python3.12
from scipy import ndimage
import numpy as np
import cv2


class ImOpen:
    name = "Im_open"
    image = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def run(self):
        return self.image

    def rewrite(self, params):
        pass

    def rec(self):
        return ""

    def read(self, vals):
        pass


class Smoothing:
    name = "Smoothing"
    range = None
    params = ["range"]
    params_type = ["entry"]
    image = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y

    def rewrite(self, params):
        self.range = float(params[0])

    def getval(self, p_name):
        if p_name == "range":
            return self.range

    def run(self):
        image_mod = ndimage.gaussian_filter(self.image, float(self.range))
        return image_mod

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.range = float(vals[i + 1])
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Median:
    name = "Median"
    range = None
    params = ["range"]
    params_type = ["entry"]
    image = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        self.range = int(float(params[0]))

    def getval(self, p_name):
        if p_name == "range":
            return self.range

    def run(self):
        if int(float(self.range)) <= 0:
            image_mod = self.image
        else:
            image_mod = ndimage.median_filter(self.image, int(float(self.range)))
        return image_mod

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.range = int(float(vals[i + 1]))
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Drift:
    name = "Drift"
    image = None
    x = None
    y = None
    params = ["x", "y"]
    params_type = ["entry", "entry"]
    cal = None
    switch = True
    type = None
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        self.x = float(params[0])
        self.y = float(params[1])

    def getval(self, p_name):
        if p_name == "x":
            return self.x
        if p_name == "y":
            return self.y

    def run(self):
        min_val = np.min(self.image).tolist()
        ps_y, ps_x = self.image.shape[:2]
        #
        v11 = 1 + self.x / 2 / ps_y / ps_y
        v12 = self.x / ps_y
        v21 = self.y / 2 / ps_y / ps_x
        v22 = 1 + self.y / ps_y
        #
        if v12 < 0:
            x_shift = -v12 * ps_y
        else:
            x_shift = 0
        mat = np.array([[v11, v12, x_shift], [v21, v22, 0]], dtype=np.float32)
        affine_img = cv2.warpAffine(
            self.image, mat, (2 * ps_x, 2 * ps_y), borderValue=min_val
        )
        # calculate the edge of the image
        ax = v11 * ps_x
        ay = v21 * ps_x
        bx = v12 * ps_y
        by = v22 * ps_y
        #
        x0 = int(min(bx, 0) + x_shift)
        y0 = int(min(ay, 0))
        xmax = int(max(ax, bx, ax + bx) + x_shift)
        ymax = int(max(by, by + ay, ay))
        # crop the image
        im_crop = affine_img[y0:ymax, x0:xmax]
        self.mag_rate_x = (xmax - x0) / ps_x
        self.mag_rate_y = (ymax - y0) / ps_y
        return im_crop

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.x = float(vals[i + 1])
            if vals[i] == self.params[1]:
                self.y = float(vals[i + 1])
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Rescale:
    name = "Rescale"
    image = None
    all = 1
    x = 1
    y = 1
    params = ["All", "X", "Y"]
    params_type = ["entry", "entry", "entry"]
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        self.all = float(params[0])
        self.x = float(params[1])
        self.y = float(params[2])

    def getval(self, p_name):
        if p_name == "All":
            return self.all
        if p_name == "X":
            return self.x
        if p_name == "Y":
            return self.y

    def run(self):
        or_y, or_x = self.image.shape[:2]
        width_x = int(or_x * float(self.x) * float(self.all))
        height_y = int(or_y * float(self.y) * float(self.all))
        modified_image = cv2.resize(self.image, (width_x, height_y))
        self.mag_rate_x = self.x
        self.mag_rate_y = self.y
        return modified_image

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.all = float(vals[i + 1])
            if vals[i] == self.params[1]:
                self.x = float(vals[i + 1])
            if vals[i] == self.params[2]:
                self.y = float(vals[i + 1])
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Cut:
    name = "Cut"
    image = None
    ratio = None
    params = ["ratio"]
    params_type = ["entry"]
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        self.ratio = float(params[0])

    def getval(self, p_name):
        if p_name == "ratio":
            return self.ratio

    def run(self):
        if self.ratio == 100:
            self.mag_rate_x = 1
            self.mag_rate_y = 1
            return self.image
        else:
            half_ratio = self.ratio / 200
            height, width = self.image.shape[:2]
            diff_h = int(height * half_ratio)
            diff_w = int(width * half_ratio)
            image_cropped = self.image[
                diff_h : height - diff_h, diff_w : width - diff_w
            ]
            self.mag_rate_x = 2 * diff_w / width
            self.mag_rate_y = 2 * diff_h / height
            return image_cropped

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.ratio = float(vals[i + 1])
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Intensity:
    name = "Intensity"
    image = None
    method = None
    params = ["method"]
    params_type = ["combo_box"]
    method_list = ["Normal", "Log", "Sqrt"]
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def get_list(self, name):
        return self.method_list

    def rewrite(self, params):
        self.method = params[0]

    def getval(self, p_name):
        if p_name == "method":
            return self.method

    def pos_offset(self, image, base):
        minimum = image.min()
        image_off = image - minimum + base
        return image_off

    def run(self):
        if self.method == "Normal":
            return self.image
        elif self.method == "Log":
            image_mod = self.pos_offset(self.image, 1)
            image_mod = np.log(
                image_mod,
                out=np.zeros_like(image_mod),
                where=(image_mod != 0),
            )
            return image_mod
        elif self.method == "Sqrt":
            image_mod = self.pos_offset(self.image, 0)
            image_mod = np.sqrt(
                image_mod,
            )
        return image_mod

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.method = vals[i + 1]
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Gamma:
    name = "Gamma"
    image = None
    val = None
    params = ["val"]
    params_type = ["entry"]
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        self.val = float(params[0])

    def getval(self, p_name):
        if p_name == "val":
            return self.val

    def run(self):
        image_mod = self.image
        # あとで
        return image_mod

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.val = float(vals[i + 1])
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Edge:
    name = "Edge"
    image = None
    method = None
    const = None
    mul_or = None
    params = ["method", "const.", "mul. or."]
    params_type = ["combo_box", "entry", "check_box"]
    method_list = [
        "None",
        "Sobel_x",
        "Sobel_y",
        "Laplacian",
        "Curvature",
    ]
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def get_list(self, name):
        return self.method_list

    def rewrite(self, params):
        self.method = params[0]
        self.const = float(params[1])
        self.mul_or = bool(params[2])

    def getval(self, p_name):
        if p_name == "method":
            return self.method
        elif p_name == "const.":
            return self.const
        elif p_name == "mul. or.":
            return self.mul_or

    def get_kernel(self, k):
        kernel = float(k)
        if kernel > 0 and kernel < 2:
            kernel = 1
        elif kernel >= 2 and kernel < 4:
            kernel = 3
        elif kernel >= 4 and kernel < 6:
            kernel = 5
        elif kernel >= 6 and kernel < 8:
            kernel = 7
        elif kernel == -1:
            kernel = -1
        else:
            kernel = 3
        return kernel

    def curvature_formation(self):
        kernel_dfdx = np.array([[0, 0, 0], [-0.5, 0, 0.5], [0, 0, 0]])
        kernel_dfdy = np.array([[0, -0.5, 0], [0, 0, 0], [0, 0.5, 0]])
        kernel_d2fdx2 = np.array([[0, 0, 0], [0.25, -0.5, 0.25], [0, 0, 0]])
        kernel_d2fdy2 = np.array([[0, 0.25, 0], [0, -0.5, 0], [0, 0.25, 0]])
        kernel_d2fdxdy = np.array([[0.25, 0, -0.25], [0, 0, 0], [-0.25, 0, 0.25]])
        #
        im_dfdx = cv2.filter2D(self.image, -1, kernel_dfdx)
        im_dfdy = cv2.filter2D(self.image, -1, kernel_dfdy)
        im_d2fdx2 = cv2.filter2D(self.image, -1, kernel_d2fdx2)
        im_d2fdy2 = cv2.filter2D(self.image, -1, kernel_d2fdy2)
        im_d2fdxdy = cv2.filter2D(self.image, -1, kernel_d2fdxdy)
        im_const = np.full(
            (self.image.shape[0], self.image.shape[1]),
            self.const,
            dtype=type(self.image[0][0]),
        )
        #
        image_cur_upper = (
            (im_const + im_dfdx**2) * im_d2fdy2
            - 2 * im_dfdx * im_dfdy * im_d2fdxdy
            + (im_const + im_dfdy**2) * im_d2fdx2
        )
        image_cur_lower = (im_const + im_dfdx**2 + im_dfdy**2) ** (1.5)
        image_cur = image_cur_upper / image_cur_lower
        return image_cur

    def pos_offset(self, image, base):
        minimum = image.min()
        image_off = image - minimum + base
        return image_off

    def run(self):
        if self.method == "None":
            return self.image
        elif self.method == "Sobel_x":
            kernel = self.get_kernel(self.const)
            image_mod = cv2.Sobel(self.image, cv2.CV_32F, 1, 0, ksize=kernel)
        elif self.method == "Sobel_y":
            kernel = self.get_kernel(self.const)
            image_mod = cv2.Sobel(self.image, cv2.CV_32F, 0, 1, ksize=kernel)
        elif self.method == "Laplacian":
            image_mod = cv2.Laplacian(self.image, cv2.CV_32F) * (-1)
        elif self.method == "Curvature":
            image_mod = self.curvature_formation() * (-1)

        if (self.mul_or is True) or (self.mul_or == "True"):
            image_mul = self.pos_offset(self.image, 1)
            image_mod = image_mod * image_mul
        return image_mod

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.method = vals[i + 1]
            if vals[i] == self.params[1]:
                self.const = float(vals[i + 1])
            if vals[i] == self.params[2]:
                self.mul_or = bool(vals[i + 1])
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Symm:
    name = "Symmetrize"
    image = None
    method = None
    params = ["method"]
    params_type = ["combo_box"]
    method_list = [
        "None",
        "mirror_X",
        "mirror_XY",
        "six_fold",
        "six_fold+mirror",
    ]
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        self.method = params[0]

    def getval(self, p_name):
        if p_name == "method":
            return self.method

    def get_list(self, name):
        return self.method_list

    def run(self):
        height, width = self.image.shape[:2]
        center = (int(width / 2), int(height / 2))
        min_val = np.min(self.image).tolist()
        if self.method == "None":
            image_sym = self.image
        elif self.method == "mirror_XY":
            image2 = cv2.flip(self.image / 4, 0)
            image3 = cv2.flip(self.image / 4, 1)
            image4 = cv2.flip(self.image / 4, -1)
            image5 = cv2.add(self.image / 4, image2)
            image6 = cv2.add(image3, image4)
            image_sym = cv2.add(image5, image6)

        elif self.method == "mirror_X":
            image2 = cv2.flip(self.image / 2, 0)
            image_sym = cv2.add(self.image / 2, image2)

        elif self.method == "six_fold":
            affine_60 = cv2.getRotationMatrix2D(center, 60, 1)
            image2 = cv2.warpAffine(
                self.image,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image3 = cv2.warpAffine(
                image2,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image4 = cv2.warpAffine(
                image3,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image5 = cv2.warpAffine(
                image4,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image6 = cv2.warpAffine(
                image5,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )

            image_s = cv2.add(self.image / 6, image2 / 6)
            image_p = cv2.add(image3 / 6, image4 / 6)
            image_k = cv2.add(image5 / 6, image6 / 6)
            image7 = cv2.add(image_s, image_p)
            image_sym = cv2.add(image7, image_k)

        elif self.method == "six_fold+mirror":
            affine_60 = cv2.getRotationMatrix2D(center, 60, 1)

            image2 = cv2.warpAffine(
                self.image,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image3 = cv2.warpAffine(
                image2,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image4 = cv2.warpAffine(
                image3,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
            )
            image5 = cv2.warpAffine(
                image4,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image6 = cv2.warpAffine(
                image5,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )

            image_m1 = cv2.flip(self.image, 0)
            image_m2 = cv2.warpAffine(
                image_m1,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image_m3 = cv2.warpAffine(
                image_m2,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
            )
            image_m4 = cv2.warpAffine(
                image_m3,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image_m5 = cv2.warpAffine(
                image_m4,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )
            image_m6 = cv2.warpAffine(
                image_m5,
                affine_60,
                (width, height),
                flags=cv2.INTER_CUBIC,
                borderValue=min_val,
            )

            image_s = cv2.add(self.image / 12, image2 / 12)
            image_p = cv2.add(image3 / 12, image4 / 12)
            image_k = cv2.add(image5 / 12, image6 / 12)

            image_ms = cv2.add(image_m1 / 12, image_m2 / 12)
            image_mp = cv2.add(image_m3 / 12, image_m4 / 12)
            image_mk = cv2.add(image_m5 / 12, image_m6 / 12)

            image_q = cv2.add(image_s, image_p)
            image_w = cv2.add(image_k, image_ms)
            image_e = cv2.add(image_mp, image_mk)

            image7 = cv2.add(image_q, image_w)
            image_sym = cv2.add(image7, image_e)
        return image_sym

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.method = vals[i + 1]
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Angle:
    name = "Angle"
    image = None
    angle = None
    params = ["angle"]
    params_type = ["entry"]
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        self.angle = float(params[0])

    def getval(self, p_name):
        if p_name == "angle":
            return self.angle

    def run(self):
        height, width = self.image.shape[:2]
        center = (int(width / 2), int(height / 2))
        min_val = np.min(self.image).tolist()
        affine_trans = cv2.getRotationMatrix2D(center, self.angle, 1)
        r_image = cv2.warpAffine(
            self.image,
            affine_trans,
            (width, height),
            flags=cv2.INTER_CUBIC,
            borderValue=min_val,
        )
        return r_image

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.angle = float(vals[i + 1])
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Square:
    name = "Squarize"
    image = None
    params = []
    params_type = []
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        pass

    def getval(self, p_name):
        return

    def run(self):
        height, width = self.image.shape[:2]
        if height == width:
            image = self.image
            self.mag_rate_x = 1
            self.mag_rate_y = 1
        elif width > height:
            center = (int(width / 2), int(height / 2))
            diff = int(height / 2)
            image = self.image[
                center[1] - diff : center[1] + diff, center[0] - diff : center[0] + diff
            ]
            self.mag_rate_x = 2 * diff / width
            self.mag_rate_y = 2 * diff / height
        else:
            center = (int(width / 2), int(height / 2))
            diff = int(width / 2)
            image = self.image[
                center[1] - diff : center[1] + diff, center[0] - diff : center[0] + diff
            ]
            self.mag_rate_x = 2 * diff / width
            self.mag_rate_y = 2 * diff / height
        return image

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        """
        for i in range(len(vals)):
            if vals[i] == self.params[0]:
                self.on = bool(vals[i + 1])
        """
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Odd:
    name = "Oddize"
    image = None
    params = []
    cal = None
    params_type = []
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        pass

    def getval(self, p_name):
        return

    def run(self):
        height, width = self.image.shape[:2]
        if width % 2 == 0:
            width = int(self.image.shape[1] + 1)
        if height % 2 == 0:
            height = int(self.image.shape[0] + 1)
        image_odd = cv2.resize(self.image, dsize=(width, height))
        return image_odd

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Average:
    name = "Ave._sub."
    image = None
    params = []
    params_type = []
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        pass

    def getval(self, p_name):
        return

    def run(self):
        for rows in range(len(self.image)):
            average = np.average(self.image[rows])
            self.image[rows] = self.image[rows] - average
        image_sub = self.image + np.min(self.image)
        return image_sub

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Mirror:
    name = "Mirror"
    params = []
    params_type = []
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        pass

    def getval(self, p_name):
        pass

    def run(self):
        m_image = cv2.flip(self.image, 1)
        return m_image

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False


class Ignore_neg:
    name = "Ignore_neg."
    on = None
    params = []
    params_type = []
    cal = None
    switch = True
    prev_mag_x = 1
    prev_mag_y = 1
    mag_rate_x = 1
    mag_rate_y = 1

    def mag_update(self):
        return [self.prev_mag_x * self.mag_rate_x, self.prev_mag_y * self.mag_rate_y]

    def rewrite(self, params):
        pass

    def getval(self, p_name):
        return

    def run(self):
        image_mod = np.where(self.image < 0, 0, self.image)
        return image_mod

    def rec(self):
        txt = self.name + "\t"
        for param in self.params:
            txt += param + "\t" + str(self.getval(param)) + "\t"
        txt += str(self.switch)
        return txt

    def read(self, vals):
        if vals[-1] == "True":
            self.switch = True
        elif vals[-1] == "False":
            self.switch = False
