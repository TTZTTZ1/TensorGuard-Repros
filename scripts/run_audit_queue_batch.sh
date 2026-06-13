#!/usr/bin/env bash
set -euo pipefail

QUEUE="${1:?usage: bash TensorGuard-Repros/scripts/run_audit_queue_batch.sh <queue.tsv> [start] [limit] [timeout_sec]}"
START="${2:-1}"
LIMIT="${3:-10}"
TIMEOUT_SEC="${4:-60}"

if [[ ! -f "$QUEUE" ]]; then
  echo "queue not found: $QUEUE" >&2
  exit 1
fi

QUEUE_NAME="$(basename "$QUEUE" .tsv)"
OUT_DIR="TensorGuard-Repros/logs/audit_next/runs/${QUEUE_NAME}"
mkdir -p "$OUT_DIR"

echo "queue=$QUEUE" | tee -a "$OUT_DIR/index.log"
echo "start=$START limit=$LIMIT timeout=${TIMEOUT_SEC}s" | tee -a "$OUT_DIR/index.log"
echo "started=$(date '+%F %T')" | tee -a "$OUT_DIR/index.log"

count=0
run_count=0
tail -n +2 "$QUEUE" | while IFS=$'\t' read -r priority bucket score api label source reason evidence; do
  if [[ -z "${source:-}" ]]; then
    continue
  fi
  count=$((count + 1))
  if (( count < START )); then
    continue
  fi
  run_count=$((run_count + 1))
  if (( run_count > LIMIT )); then
    break
  fi

  safe_label="${label//\//_}"
  log="$OUT_DIR/${count}_${safe_label}.log"
  echo "===== queue_index=${count} batch_index=${run_count}/${LIMIT} ${priority} ${label} source=${source} =====" | tee -a "$OUT_DIR/index.log"

  if [[ ! -f "$source" ]]; then
    echo "missing source: $source" | tee "$log"
    continue
  fi

  CUDA_LAUNCH_BLOCKING=1 timeout "${TIMEOUT_SEC}s" \
    python torch2cuda.py --mode duel --input "$source" \
    > "$log" 2>&1 || true
done

echo "finished=$(date '+%F %T')" | tee -a "$OUT_DIR/index.log"
echo "logs written to $OUT_DIR"

grep -RInE 'INTERNAL ASSERT|please report|Segmentation fault|Floating point exception|double free|free\(\)|invalid pointer|invalid next size|Check failed|device-side assert|cudaErrorAssert|AcceleratorError|returncode=13[469]' \
  "$OUT_DIR" > "$OUT_DIR/interesting_hits.txt" || true

echo "interesting hits:"
sed -n '1,80p' "$OUT_DIR/interesting_hits.txt" || true
