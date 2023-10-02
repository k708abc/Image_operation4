#!python3.11
from scipy import ndimage


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
