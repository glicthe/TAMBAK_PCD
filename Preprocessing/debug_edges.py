"""
Look at what each edge method sees on ONE tile. Use TUNING tiles only.
  python debug_edges.py ../out/A/A_pademawu_03052020_01.png --params counting_params_pademawu.json
  python debug_edges.py ../out/A/A_pademawu_22082022_03.png --params counting_params_pademawu.json

Panels (left to right): grayscale | Canny with your locked params | Kirsch + Otsu, dilated | adaptive threshold.
The printed percentages are the share of white pixels in each binary panel.
Near 0% for Canny means the edge detector found almost no pematang, so the inverted map becomes
one huge region and the counter returns 0.
Writes debug_<filename> next to the script.
"""
import argparse
import json
from pathlib import Path

import cv2
import numpy as np


def kirsch(gray):
    ring = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]
    base = [5, 5, 5, -3, -3, -3, -3, -3]
    g = gray.astype(np.float32)
    best = np.zeros_like(g)
    for i in range(8):
        k = np.zeros((3, 3), np.float32)
        for (r, c), v in zip(ring, base[-i:] + base[:-i] if i else base):
            k[r, c] = v
        best = np.maximum(best, cv2.filter2D(g, cv2.CV_32F, k))
    best = best / max(float(np.percentile(best, 99.5)), 1e-6)   # normalise per tile
    return np.clip(best * 255, 0, 255).astype(np.uint8)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("--params", default=None)
    a = p.parse_args()

    img = cv2.imread(a.image, cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"cannot read {a.image}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    lo, hi = 50, 150
    scale, speck, dil, klabel = 1.0, 0, 3, "kirsch+otsu"
    if a.params:
        prm = json.loads(Path(a.params).read_text())
        lo, hi = prm.get("canny_low", lo), prm.get("canny_high", hi)
        if prm.get("method") == "kirsch":          # show exactly what the locked counter sees
            scale, speck, dil = prm["thr_scale"], prm["speck_area"], prm["dilate_k"]
            klabel = f"kirsch locked x{scale}"
    canny = cv2.Canny(gray, lo, hi)

    kmag = kirsch(gray)
    t, _ = cv2.threshold(kmag, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kbin = ((kmag > t * scale) * 255).astype(np.uint8)
    if speck > 0:
        n0, lab0, st0, _ = cv2.connectedComponentsWithStats(kbin, connectivity=8)
        kbin[np.isin(lab0, [i for i in range(1, n0) if st0[i, cv2.CC_STAT_AREA] < speck])] = 0
    if dil > 1:
        kbin = cv2.dilate(kbin, np.ones((dil, dil), np.uint8))

    adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY_INV, 31, 5)

    print(f"mean gray {gray.mean():.1f}, std {gray.std():.1f}")
    for name, m in (("canny", canny), (klabel, kbin), ("adaptive", adapt)):
        print(f"{name:12} white pixels: {100 * (m > 0).mean():.2f}%")

    panels = []
    for name, m in (("gray", gray), (f"canny {lo}/{hi}", canny), (klabel, kbin), ("adaptive", adapt)):
        pm = cv2.cvtColor(m, cv2.COLOR_GRAY2BGR)
        cv2.putText(pm, name, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        panels.append(pm)
    out = f"debug_{Path(a.image).name}"
    cv2.imwrite(out, np.hstack(panels))
    print(f"saved {out}")


if __name__ == "__main__":
    main()