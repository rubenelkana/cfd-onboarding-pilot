# Phase 4 — Symmetric-jet velocity sweep of the counter-flow flame

**Date:** 2026-05-28
**Base case:** `tutorials/counterFlowFlame2D` (from Phase 3)
**Sweep parameter:** $U_{jet}$, the magnitude of the inlet velocity on both the fuel and air boundaries (kept symmetric so the stagnation plane stays at the geometric midpoint)
**Levels:** 0.05, 0.10, 0.15, 0.20, 0.25, 0.30 m/s (baseline is 0.10)
**Wall time:** ~6 × 15 s ≈ 90 s for the run portion; case preparation + post-processing add ~20 s

## Why velocity

The scholarship target's research group (Liu, Mathieson and Shen 2026; Liu, Zhang and Shen 2022) routinely sweeps tuyere injection velocity in pulverised-coal blast-furnace CFD as a way to map the operating window. Symmetric counter-jet velocity in this 2D toy case is the cleanest single-knob analogue of "increase tuyere injection velocity" — it raises the strain rate, narrows the reaction zone, and shifts where the diffusion flame sits.

Other candidates I considered and parked for later:

- **Inlet temperature** would test ignition behaviour; with single-step methane chemistry and 293 K inlets, the flame is already ignited and steady, so a temperature sweep would mostly confirm the obvious.
- **O₂/N₂ ratio (oxygen enrichment)** is the closest analogue to Liu's H₂-coal co-injection work, but requires modifying two coupled boundary fields and the species set, which is more invasive. Worth coming back to in Phase 7 (out of scope here).

Sticking with velocity gives clean, monotonic trends — exactly what a small ML surrogate needs in Phase 6.

## Sweep results (raw)

From [`results.csv`](../tutorials/sweep_velocity/results.csv):

| $U_{jet}$ (m/s) | peak $T$ (K) | $x_{flame}$ (mm) | FWHM (mm) | $Y_{CO_2,max}$ | $Y_{H_2O,max}$ |
|---|---|---|---|---|---|
| 0.05 | 1886 | 12.60 | 7.80 | 0.079 | 0.064 |
| 0.10 | 2105 | 11.60 | 5.05 | 0.120 | 0.098 |
| 0.15 | 2123 | 10.80 | 3.90 | 0.135 | 0.111 |
| 0.20 | 2122 | 10.40 | 3.30 | 0.140 | 0.115 |
| 0.25 | 2121 | 10.00 | 3.00 | 0.141 | 0.116 |
| 0.30 | 2116 | 9.80 | 2.80 | 0.141 | 0.116 |

## What the trends look like

![sweep trends](../figures/04_sweep_trends.png)

Four observations, each a textbook diffusion-flame response:

1. **Peak temperature plateaus at ~2120 K** once $U_{jet} \geq 0.10$ m/s. The lowest velocity (0.05 m/s) sits at 1886 K — about 230 K below the plateau — because the reaction zone is much wider (7.8 mm FWHM) and conductive heat loss to the fuel-rich and air-rich sides becomes a non-negligible fraction of the heat-release rate. Once strain rate is high enough to confine the reaction zone, the flame approaches its strain-rate-independent adiabatic-like ceiling.
2. **Flame migrates toward the geometric midpoint as $U_{jet}$ rises.** At 0.05 m/s, fuel diffusion dominates momentum and the stoichiometric surface sits at $x = 12.6$ mm — well on the air side. Each step of $U_{jet}$ pushes the flame about 0.5–1.0 mm closer to $x = 10$ mm; at $U_{jet} = 0.25$ m/s the flame *exactly* hits the geometric midpoint, and slightly overshoots to 9.8 mm at $U_{jet} = 0.30$ m/s. This is the classical momentum–diffusion balance — fuel and air molecular masses differ by a factor of 16/29 ≈ 0.55, so the symmetric-velocity flame settles where the diffusive imbalance is offset by the convective imbalance.
3. **FWHM shrinks monotonically from 7.8 mm to 2.8 mm.** Higher jet velocity = higher strain rate = thinner diffusive heating zone. Quantitatively, FWHM × $U_{jet}$ stays approximately constant (~0.4 mm·s — within a factor of 2 across the sweep), which is the leading-order $1/\dot{\gamma}^{0.5}$-ish scaling expected from a diffusion-controlled flame.
4. **Products track peak $T$.** Both $Y_{CO_2}$ and $Y_{H_2O}$ rise from ~0.08 / ~0.06 (at the low-strain heat-leaky end) to plateau at 0.14 / 0.12 (close to the stoichiometric methane-air values 0.151 / 0.124). The plateau confirms the heat-loss-limited regime is gone above $U_{jet} = 0.15$ m/s.

## What I learned

- Even at this toy scale, the dataset has clean, learnable structure: one input, five outputs, monotonic + smooth. This is the *exact* signal shape an ML surrogate can over-fit at zero generalisation risk if I'm not careful in Phase 6 — important to plan a train/test split where 1–2 of the 6 points are held out.
- Repeating the same `prepare → run → post-process` pattern across 6 cases via a Bash orchestrator + Python case-prep utility is much cleaner than copy-paste-edit. Worth carrying this pattern into any future parameter studies — the only thing that changes between cases is the input dictionary or boundary file.
- Docker daemon will quietly stop on macOS when the laptop sleeps. The first attempt of this sweep failed mid-loop for exactly that reason. A `docker info` health-check at the start of the orchestrator would prevent the silent failure — worth adding if the sweep gets longer or unattended.

## Pointer to Phase 5 and Phase 6

Phase 5 will be desk-work: read Liu, Zhang and Shen (2022, *Chemical Engineering Science*) carefully — that paper builds a random-forest surrogate trained on a CFD database of pulverised-coal in-furnace phenomena, and uses it for fast prediction. The methodology I am about to apply to the velocity sweep in Phase 6 is intentionally a tutorial-grade version of theirs. The reading notes will sit at `notes/05_liu_2022_ces_reading.md`.

Phase 6 will train a small regressor (random forest plus a baseline linear model) on the 6-row dataset, validate via leave-one-out, and plot CFD-truth vs surrogate predictions side-by-side with the trends in this Phase. The honest framing: 6 training points is far too few to claim anything except "I can wire this end to end" — and that, alongside Liu's own framing of their 2022 paper, is exactly the point.
