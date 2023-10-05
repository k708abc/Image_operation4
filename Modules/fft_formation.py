import numpy as np
from numpy import fft, minimum
from scipy import signal


def apply_window(target, window):
    target_copy = np.copy(target)
    if window == "Hann":
        wfunc = signal.hann(target.shape[0])
        wfunc2 = signal.hann(target.shape[1])
    elif window == "Hamming":
        wfunc = signal.hamming(target.shape[0])
        wfunc2 = signal.hamming(target.shape[1])
    elif window == "Blackman":
        wfunc = signal.blackman(target.shape[0])
        wfunc2 = signal.blackman(target.shape[1])
    else:
        wfunc = signal.boxcar(target.shape[0])
        wfunc2 = signal.boxcar(target.shape[1])
    for i in range(target.shape[0]):
        for k in range(target.shape[1]):
            target_copy[i][k] = target[i][k] * wfunc[i] * wfunc2[k]
    target_copy = subtraction(target_copy)
    return target_copy


def subtraction(image):
    minimum = image.min()
    image_mod = image - minimum
    return image_mod


def fft_processing(w_image):
    fimage_or = np.fft.fft2(w_image)
    fimage_or = np.fft.fftshift(fimage_or)
    # fimage_or = np.angle(fimage_or)
    fimage_or = np.abs(fimage_or)
    return fimage_or


def fft_scaling(image, method):
    if method == "Linear":
        fimage = image
    elif method == "Log":
        fimage = np.log(image, out=np.zeros_like(image), where=(image != 0))
    elif method == "Sqrt":
        fimage = np.sqrt(image)
    return fimage


def datatype_change(image):
    maximum = image.max()
    minimum = image.min()
    image_mod = (image - minimum) / (maximum - minimum) * 255
    return image_mod.astype(np.uint8)


def fft_process(target, method, window):
    image_mod = datatype_change(target)
    w_image = apply_window(image_mod, window)
    fft_image = fft_processing(w_image)
    fft_image = fft_scaling(fft_image, method)
    fft_image = fft_image.astype(np.float32)
    fft_image = cut_center(fft_image)
    return fft_image


def cut_center(image):
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
