import cv2
import numpy as np
from config import CFG


def unsharp(img):
    a = CFG["us_amount"]
    blur = cv2.GaussianBlur(img, (0, 0), CFG["us_sigma"])
    return cv2.addWeighted(img, 1 + a, blur, -a, 0)


def laplacian(img):
    f = img.astype(np.float32)
    lap = cv2.Laplacian(f, cv2.CV_32F, ksize=3)
    return np.clip(f - CFG["lap_amount"] * lap, 0, 255).astype(np.uint8)
