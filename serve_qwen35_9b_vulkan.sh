#!/usr/bin/env bash
# Pinned official llama.cpp Vulkan server for Linux x64.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD="b10621"
SERVER="${ROOT_DIR}/llama-${BUILD}/llama-server"
MODEL="${ROOT_DIR}/models/Qwen3.5-9B-Q4_K_M.gguf"

if [[ ! -f "${MODEL}" ]]; then
  echo "Model not found: ${MODEL}" >&2
  exit 1
fi

if [[ ! -x "${SERVER}" ]]; then
  echo "Pinned server not found: ${SERVER}" >&2
  exit 1
fi

exec "${SERVER}" \
  --model "${MODEL}" \
  --n-gpu-layers -1 \
  --ctx-size 8192 \
  --jinja \
  --host 127.0.0.1 \
  --port 8080 \
  "$@"
