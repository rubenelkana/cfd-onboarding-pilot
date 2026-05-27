"""Plot lid-driven cavity velocity profiles along the two centrelines.

Reads sampleDict output (raw .xy files with header `# y U_x U_y U_z`) and
produces a two-panel figure suitable for the README of Phase 2.

Usage:
    python scripts/plot_cavity.py \\
        --vertical tutorials/cavity/postProcessing/sampleDict/10/verticalCentreline.xy \\
        --horizontal tutorials/cavity/postProcessing/sampleDict/10/horizontalCentreline.xy \\
        --out figures/02_cavity_centrelines.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def load_xy(path: Path) -> np.ndarray:
    return np.loadtxt(path, comments="#")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--vertical", type=Path, required=True)
    p.add_argument("--horizontal", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    v = load_xy(args.vertical)
    h = load_xy(args.horizontal)

    fig, (ax_v, ax_h) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Vertical centreline (x=0.05): plot U_x vs y.
    ax_v.plot(v[:, 1], v[:, 0], "o-", color="#c0392b", lw=2, ms=5, label="$U_x$")
    ax_v.axvline(0, color="gray", lw=0.6, ls="--")
    ax_v.set_xlabel("$U_x$ (m/s)")
    ax_v.set_ylabel("$y$ (m)")
    ax_v.set_title("Vertical centreline at $x = 0.05$ m")
    ax_v.grid(alpha=0.3)
    ax_v.legend()

    # Horizontal centreline (y=0.05): plot U_y vs x.
    ax_h.plot(h[:, 0], h[:, 2], "s-", color="#2980b9", lw=2, ms=5, label="$U_y$")
    ax_h.axhline(0, color="gray", lw=0.6, ls="--")
    ax_h.set_xlabel("$x$ (m)")
    ax_h.set_ylabel("$U_y$ (m/s)")
    ax_h.set_title("Horizontal centreline at $y = 0.05$ m")
    ax_h.grid(alpha=0.3)
    ax_h.legend()

    fig.suptitle(
        "Lid-driven cavity — centreline velocity at $t=10$ s "
        "(20×20 mesh, OpenFOAM 11 incompressibleFluid)",
        fontsize=11,
    )
    fig.tight_layout()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=150, bbox_inches="tight")
    print(f"wrote {args.out}")

    # Quick numerical sanity check: peak |U_x| on vertical centreline near top
    near_top = v[v[:, 0] > 0.085]
    print(
        f"peak |U_x| in upper 15% of cavity: {np.abs(near_top[:, 1]).max():.3f} m/s "
        f"(expected ~lid speed 1.0 since lid is the driver)"
    )


if __name__ == "__main__":
    main()
