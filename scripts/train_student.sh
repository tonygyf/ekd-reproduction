#!/usr/bin/env bash
set -euo pipefail
trap 'printf "failed\n" > /workspace/artifacts/training-status.txt' ERR
printf 'running\n' > /workspace/artifacts/training-status.txt
cd /workspace/EKD
python tools/train.py --cfg configs/cifar100/ekd/resnet32x4_resnet8x4.yaml --seed 42 "$@" \
  LOG.WANDB False LOG.PREFIX /workspace/artifacts/runs \
  EXPERIMENT.NAME resnet32x4_resnet8x4_seed42
python - <<'PY'
import torch
state = torch.load('/workspace/artifacts/runs/cifar100_baselines/resnet32x4_resnet8x4_seed42/latest', map_location='cpu', weights_only=False)
assert state['epoch'] == 240, f"Training stopped at epoch {state['epoch']}"
assert all(torch.isfinite(v).all() for v in state['model'].values())
PY
python /workspace/scripts/evaluate.py --model resnet8x4 \
  --checkpoint /workspace/artifacts/runs/cifar100_baselines/resnet32x4_resnet8x4_seed42/student_best \
  --output /workspace/artifacts/student-best-eval.json
python /workspace/scripts/evaluate.py --model resnet8x4 \
  --checkpoint /workspace/artifacts/runs/cifar100_baselines/resnet32x4_resnet8x4_seed42/student_latest \
  --output /workspace/artifacts/student-last-eval.json
printf 'completed\n' > /workspace/artifacts/training-status.txt
