# Phase 2 — Lid-driven cavity (non-reacting baseline)

**Date:** 2026-05-27
**Solver:** `foamRun` with module `incompressibleFluid`
**Mesh:** 20 × 20 × 1 (the bundled OpenFOAM 11 tutorial)
**Wall time:** 5.7 s on Apple M2 via Rosetta-2 emulation (Docker Desktop 27.5.1, `--platform linux/amd64`)

## What this case is

The canonical first CFD case: a square cavity with a lid that moves at 1 m/s in the $+x$ direction. The other three walls are no-slip. Inside the cavity, a clockwise eddy forms; the velocity along the vertical centreline at $x = 0.05\,\text{m}$ should be 1 m/s at the lid, drop sharply to a recirculation peak negative value somewhere in the lower third, and pass through zero near the middle.

This is a non-reacting incompressible test — its job is to confirm that the toolchain runs end-to-end, not to teach me anything about combustion.

## What I did

1. Copied `$FOAM_TUTORIALS/incompressibleFluid/cavity` into `tutorials/cavity` so the case is version-controlled with the repo (the bundled tutorial inside the container is read-only).
2. Ran `blockMesh` → 400 hex cells generated, mesh quality OK (no warnings).
3. Ran `foamRun` end-to-end to $t = 10\,\text{s}$ with `writeInterval = 100` time steps, so 21 time directories are written ($t = 0, 0.5, 1, \ldots, 10$).
4. Wrote a `system/sampleDict` to sample the velocity field along the vertical and horizontal centrelines, then ran `postProcess -func sampleDict -time 10`.
5. Plotted the two centrelines with `scripts/plot_cavity.py`.

## What the figure shows

![cavity centrelines](../figures/02_cavity_centrelines.png)

- **Vertical centreline ($x = 0.05$):** $U_x$ climbs from $-0.16\,\text{m/s}$ at the bottom of the cavity (where the floor recirculation drags the flow backward) through zero near $y = 0.06$ and up to the lid speed $1.0\,\text{m/s}$ at $y = 0.1$. The numerical sanity check in the plot script confirms the peak $|U_x|$ in the upper 15% of the cavity is exactly 1.000 m/s — matches the lid Dirichlet boundary condition to printed precision.
- **Horizontal centreline ($y = 0.05$):** $U_y$ peaks positive ($\sim +0.14\,\text{m/s}$) near the left wall and negative ($\sim -0.21\,\text{m/s}$) near the right wall. This is the antisymmetric "rotation" signature of the central eddy: fluid rising on the left, falling on the right.

## What I learned

- The OpenFOAM 11 solver-as-module pattern (`foamRun` + `solver` entry in `controlDict`) is cleaner than the OpenFOAM 7 / `icoFoam`-style invocation I'd read about in older tutorials. Worth noting for Phase 3 — combustion will use the same `foamRun` shell with a different module (`multicomponentFluid` or similar).
- Running amd64 OpenFOAM via Rosetta-2 on Apple Silicon is essentially free at this scale — 5.7 s wall time for 21 time steps × 400 cells means I'm probably not getting close to the emulation overhead floor.
- `postProcess -func sampleDict -time N` is the idiomatic way to extract centreline data after a run; cleaner than parsing the field files by hand.

## What didn't go to plan

Two small misses, neither blocking:

1. First Docker pull attempted `openfoam/openfoam12-paraview510`; v12 is not yet packaged as a Docker image (only source). Fell back to v11.
2. The container image's entrypoint hardcodes an interactive welcome shell — running a command via the default entrypoint silently swallowed my arguments. Fixed in `scripts/of` by explicitly `--entrypoint /bin/bash` and sourcing the OpenFOAM bashrc.

## Pointer to Phase 3

Phase 3 moves to a combustion-relevant tutorial — most likely `tutorials/multicomponentFluid/counterFlowFlame2D` or a comparable case under `multicomponentFluid` — to bring species transport and a reaction model into the loop.
