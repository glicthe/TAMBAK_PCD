import cv2
from config import CFG


def _on_lightness(img, fn):
    """Apply fn to the L channel of LAB so colour is left untouched."""
    l, a, b = cv2.split(cv2.cvtColor(img, cv2.COLOR_BGR2LAB))
    return cv2.cvtColor(cv2.merge((fn(l), a, b)), cv2.COLOR_LAB2BGR)


def hist_eq(img):
    return _on_lightness(img, cv2.equalizeHist)


def clahe(img):
    c = cv2.createCLAHE(clipLimit=CFG["clip"], tileGridSize=(CFG["tile"], CFG["tile"]))
    return _on_lightness(img, c.apply)
