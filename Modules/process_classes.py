#!python3.11

class Smothing:
    name = "Smoothing"
    image = None
    range = None
    params = ["range"]
    cal = None

    def rewrite(self, params):
        self.range = params[0]

    def getval(self, p_name):
        if p_name == "range":
            return self.range

    def run_pro(self):
        image_mod = ndimage.gaussian_filter(self.image, float(self.range))
        """
        image_mod = cv2.GaussianBlur(
            self.image, (int(self.range), int(self.range)), float(self.range)
        )
        """
        return image_mod

    def rec(self):
        return "Smoothing:" + "\n\t" "Range: " + "\t" + str(self.range) + "\n"