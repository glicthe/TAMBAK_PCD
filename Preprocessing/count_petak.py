"""
Tahap 6 and 7: petak counting, parameter tuning, and the main experiment.

Ground truth CSV: either columns tile,final,split or your log format
(Nama file, Jumlah tile (hitung manual), split). split is 'tuning' or 'test'.

Method 2 (Kirsch): add --method kirsch to tune. Its parameters go to counting_params[_location]_kirsch.json.
run needs no method flag, it reads the method from the parameter file you pass with --params.

Optional: add --location galis (or pademawu) to tune and run each location separately,
with its own counting_params_<location>.json. Report that choice in the methods.

Step 1, tune on TUNING tiles with flow A only (writes counting_params.json):
  python count_petak.py tune --out ../out --truth ../ground_truth.csv

Step 2, run all flows on TEST tiles with the locked parameters:
  python count_petak.py run --out ../out --truth ../ground_truth.csv --flows ABCD --results ../results

run refuses to start if counting_params.json does not exist, and it only touches test tiles.
Use --out ../out_bilateral to evaluate the bilateral set. Never mix both sets in one results folder.
"""
import argparse
import csv
import itertools
import json
from pathlib import Path

import cv2
import numpy as np

PARAMS_FILE = "counting_params.json"

GRID = {
    "canny_low": [30, 50, 80],
    "canny_high": [100, 150, 200],
    "close_k": [3, 5, 7],
    "min_area": [20, 50, 100, 200, 500],
}
FIXED = {"method": "canny", "open_k": 3, "max_area": 100000, "channel": "gray"}   # channel: gray, b, g or r

# Method 2: Kirsch edge magnitude, normalised per tile, Otsu threshold, speck removal, dilation.
GRID_KIRSCH = {
    "thr_scale": [0.8, 1.0, 1.2],     # multiplier on the Otsu threshold
    "speck_area": [0, 10, 30],        # drop white components smaller than this (pixels)
    "dilate_k": [1, 3],               # 1 = no dilation; 3 thickens the edge mask
    "min_area": [20, 50, 100, 200, 500],
}
FIXED_KIRSCH = {"method": "kirsch", "open_k": 3, "max_area": 100000, "channel": "gray"}


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
    best = best / max(float(np.percentile(best, 99.5)), 1e-6)    # normalise per tile
    return np.clip(best * 255, 0, 255).astype(np.uint8)


