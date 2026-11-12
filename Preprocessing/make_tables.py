"""
Merge the results folders of one experiment into one table per group (Tahap 8).

A group = one location + one denoise filter + one counter. Give it every results folder that
belongs to it (for example the ABCD folder and the EF folder). Never mix counters or filters.

Usage (from the Preprocessing folder):
  python make_tables.py --out ../tables ^
    --group pademawu_median ../results_pademawu_v2_kirsch_median ../results_pademawu_v2_kirsch_median_EF ^
    --group pademawu_bilateral ../results_pademawu_v2_kirsch_bilateral ../results_pademawu_v2_kirsch_bilateral_EF

(Use \\ instead of ^ in bash. Or put everything on one line.)

Writes <out>/<group>.csv and <out>/overview.csv, and prints them.
bias = mean(predicted - truth): negative means the flow undercounts, positive means it overcounts.
"""
import argparse
import csv
from pathlib import Path


def read(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def date_key(d):          # DDMMYYYY -> YYYYMMDD for chronological order
    return d[4:] + d[2:4] + d[:2]


def build_group(name, folders):
    summ, tiles = {}, {}
    for f in folders:
        f = Path(f)
        for r in read(f / "summary.csv"):
            key = (r["flow"], r["group_type"], r["group"])
            if key in summ:
                raise SystemExit(f"[{name}] duplicate row {key} (flow computed twice in this group)")
            summ[key] = r
        for r in read(f / "counts_per_tile.csv"):
            tiles.setdefault(r["flow"], []).append(r)

    flows = sorted({k[0] for k in summ})
    dates = sorted({k[2] for k in summ if k[1] == "date"}, key=date_key)
    ns = {fl: int(summ[(fl, "all", "all")]["n"]) for fl in flows}
    if len(set(ns.values())) > 1:
        print(f"WARNING [{name}]: different tile counts per flow: {ns}")

    rows = []
    for fl in flows:
        a = summ[(fl, "all", "all")]
        t = tiles[fl]
        bias = sum(int(x["pred"]) - int(x["truth"]) for x in t) / len(t)
        row = {"flow": fl, "n": a["n"], "MAE": a["mae"], "MAPE": a["mape"], "bias": round(bias, 2)}
        for d in dates:
            s = summ.get((fl, "date", d))
            row[f"MAE_{d}"] = s["mae"] if s else ""
            row[f"MAPE_{d}"] = s["mape"] if s else ""
        rows.append(row)
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--group", nargs="+", action="append", metavar=("NAME", "FOLDER"), required=True)
    a = p.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    groups = {}
    for g in a.group:
        name, folders = g[0], g[1:]
        rows = build_group(name, folders)
        groups[name] = rows
        with open(out / f"{name}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        print(f"\n== {name} ==")
        print(",".join(rows[0].keys()))
        for r in rows:
            print(",".join(str(v) for v in r.values()))

    flows = sorted({r["flow"] for rows in groups.values() for r in rows})
    with open(out / "overview.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["flow"] + list(groups))
        for fl in flows:
            line = [fl]
            for rows in groups.values():
                m = next((r for r in rows if r["flow"] == fl), None)
                line.append(f'{m["MAE"]} ({m["MAPE"]}%)' if m else "")
            w.writerow(line)
    print(f"\nWrote {out}/overview.csv (cells are MAE (MAPE%))")


if __name__ == "__main__":
    main()