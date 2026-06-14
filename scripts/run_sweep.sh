#!/usr/bin/env bash
# Sweep the counter-flow flame over a list of inlet jet velocities.
# Each case is built fresh from the base, run end-to-end, and sampled.
#
# Usage:
#   ./scripts/run_sweep.sh

set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

BASE="tutorials/counterFlowFlame2D"
OUT_ROOT="tutorials/sweep_velocity"

# Velocities (m/s). Baseline is 0.10.
VELOCITIES=(0.05 0.10 0.15 0.20 0.25 0.30)

mkdir -p "$OUT_ROOT"

for U in "${VELOCITIES[@]}"; do
    CASE_DIR="$OUT_ROOT/U_${U}"
    echo "=== sweep: U_jet = $U m/s -> $CASE_DIR ==="
    python3 scripts/prep_sweep_case.py --base "$BASE" --u "$U" --out "$CASE_DIR"
    ./scripts/of "cd /workspace/$CASE_DIR && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && postProcess -func sampleDict -time 0.1 > log.postProcess 2>&1"
    echo "  done. final time dirs:"
    ls -d "$CASE_DIR"/[0-9]* 2>/dev/null | sort -V | tail -3
    echo ""
done

echo "=== sweep complete ==="
