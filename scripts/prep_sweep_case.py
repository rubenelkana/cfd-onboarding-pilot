"""Build a sweep case from a base counter-flow flame, varying the inlet jet velocity.

Copies the base case to a new directory and rewrites the fuel and air inlet
velocity in `0/U`. Both inlets are set symmetrically so the stagnation plane
stays at the geometric midpoint.

Usage:
    python scripts/prep_sweep_case.py \\
        --base tutorials/counterFlowFlame2D \\
        --u 0.15 \\
        --out tutorials/sweep_velocity/U_0.15
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


def rewrite_U_file(u_path: Path, u_jet: float) -> None:
    text = u_path.read_text()
    # Match the fuel uniform line and the air uniform line independently.
    # Pattern looks for: `fuel { ... value uniform (X 0 0); }`
    fuel_block_re = re.compile(
        r"(fuel\s*\{[^}]*?value\s+uniform\s+\()-?\d*\.?\d+(\s+0\s+0\)\s*;[^}]*\})",
        re.DOTALL,
    )
    air_block_re = re.compile(
        r"(air\s*\{[^}]*?value\s+uniform\s+\()-?\d*\.?\d+(\s+0\s+0\)\s*;[^}]*\})",
        re.DOTALL,
    )
    text = fuel_block_re.sub(rf"\g<1>{u_jet:g}\g<2>", text)
    text = air_block_re.sub(rf"\g<1>{-u_jet:g}\g<2>", text)
    u_path.write_text(text)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--base", type=Path, required=True, help="path to the base case")
    p.add_argument("--u", type=float, required=True, help="fuel inlet velocity magnitude (m/s)")
    p.add_argument("--out", type=Path, required=True, help="path to the new sweep case dir")
    args = p.parse_args()

    if args.out.exists():
        shutil.rmtree(args.out)
    # Copy only what we need: 0/, constant/, system/
    args.out.mkdir(parents=True)
    for sub in ("0", "constant", "system"):
        shutil.copytree(args.base / sub, args.out / sub)

    u_path = args.out / "0" / "U"
    rewrite_U_file(u_path, args.u)
    print(f"prepared {args.out} with U_jet = {args.u:g} m/s")


if __name__ == "__main__":
    main()
