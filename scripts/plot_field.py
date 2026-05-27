"""Quick plotting helper for OpenFOAM ASCII field files.

Reads a scalar or vector field at a given time step and plots it. Designed for
small 2-D tutorial cases (cavity, counter-flow flame). For production-scale
visualisation, use ParaView.

Usage:
    python scripts/plot_field.py tutorials/cavity/postProcessing/.../U.xy \\
        --title "Cavity flow velocity magnitude, t=0.5s" \\
        --out figures/02_cavity_velocity.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def parse_xy_file(path: Path) -> np.ndarray:
    """Parse an OpenFOAM `.xy` sample file: whitespace-separated columns,
    first column = sample location, remaining columns = field components."""
    return np.loadtxt(path)


def plot_line_field(data: np.ndarray, title: str, out: Path, ylabel: str = "field") -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    x = data[:, 0]
    if data.shape[1] == 2:
        ax.plot(x, data[:, 1], lw=2)
    else:
        # Vector field — plot magnitude
        mag = np.linalg.norm(data[:, 1:], axis=1)
        ax.plot(x, mag, lw=2)
    ax.set_xlabel("position along sample line")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("path", type=Path, help=".xy file from postProcessing")
    p.add_argument("--title", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--ylabel", default="field value")
    args = p.parse_args()

    data = parse_xy_file(args.path)
    plot_line_field(data, args.title, args.out, args.ylabel)


if __name__ == "__main__":
    main()
