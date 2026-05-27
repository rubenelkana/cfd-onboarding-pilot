# Pilot plan — 6 phases

This document is the source-of-truth for what the pilot covers, what is intentionally out of scope, and where each phase sits in execution.

## Scope framing

The pilot is **bounded by what a candidate can reasonably do solo before PhD admission**. Phases 1–6 below sit within that envelope. Phases 7–9 (listed at the end) are deliberately deferred to post-admission because they require infrastructure or guidance that does not exist pre-application.

## Phase status

| # | Phase | Status | Deliverable |
|---|---|---|---|
| 1 | Environment — Docker + OpenFOAM 12 container | ⏳ in progress | Working `foamHelp`; container documented |
| 2 | Cavity flow — non-reacting baseline tutorial | ⏳ queued | Reproduced velocity field; matplotlib plot; setup-log notes |
| 3 | Combustion tutorial — `simpleReactingFoam` counter-flow flame | ⏳ queued | Temperature + species concentration plots; tutorial notes |
| 4 | Parameter sweep on the combustion case | ⏳ queued | 5–10 runs over one parameter; trend plots; CSV dataset of inputs↔outputs |
| 5 | Annotated reading — Liu, Zhang & Shen (2022, *Chem. Eng. Sci.*) | ⏳ queued (post-send) | Markdown notes: figure-by-figure annotation, method critique, extension ideas |
| 6 | ML surrogate on the Phase-4 dataset | ⏳ queued (post-send) | Random forest / XGBoost regressor trained on Phase-4 CSV; CFD-truth vs ML-prediction plots; notes on the methodological homage to Liu 2022 |

## What is deliberately not in this pilot

| # | Phase | Why deferred |
|---|---|---|
| 7 | 2D blast-furnace raceway custom-geometry combustion | Requires the CFD intuition that Phases 1–4 build; borderline solo, but better attempted under supervisor guidance once admitted |
| 8 | Coupled HMB ↔ CFD multi-view pipeline replicating Liu et al. (2026, *Fuel*) | Requires depth of paper understanding that only matures after Phase 5–6, and would benefit from Liu's direct guidance |
| 9 | Industrial-scale 3-D CFD on a representative reactor | Requires Pawsey Supercomputing Centre allocation, only accessible post-admission via UWA |

## Execution window

| Window | Phases | Approximate dates |
|---|---|---|
| Pre-application (cold email) | 1 – 4 | 2026-05-28 → 2026-06-07 |
| Post-send / pre-zoom-call | 5 – 6 | 2026-06-09 → 2026-06-24 |

## Choice of stack

**OpenFOAM 12** via Docker. Chosen over ANSYS Fluent for licence accessibility (Fluent requires a commercial licence the candidate does not yet hold); transition to Fluent under a UWA academic licence post-admission is straightforward — both are Navier-Stokes solvers with similar primitives. Plotting via Python (matplotlib, pandas). ML in Phase 6 via scikit-learn / XGBoost.

## Honest scoping

This is a **tutorial-grade** pilot, not a publication-quality CFD study. The goal is to evidence (i) capability to install, configure, and run an open-source CFD pipeline end-to-end without supervision; (ii) capability to extend a tutorial case into a small parameter study; and (iii) capability to bridge CFD output to ML methodology — the same "expensive physics ↔ cheap surrogate" pattern Liu, Zhang & Shen 2022 use in their *Chemical Engineering Science* paper.

Any framing of the resulting artefacts as a replication of the published research would be premature. They are a candidate's pre-admission readiness exercise.
