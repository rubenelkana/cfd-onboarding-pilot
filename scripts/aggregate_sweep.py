"""Aggregate a parameter sweep over inlet jet velocity into one CSV.

Reads each case's `postProcessing/sampleDict/0.1/axis.xy`, extracts per-case
scalar metrics, and writes a tidy CSV with one row per case.

Metrics extracted:
    U_jet         (m/s) input parameter
    peak_T        (K)   maximum temperature on the axis
    x_flame       (mm)  x-position where peak_T occurs
    peak_CO2      (mass fraction) max along axis
    peak_H2O      (mass fraction) max along axis
    fwhm_T        (mm)  full-width half-max of the temperature profile
                       (above (peak_T + inlet_T)/2)

Usage:
    python scripts/aggregate_sweep.py \\
        --root tutorials/sweep_velocity \\
        --time 0.1 \\
        --out tutorials/sweep_velocity/results.csv
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import numpy as np


def case_metrics(axis_xy: Path) -> dict[str, float]:
    data = np.loadtxt(axis_xy, comments="#")
    # Columns: x, T, CH4, O2, N2, CO2, H2O
    x_mm = data[:, 0] * 1000.0
    T = data[:, 1]
    CO2 = data[:, 5]
    H2O = data[:, 6]

    peak_idx = int(T.argmax())
    peak_T = float(T[peak_idx])
    x_flame = float(x_mm[peak_idx])
    inlet_T = 293.0
    half = (peak_T + inlet_T) / 2.0
    in_hot = T > half
    if in_hot.any():
        fwhm = float(x_mm[in_hot].max() - x_mm[in_hot].min())
    else:
        fwhm = 0.0
    return {
        "peak_T": peak_T,
        "x_flame": x_flame,
        "peak_CO2": float(CO2.max()),
        "peak_H2O": float(H2O.max()),
        "fwhm_T": fwhm,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--time", required=True, help="time dir name, e.g. 0.1")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    case_dir_re = re.compile(r"^U_(?P<u>\d*\.?\d+)$")
    rows = []
    for case_dir in sorted(args.root.iterdir()):
        if not case_dir.is_dir():
            continue
        m = case_dir_re.match(case_dir.name)
        if m is None:
            continue
        u = float(m.group("u"))
        axis_xy = case_dir / "postProcessing" / "sampleDict" / args.time / "axis.xy"
        if not axis_xy.exists():
            print(f"WARN: missing {axis_xy}; skipping")
            continue
        metrics = case_metrics(axis_xy)
        metrics["U_jet"] = u
        rows.append(metrics)

    rows.sort(key=lambda r: r["U_jet"])
    cols = ["U_jet", "peak_T", "x_flame", "fwhm_T", "peak_CO2", "peak_H2O"]
    with args.out.open("w") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in cols})
    print(f"wrote {args.out} with {len(rows)} rows")
    for r in rows:
        print(
            f"  U={r['U_jet']:.2f}  peak_T={r['peak_T']:.0f}  "
            f"x_flame={r['x_flame']:.2f}  fwhm={r['fwhm_T']:.2f}  "
            f"CO2={r['peak_CO2']:.3f}  H2O={r['peak_H2O']:.3f}"
        )


if __name__ == "__main__":
    main()
