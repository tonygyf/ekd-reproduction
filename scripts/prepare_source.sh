#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
git submodule update --init EKD
if git -C EKD apply --reverse --check ../patches/upstream-fixes.patch 2>/dev/null; then
  printf 'Official source fixes already applied.\n'
else
  git -C EKD apply --check ../patches/upstream-fixes.patch
  git -C EKD apply ../patches/upstream-fixes.patch
fi
