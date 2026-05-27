# CFD Onboarding Pilot — OpenFOAM tutorial study

Self-directed CFD ramp ahead of a PhD application to UWA's Chemical Engineering scholarship *Advanced CFD Studies for Chemical Engineering Processes* (closes 30 Jun 2026). Documents the process of going from a metallurgical-engineering / ML background (see related repo: <https://github.com/rubenelkana/predictive-maintenance-bearing-ml>) to a working OpenFOAM toolchain capable of running and adapting combustion-relevant tutorial cases.

## Intent

This is a **tutorial-grade case study**, not a publication-quality CFD reproduction. The goal is to evidence (i) that the candidate can install, configure, and run an open-source CFD pipeline end-to-end without supervision; and (ii) that the candidate can read, interpret, and document the output in a way that demonstrates pre-PhD readiness to engage Year 1 CFD coursework. Any framing of this work as a replication of published research would be premature.

## Plan (4–6 weeks)

| Phase | Deliverable | Status |
|---|---|---|
| 1. Install & first run | OpenFOAM working on local machine; cavity flow tutorial reproduced | Pending |
| 2. Tutorial walkthrough | Combustion-relevant tutorials (counter-flow flame, simple reacting flow); plots saved | Pending |
| 3. Parameter sensitivity | Re-run a chosen tutorial with one parameter swept; document trend | Pending |
| 4. Synthesis notes | One-page reflective writeup tying the pilot to the proposed PhD direction | Pending |

## Choice of stack

**OpenFOAM** chosen over ANSYS Fluent for license accessibility. Fluent requires a commercial licence the candidate does not currently hold; OpenFOAM is open-source and installable on Linux / macOS / Windows (WSL or Docker). Transition to Fluent under a UWA academic licence post-admission is straightforward — both are Navier-Stokes solvers with similar primitives; capability in one transfers to the other.

## Context

PhD candidate profile: BEng Metallurgical Engineering ITB 2017, 8 years industry (PM / mining / digital transformation), recent ML mini-research on the NASA IMS bearing dataset (see linked repo). Pivoting back to research with a focus on coupled CFD–ML for pyrochemical reactors. Full background: <https://rubenelkana.com>.

## License

MIT — see [LICENSE](LICENSE) once added (planned alongside Phase 1 deliverable).
