#!python3.11
from scipy import ndimage
import numpy as np
import cv2


class ImOpen:
    name = "Im_open"
    image = None

    def run(self):
        return self.image


class Smoothing:
    name = "Smoothing"
    range = None
    params = ["range"]
    image = None
    switch = True

    def rewrite(self, params):
        self.range = params[0]

    def getval(self, p_name):
        if p_name == "range":
            return self.range

    def run(self):
        image_mod = ndimage.gaussian_filter(self.image, float(self.range))
        return image_mod

    def rec(self):
        return "Smoothing:" + "\n\t" "Range: " + "\t" + str(self.range) + "\n"

    def test(self):
        print(self.name)


class Median:
    name = "Median"
    range = None
    params = ["range"]
    image = None
    switch = True

    def rewrite(self, params):
        self.range = params[0]

    def getval(self, p_name):
        if p_name == "range":
            return self.range

    def run(self):
        image_mod = ndimage.median_filter(self.image, int(self.range))
        return image_mod

    def rec(self):
        return "Median:" + "\n\t" "Range: " + "\t" + str(self.range) + "\n"


class Drift:
    name = "Drift"
    image = None
    x = None
    y = None
    params = ["x", "y"]
    cal = None
    switch = True
    type = None

    def rewrite(self, params):
        self.x = params[0]
        self.y = params[1]

    def getval(self, p_name):
        if p_name == "x":
            return self.x
        if p_name == "y":
            return self.y

    def run(self):
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
        affine_img = cv2.warpAffine(self.image, mat, (2 * ps_x, 2 * ps_y))
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
        return im_crop

    def rec(self):
        return (
            "Drift:"
            + "\n\t"
            + "x: "
            + "\t"
            + str(self.x)
            + "\n\t"
            + "y: "
            + "\t"
            + str(self.y)
            + "\n"
        )


class Rescale:
    name = "Rescale"
    image = None
    all = None
    x = None
    y = None
    params = ["All", "X", "Y"]
    cal = None

    def rewrite(self, params):
        self.all = params[0]
        self.x = params[1]
        self.y = params[2]

    def getval(self, p_name):
        if p_name == "All":
            return self.all
        if p_name == "X":
            return self.x
        if p_name == "Y":
            return self.y

    def run(self):
        or_y, or_x = self.image.shape[:2]
        width_x = int(or_x * self.x * self.all)
        height_y = int(or_y * self.y * self.all)
        modified_image = cv2.resize(self.image, (width_x, height_y))
        return modified_image

    def rec(self):
        return (
            "Rescale:"
            + "\n\t"
            + "size_x: "
            + "\t"
            + str(int(self.x))
            + "\n\t"
            + "size_y: "
            + "\t"
            + str(int(self.y))
            + "\n"
        )


class Cut:
    name = "Cut"
    image = None
    ratio = None
    params = ["ratio"]
    cal = None

    def rewrite(self, params):
        self.ratio = params[0]

    def getval(self, p_name):
        if p_name == "ratio":
            return self.ratio

    def run(self):
        if self.ratio == 100:
            return self.image
        else:
            half_ratio = self.ratio / 200
            height, width = self.image.shape[:2]
            diff_h = int(height * half_ratio)
            diff_w = int(width * half_ratio)
            image_cropped = self.image[
                diff_h : height - diff_h, diff_w : width - diff_w
            ]
            return image_cropped

    def rec(self):
        return "Cut:" + "\n\t" + "ratio: " + "\t" + str(int(self.ratio)) + "\n"


class Intensity:
    name = "Intensity"
    image = None
    method = None
    params = ["method"]
    cal = None

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
        return "Intensity:" + "\n\t" + "method: " + "\t" + str(self.method) + "\n"


class Gamma:
    name = "Gamma"
    image = None
    val = None
    val = ["method"]
    cal = None

    def rewrite(self, params):
        self.val = params[0]

    def getval(self, p_name):
        if p_name == "val":
            return self.val

    def run(self):
        image_mod = self.image
        # あとで
        return image_mod

    def rec(self):
        return "Gamma:" + "\n\t" + "val: " + "\t" + str(self.val) + "\n"


