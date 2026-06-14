"""Plot trends across the inlet-velocity sweep of the counter-flow flame.

Reads the aggregated CSV produced by `aggregate_sweep.py` and produces a
four-panel figure: peak temperature, flame position, reaction-zone width
(FWHM), and product mass fractions, all vs the inlet jet velocity.

Usage:
    python scripts/plot_sweep_trends.py \\
        --csv tutorials/sweep_velocity/results.csv \\
        --out figures/04_sweep_trends.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    df = pd.read_csv(args.csv)
    df = df.sort_values("U_jet").reset_index(drop=True)

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    (ax_T, ax_x), (ax_w, ax_Y) = axes

    style = dict(marker="o", lw=2, ms=7)

    ax_T.plot(df["U_jet"], df["peak_T"], color="#c0392b", **style)
    ax_T.set_xlabel("$U_{jet}$ (m/s)")
    ax_T.set_ylabel("peak $T$ (K)")
    ax_T.set_title("Peak temperature on the axis")
    ax_T.grid(alpha=0.3)

    ax_x.plot(df["U_jet"], df["x_flame"], color="#2980b9", **style)
    ax_x.axhline(10, color="gray", lw=0.5, ls="--", label="geometric midpoint (10 mm)")
    ax_x.set_xlabel("$U_{jet}$ (m/s)")
    ax_x.set_ylabel("$x$ of peak $T$ (mm)")
    ax_x.set_title("Flame-sheet position")
    ax_x.grid(alpha=0.3)
    ax_x.legend(loc="best")

    ax_w.plot(df["U_jet"], df["fwhm_T"], color="#8e44ad", **style)
    ax_w.set_xlabel("$U_{jet}$ (m/s)")
    ax_w.set_ylabel("FWHM of $T$ profile (mm)")
    ax_w.set_title("Reaction-zone width (T-FWHM)")
    ax_w.grid(alpha=0.3)

    ax_Y.plot(df["U_jet"], df["peak_CO2"], color="#e67e22", label="$Y_{CO_2,max}$", **style)
    ax_Y.plot(df["U_jet"], df["peak_H2O"], color="#9b59b6", label="$Y_{H_2O,max}$", **style)
    ax_Y.set_xlabel("$U_{jet}$ (m/s)")
    ax_Y.set_ylabel("max product mass fraction")
    ax_Y.set_title("Peak combustion products on the axis")
    ax_Y.grid(alpha=0.3)
    ax_Y.legend()

    fig.suptitle(
        "Counter-flow CH$_4$/air flame — symmetric-jet velocity sweep "
        f"({len(df)} runs, OpenFOAM 11 multicomponentFluid)",
        fontsize=11,
    )
    fig.tight_layout()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=150, bbox_inches="tight")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
