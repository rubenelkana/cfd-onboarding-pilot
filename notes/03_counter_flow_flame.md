# Phase 3 — Counter-flow methane flame (combustion baseline)

**Date:** 2026-05-28
**Solver:** `foamRun` with module `multicomponentFluid`
**Case:** copied from `$FOAM_TUTORIALS/multicomponentFluid/counterFlowFlame2D`
**Wall time:** 15.1 s on Apple M2 / Rosetta-2 (for the reduced `endTime = 0.1 s`)

## What this case is

Two opposing inlets, 20 mm apart:

- **Fuel inlet** (left, $x = 0$): pure CH₄ at 293 K
- **Air inlet** (right, $x = 20$ mm): O₂/N₂ at the standard mass-fraction mix (~0.23/0.77), 293 K

The fuel and oxidiser counter-propagate, and the diffusion flame forms in the strain region between them — somewhere near the stoichiometric mixture fraction surface. With single-step methane chemistry (the default in this OpenFOAM-11 tutorial), the steady-state structure is a sharp temperature peak with co-located CO₂ and H₂O production.

This is the first real combustion case in the pilot — it brings species transport, reaction chemistry, and the multicomponent solver into play. The cavity in Phase 2 was incompressible non-reacting; nothing in that pipeline tested the chemistry side.

## What I changed from the bundled tutorial

| Setting | Bundled | My value | Reason |
|---|---|---|---|
| `endTime` (in `system/controlDict`) | 0.5 s | **0.1 s** | The flame sheet is already established by $t = 0.1$ s with peak $T = 2105$ K (close to the CH₄/air adiabatic flame temperature ~2200 K). Running to $t = 0.5$ s would add no new physics, only ~50 s more wall time. Will use the full 0.5 s in Phase 4 when sweeping. |

Everything else is the stock tutorial (mesh, chemistry, transport, boundary conditions, solvers).

## What I did

1. Copied the tutorial into `tutorials/counterFlowFlame2D/` so it is version-controlled with the pilot.
2. Reduced `endTime` to 0.1 s (see above).
3. Ran `blockMesh` → 4000 hex cells generated.
4. Ran `foamRun` end-to-end → reached `t = 0.1` s in 15.1 s wall time. Wrote two time snapshots ($t = 0$ and $t = 0.1$).
5. Wrote `system/sampleDict` to extract `T, CH4, O2, N2, CO2, H2O` along the horizontal centreline.
6. Ran `postProcess -func sampleDict -time 0.1`.
7. Plotted the temperature + species profiles with `scripts/plot_flame.py`.

## What the figure shows

![flame axis profile](../figures/03_flame_axis_t0.1.png)

- **Temperature panel (left).** Sharp Gaussian-shaped peak at $x = 11.6$ mm reaching $T = 2105$ K. Inlet temperature 293 K is preserved at both ends. The peak sits closer to the air boundary than to the fuel boundary because the stoichiometric mixture fraction for CH₄/air is small ($Z_{st} \approx 0.055$ by mass) — combustion needs much more air than methane per unit mass, so the iso-surface $Z = Z_{st}$ sits close to where $Z$ drops toward zero on the air side. Differential diffusion (CH₄ is lighter than O₂ and N₂) and finite-rate chemistry shift the actual peak-temperature location modestly from the pure stoichiometric prediction, which is why $x_{flame}$ at $U_{jet} = 0.1$ lands at 11.6 mm rather than nearer 18 mm.
- **Species panel (right).** Five fields tell the chemistry story:
  - Y(CH₄) is 1.0 at the fuel inlet, drops sharply through the reaction zone, and is fully consumed by $x \approx 12.5$ mm.
  - Y(O₂) is ~0.23 at the air inlet (correct stoichiometric air composition), drops to zero through the reaction zone where it is consumed.
  - Y(N₂) ramps from 0 (fuel side) to ~0.77 (air side) — correct stoichiometric air N₂ fraction. Inert, so no consumption.
  - Y(CO₂) and Y(H₂O) peak together at $x \approx 11$ mm, both at ~0.10–0.12 mass fraction. Product co-location with the temperature peak is the textbook signature of a reaction zone.

## What I learned

- The OpenFOAM-11 `multicomponentFluid` module uses the same `foamRun` shell as `incompressibleFluid` from Phase 2 — only the `solver` line in `controlDict` and the species set in `0/` differ. The shell pattern is consistent, which is a relief for adding more cases.
- `adjustTimeStep yes` matters: nominal `deltaT = 1e-6 s` would imply 500,000 time steps to reach 0.5 s, but with $\text{Co}_{max} = 0.4$ the solver ramped up to $\Delta t \approx 2.7 \times 10^{-4}$ s quickly. So real step count is ~400, not 500,000.
- When `sampleDict` is given multiple `fields`, the raw `setFormat` writes one combined `.xy` file with all fields side-by-side as columns — not one file per field as I'd assumed. Updated the plot script to read columns from the single file.
- Rosetta-2 emulation overhead is still negligible at this mesh size (4000 cells, 15 s wall time). Phase 4 sweep with 5–10 runs at the same mesh should comfortably fit in laptop wall-time budget.

## Sanity check vs published expectations

| Quantity | Observed | Expected | Note |
|---|---|---|---|
| Peak temperature | 2105 K | ~2200 K (CH₄/air adiabatic, single-step) | Slightly lower than adiabatic — typical for diffusion flames at finite strain rate |
| Peak T location | $x = 11.6$ mm | Near the stoichiometric-Z surface, expected on the air side of geometric midpoint since $Z_{st} \approx 0.055$ | ✓ correct side; finite-rate chemistry shifts the actual peak modestly toward the fuel side of the pure-mixing prediction |
| Y(CO₂) max | 0.12 | ~0.15 (stoichiometric CH₄/air) | ✓ within reasonable range for finite-rate single-step chemistry |
| Y(N₂) on air inlet | 0.77 | 0.767 (air composition) | ✓ exact |

## Pointer to Phase 4

Phase 4 will reuse this case as the base, sweep one parameter (most likely fuel-inlet velocity to vary the strain rate, or the equivalence ratio if that maps cleanly to a single boundary-condition knob), and collect the resulting (input → output) pairs into a CSV. That CSV becomes the training dataset for the ML surrogate in Phase 6 — the same "expensive physics → cheap surrogate" pattern that Liu, Zhang & Shen 2022 use in their *Chemical Engineering Science* paper.
