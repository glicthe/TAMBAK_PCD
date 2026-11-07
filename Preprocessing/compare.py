"""
Side-by-side check of one tile across flows.
Usage (from Preprocessing folder):
  python compare.py ../out galis_03052020_03.png --flows ABCD
  python compare.py ../out galis_03052020_03.png --crop 100 100 128   # x y size, zoomed 3x
Writes compare_<tile>.png next to the script.
"""
import argparse
from pathlib import Path

import cv2
import numpy as np

p = argparse.ArgumentParser()
p.add_argument("out")
p.add_argument("tile")
p.add_argument("--flows", default="ABCD")
p.add_argument("--crop", nargs=3, type=int, metavar=("X", "Y", "SIZE"))
a = p.parse_args()

panels = []
for k in a.flows:
    img = cv2.imread(str(Path(a.out) / k / f"{k}_{a.tile}"))
    if img is None:
        raise SystemExit(f"missing: {k}/{k}_{a.tile}")
    if a.crop:
        x, y, s = a.crop
        img = cv2.resize(img[y:y + s, x:x + s], None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
    cv2.putText(img, k, (8, 28), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    panels.append(img)

cv2.imwrite(f"compare_{a.tile}", np.hstack(panels))
print(f"saved compare_{a.tile}")