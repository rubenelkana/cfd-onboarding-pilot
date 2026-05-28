"""Plot T and species mass-fraction profiles across a counter-flow flame.

Reads sampleDict raw output where multiple scalar fields share one .xy file
with header `# x T CH4 O2 N2 CO2 H2O`.

Usage:
    python scripts/plot_flame.py \\
        --case tutorials/counterFlowFlame2D \\
        --time 0.1 \\
        --out figures/03_flame_axis.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--case", type=Path, required=True)
    p.add_argument("--time", required=True, help="time directory name, e.g. 0.1")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    path = args.case / "postProcessing" / "sampleDict" / args.time / "axis.xy"
    data = np.loadtxt(path, comments="#")
    # Columns: x T CH4 O2 N2 CO2 H2O
    x_mm = data[:, 0] * 1000  # to mm
    T = data[:, 1]
    CH4 = data[:, 2]
    O2 = data[:, 3]
    N2 = data[:, 4]
    CO2 = data[:, 5]
    H2O = data[:, 6]

    fig, (ax_T, ax_Y) = plt.subplots(1, 2, figsize=(12, 4.5))

    # Temperature
    ax_T.plot(x_mm, T, color="#c0392b", lw=2)
    ax_T.set_xlabel("$x$ (mm)")
    ax_T.set_ylabel("$T$ (K)")
    ax_T.set_title(f"Temperature, $t = {args.time}$ s")
    ax_T.grid(alpha=0.3)
    ax_T.axhline(293, color="gray", lw=0.5, ls="--", label="inlet $T = 293$ K")
    ax_T.legend(loc="best")

    # Species
    ax_Y.plot(x_mm, CH4, color="#2980b9", lw=2, label="$Y_{CH_4}$ (fuel)")
    ax_Y.plot(x_mm, O2, color="#27ae60", lw=2, label="$Y_{O_2}$ (oxidiser)")
    ax_Y.plot(x_mm, N2, color="#7f8c8d", lw=2, ls="--", label="$Y_{N_2}$ (inert)")
    ax_Y.plot(x_mm, CO2, color="#e67e22", lw=2, label="$Y_{CO_2}$ (product)")
    ax_Y.plot(x_mm, H2O, color="#9b59b6", lw=2, label="$Y_{H_2O}$ (product)")
    ax_Y.set_xlabel("$x$ (mm)")
    ax_Y.set_ylabel("mass fraction")
    ax_Y.set_title(f"Species mass fractions, $t = {args.time}$ s")
    ax_Y.grid(alpha=0.3)
    ax_Y.legend(loc="center right", fontsize=9)

    fig.suptitle(
        "Counter-flow flame axis profile — fuel ($CH_4$) inlet at $x=0$, "
        "air inlet at $x=20$ mm  (100×40 mesh, OpenFOAM 11 multicomponentFluid)",
        fontsize=10,
    )
    fig.tight_layout()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=150, bbox_inches="tight")
    print(f"wrote {args.out}")

    # Sanity
    peak_T_idx = T.argmax()
    print(f"peak T on axis: {T[peak_T_idx]:.0f} K at x = {x_mm[peak_T_idx]:.2f} mm")
    print(f"max CO2 mass fraction: {CO2.max():.4f}  (chemistry active if > 0.01)")


if __name__ == "__main__":
    main()
