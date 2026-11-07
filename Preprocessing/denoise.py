import cv2
from config import CFG


def median(img):
    return cv2.medianBlur(img, CFG["median_k"])


def gaussian(img):
    k = CFG["gauss_k"]
    return cv2.GaussianBlur(img, (k, k), CFG["gauss_sigma"])


def bilateral(img):
    return cv2.bilateralFilter(
        img, CFG["bil_d"], CFG["bil_sigma_color"], CFG["bil_sigma_space"]
    )