def count_petak(img, p, vis=False):
    if p["channel"] == "gray":
        ch = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        ch = img[:, :, {"b": 0, "g": 1, "r": 2}[p["channel"]]]

    if p.get("method", "canny") == "kirsch":
        kmag = kirsch(ch)
        t, _ = cv2.threshold(kmag, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        edges = ((kmag > t * p["thr_scale"]) * 255).astype(np.uint8)
        if p["speck_area"] > 0:                                    # remove isolated specks, keep the pematang network
            n0, lab0, st0, _ = cv2.connectedComponentsWithStats(edges, connectivity=8)
            small = [i for i in range(1, n0) if st0[i, cv2.CC_STAT_AREA] < p["speck_area"]]
            edges[np.isin(lab0, small)] = 0
        if p["dilate_k"] > 1:
            edges = cv2.dilate(edges, np.ones((p["dilate_k"], p["dilate_k"]), np.uint8))
    else:
        edges = cv2.Canny(ch, p["canny_low"], p["canny_high"])
        kc = cv2.getStructuringElement(cv2.MORPH_RECT, (p["close_k"], p["close_k"]))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kc)      # seal gaps in pematang

    regions = cv2.bitwise_not(edges)                               # petak become objects
    ko = cv2.getStructuringElement(cv2.MORPH_RECT, (p["open_k"], p["open_k"]))
    regions = cv2.morphologyEx(regions, cv2.MORPH_OPEN, ko)        # drop small specks

    n, labels, stats, _ = cv2.connectedComponentsWithStats(regions, connectivity=4)
    keep = [i for i in range(1, n)
            if p["min_area"] <= stats[i, cv2.CC_STAT_AREA] <= p["max_area"]]
    if not vis:
        return len(keep)

    out = img.copy()
    mask = np.isin(labels, keep).astype(np.uint8)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(out, cnts, -1, (0, 0, 255), 1)
    cv2.putText(out, str(len(keep)), (8, 28), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return len(keep), out


def load_truth(path, split, location=None):
    """Accepts columns tile/final/split or the log format: 'Nama file', 'Jumlah ...', 'split'."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = {c.strip().lower(): c for c in reader.fieldnames}
        tcol = cols.get("tile") or cols.get("nama file")
        ccol = cols.get("final") or next((c for k, c in cols.items() if k.startswith("jumlah")), None)
        scol = cols.get("split")
        if not (tcol and ccol and scol):
            raise SystemExit(f"Need tile, count and split columns. Found: {reader.fieldnames}")
        rows = [r for r in reader if (r[scol] or "").strip().lower() == split]
    if location:
        rows = [r for r in rows if r[tcol].strip().lower().startswith(location.lower() + "_")]
    if not rows:
        raise SystemExit(f"No '{split}' rows" + (f" for {location}" if location else "") + f" in {path}")
    return {r[tcol].strip(): int(r[ccol]) for r in rows}


def read_flow(out, flow, tile):
    path = Path(out) / flow / f"{flow}_{tile}"
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"Missing image: {path}")
    return img


def tune(a):
    truth = load_truth(a.truth, "tuning", a.location)
    imgs = {t: read_flow(a.out, "A", t) for t in truth}
    grid, fixed = (GRID_KIRSCH, FIXED_KIRSCH) if a.method == "kirsch" else (GRID, FIXED)
    keys = list(grid)
    results = []
    for combo in itertools.product(*(grid[k] for k in keys)):
        p = {**fixed, **dict(zip(keys, combo))}
        if p["method"] == "canny" and p["canny_low"] >= p["canny_high"]:
            continue
        errs = [abs(count_petak(imgs[t], p) - truth[t]) for t in truth]
        results.append((float(np.mean(errs)), p))
    results.sort(key=lambda x: x[0])

    print(f"Tuning on {len(truth)} tiles, flow A only. Top 5 by MAE:")
    for mae, p in results[:5]:
        print(f"  MAE {mae:6.2f}  {p}")
    best = results[0][1]
    Path(a.params).write_text(json.dumps(best, indent=2))
    print(f"Locked parameters written to {a.params}. Do not edit after this.")


def run(a):
    pf = Path(a.params)
    if not pf.exists():
        raise SystemExit(f"{a.params} not found. Run 'tune' first.")
    p = json.loads(pf.read_text())
    truth = load_truth(a.truth, "test", a.location)

    res_dir = Path(a.results)
    res_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for flow in a.flows:
        for tile, gt in truth.items():
            img = read_flow(a.out, flow, tile)
            if a.overlay:
                pred, ov = count_petak(img, p, vis=True)
                od = res_dir / "overlays" / flow
                od.mkdir(parents=True, exist_ok=True)
                cv2.imwrite(str(od / f"{flow}_{tile}"), ov)
            else:
                pred = count_petak(img, p)
            err = abs(pred - gt)
            rows.append({"tile": tile, "flow": flow, "pred": pred, "truth": gt,
                         "abs_err": err, "pct_err": round(100 * err / gt, 2) if gt else ""})

    with open(res_dir / "counts_per_tile.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    summary = []
    def add(gtype, gname, flow, sel):
        pct = [r["pct_err"] for r in sel if r["pct_err"] != ""]
        summary.append({"group_type": gtype, "group": gname, "flow": flow, "n": len(sel),
                        "mae": round(float(np.mean([r["abs_err"] for r in sel])), 3),
                        "mape": round(float(np.mean(pct)), 2) if pct else ""})
    for flow in a.flows:
        fr = [r for r in rows if r["flow"] == flow]
        add("all", "all", flow, fr)
        for loc in sorted({r["tile"].split("_")[0] for r in fr}):
            add("location", loc, flow, [r for r in fr if r["tile"].split("_")[0] == loc])
        for dt in sorted({r["tile"].split("_")[1] for r in fr}):
            add("date", dt, flow, [r for r in fr if r["tile"].split("_")[1] == dt])

    with open(res_dir / "summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=summary[0].keys())
        w.writeheader()
        w.writerows(summary)

    print(f"{len(truth)} test tiles. Overall:")
    for s in summary:
        if s["group_type"] == "all":
            print(f'  flow {s["flow"]}: MAE {s["mae"]:.3f}  MAPE {s["mape"]}%')


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("tune", tune), ("run", run)):
        s = sub.add_parser(name)
        s.add_argument("--out", required=True)
        s.add_argument("--truth", required=True)
        s.add_argument("--params", default=None)
        s.add_argument("--location", default=None, help="galis or pademawu; tune/run that location only")
        if name == "tune":
            s.add_argument("--method", default="canny", choices=["canny", "kirsch"])
        if name == "run":
            s.add_argument("--flows", default="ABCD")
            s.add_argument("--results", required=True)
            s.add_argument("--overlay", action="store_true")
        s.set_defaults(fn=fn)
    args = p.parse_args()
    if args.params is None:
        base = f"counting_params_{args.location}" if args.location else "counting_params"
        suffix = "_kirsch" if getattr(args, "method", "canny") == "kirsch" else ""
        args.params = base + suffix + ".json"
    args.fn(args)