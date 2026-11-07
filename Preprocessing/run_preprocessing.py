"""
Usage (from the Preprocessing folder):
  python run_preprocessing.py "../GALIS_UDAH_DIPOTONG" "../PADEMAWU_UDAH_DIPOTONG" --dst ../out --flows ABCD
  python run_preprocessing.py ... --dst ../out_bilateral --denoise bilateral

--denoise selects the filter used in flows B, C, D (median, gaussian, bilateral; default median).
Walks every source folder recursively and keeps only files named like
galis_03052020_03.png or pademawu_22082022_01.png (location_DDMMYYYY_NN.png).
Full scene images such as "3 mei 2020.png" do not match and are skipped.
Output: <dst>/<flow>/<flow>_<original filename>, e.g. out/A/A_galis_03052020_03.png.
"""
import argparse
import re
from pathlib import Path

import cv2

from flows import DENOISERS, make_flows

TILE = re.compile(r"^[a-z]+_\d{8}_\d{2}\.png$", re.IGNORECASE)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("src", nargs="+")
    p.add_argument("--dst", required=True)
    p.add_argument("--flows", default="ABCD")
    p.add_argument("--denoise", default="median", choices=list(DENOISERS))
    args = p.parse_args()

    dst = Path(args.dst).resolve()
    flows = make_flows(args.denoise)
    files = []
    for s in args.src:
        for f in sorted(Path(s).rglob("*.png")):
            if dst in f.resolve().parents:
                continue  # never read from the output folder
            if TILE.match(f.name):
                files.append(f)

    if not files:
        raise SystemExit("No tiles matched the naming pattern.")

    names = [f.name for f in files]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        raise SystemExit(f"Duplicate filenames: {sorted(dupes)}")

    for key in args.flows:
        (dst / key).mkdir(parents=True, exist_ok=True)

    for f in files:
        img = cv2.imread(str(f), cv2.IMREAD_COLOR)
        if img is None:
            print(f"skip (unreadable): {f}")
            continue
        if img.shape[:2] != (512, 512):
            print(f"warning: {f.name} is {img.shape[1]}x{img.shape[0]}, expected 512x512")
        for key in args.flows:
            cv2.imwrite(str(dst / key / f"{key}_{f.name}"), flows[key](img))

    (dst / "denoise.txt").write_text(f"denoise={args.denoise}\nflows={args.flows}\n")
    print(f"{len(files)} tiles x {len(args.flows)} flows done")


if __name__ == "__main__":
    main()