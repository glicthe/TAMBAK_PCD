"""
Tahap 5: controlled noise experiment (PSNR and SSIM only, no counting).

Usage (from the Preprocessing folder):
  python noise_experiment.py ../clean_tiles --dst ../noise_experiment

Input : folder with copies of your cleanest tiles (PNG).
Output: <dst>/images/<noise>/<filter>/<tile>.png   (noisy and denoised images)
        <dst>/results_per_tile.csv
        <dst>/results_summary.csv                  (mean over tiles)
"""
import argparse
import csv
from pathlib import Path

import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

from denoise import median, gaussian, bilateral

GAUSS_SIGMA = 15     # std dev of Gaussian noise
SP_AMOUNT = 0.02     # fraction of pixels hit by salt-and-pepper
SEED = 0

FILTERS = {"none": lambda x: x, "median": median, "gaussian": gaussian, "bilateral": bilateral}


def add_gaussian(img, rng):
    noise = rng.normal(0, GAUSS_SIGMA, img.shape)
    return np.clip(img.astype(np.float64) + noise, 0, 255).astype(np.uint8)


def add_salt_pepper(img, rng):
    out = img.copy()
    r = rng.random(img.shape[:2])
    out[r < SP_AMOUNT / 2] = 0
    out[(r >= SP_AMOUNT / 2) & (r < SP_AMOUNT)] = 255
    return out


NOISES = {"gaussian_noise": add_gaussian, "saltpepper_noise": add_salt_pepper}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("--dst", required=True)
    a = p.parse_args()

    dst = Path(a.dst)
    files = sorted(Path(a.src).glob("*.png"))
    if not files:
        raise SystemExit(f"No PNG files in {a.src}")

    rows = []
    for i, f in enumerate(files):
        clean = cv2.imread(str(f), cv2.IMREAD_COLOR)
        for n_name, n_fn in NOISES.items():
            rng = np.random.default_rng(SEED + i)   # same noise for every filter on this tile
            noisy = n_fn(clean, rng)
            for fl_name, fl in FILTERS.items():
                res = fl(noisy)
                out_dir = dst / "images" / n_name / fl_name
                out_dir.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(out_dir / f.name), res)
                rows.append({
                    "tile": f.name, "noise": n_name, "filter": fl_name,
                    "psnr": psnr(clean, res, data_range=255),
                    "ssim": ssim(clean, res, channel_axis=2, data_range=255),
                })

    dst.mkdir(parents=True, exist_ok=True)
    with open(dst / "results_per_tile.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    summary = []
    for n_name in NOISES:
        for fl_name in FILTERS:
            sel = [r for r in rows if r["noise"] == n_name and r["filter"] == fl_name]
            summary.append({
                "noise": n_name, "filter": fl_name, "n_tiles": len(sel),
                "psnr_mean": round(float(np.mean([r["psnr"] for r in sel])), 3),
                "ssim_mean": round(float(np.mean([r["ssim"] for r in sel])), 4),
            })
    with open(dst / "results_summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=summary[0].keys())
        w.writeheader()
        w.writerows(summary)

    for s in summary:
        print(f'{s["noise"]:18} {s["filter"]:10} PSNR {s["psnr_mean"]:7.3f}  SSIM {s["ssim_mean"]:.4f}')


if __name__ == "__main__":
    main()