class Edge:
    name = "Edge"
    image = None
    method = None
    const = None
    mul_or = None
    val = ["method", "const.", "mul. original"]
    cal = None

    def rewrite(self, params):
        self.method = params[0]
        self.const = params[1]
        self.mul_or = params[2]

    def getval(self, p_name):
        if p_name == "method":
            return self.method
        elif p_name == "const.":
            return self.val
        elif p_name == "mul. original":
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

        if (self.mul_or == True) or (self.mul_or == "True"):
            image_mul = self.pos_offset(self.image, 1)
            image_mod = image_mod * image_mul
        return image_mod

    def rec(self):
        return (
            "Edge detection:"
            + "\n\t"
            + "method: "
            + "\t"
            + str(self.method)
            + "\n\t"
            + "constant: "
            + "\t"
            + str(self.val)
            + "\n\t"
            + "multiple original: "
            + "\t"
            + str(self.mul_or)
        )


class Square:
    name = "Squarize"
    on = None
    val = ["on/off"]
    cal = None

    def rewrite(self, params):
        self.on = params[0]

    def getval(self, p_name):
        if p_name == "on/off":
            return self.on

    def run(self):
        height, width = self.image.shape[:, 2]
        if height == width:
            pass
        elif width > height:
            center = (int(width / 2), int(height / 2))
            diff = int(width / 2)
            image = image[
                center[1] - diff : center[1] + diff, center[0] - diff : center[0] + diff
            ]
        else:
            center = (int(width / 2), int(height / 2))
            diff = int(height / 2)
            image = image[
                center[1] - diff : center[1] + diff, center[0] - diff : center[0] + diff
            ]
        return image

    def rec(self):
        return "Squareize:" + "\n\t" + "on/off: " + "\t" + str(self.on) + "\n"


class Odd:
    name = "Oddize"
    on = None
    val = ["on/off"]
    cal = None

    def rewrite(self, params):
        self.on = params[0]

    def getval(self, p_name):
        if p_name == "on/off":
            return self.on

    def run(self):
        height, width = self.image.shape[:, 2]
        if width % 2 == 0:
            width = int(self.image.shape[1] + 1)
        if height % 2 == 0:
            height = int(self.image.shape[0] + 1)
        image_odd = cv2.resize(self.image, dsize=(width, height))
        return image_odd

    def rec(self):
        return "Oddize:" + "\n\t" + "on/off: " + "\t" + str(self.on) + "\n"


class Average:
    name = "Ave. sub."
    on = None
    val = ["on/off"]
    cal = None

    def rewrite(self, params):
        self.on = params[0]

    def getval(self, p_name):
        if p_name == "on/off":
            return self.on

    def run(self):
        for rows in range(len(self.image)):
            average = np.average(self.image[rows])
            self.image[rows] = self.image[rows] - average
        image_sub = self.image + np.min(self.image)
        return image_sub

    def rec(self):
        return "Average subtraction:" + "\n\t" + "on/off: " + "\t" + str(self.on) + "\n"


class Mirror:
    name = "mirror"
    on = None
    val = ["on/off"]
    cal = None

    def rewrite(self, params):
        self.on = params[0]

    def getval(self, p_name):
        if p_name == "on/off":
            return self.on

    def run(self):
        m_image = cv2.flip(self.image, 1)
        return m_image

    def rec(self):
        return "Mirror:" + "\n\t" + "on/off: " + "\t" + str(self.on) + "\n"


class Ignore_neg:
    name = "ignore neg."
    on = None
    val = ["on/off"]
    cal = None

    def rewrite(self, params):
        self.on = params[0]

    def getval(self, p_name):
        if p_name == "on/off":
            return self.on

    def run(self):
        image_mod = np.where(self.image < 0, 0, self.image)
        return image_mod

    def rec(self):
        return "Ignore negative:" + "\n\t" + "on/off: " + "\t" + str(self.on) + "\n"
