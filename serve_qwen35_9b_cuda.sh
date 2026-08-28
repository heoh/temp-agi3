#!/usr/bin/env bash
# Run the locally built CUDA llama.cpp server.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER="${ROOT_DIR}/.local/llama.cpp-b10621/build-cuda/bin/llama-server"
MODEL="${ROOT_DIR}/models/Qwen3.5-9B-Q4_K_M.gguf"
MMPROJ="${ROOT_DIR}/models/mmproj-Qwen3.5-9B-BF16.gguf"

if [[ ! -x "${SERVER}" ]]; then
  echo "CUDA server not found. Run ./build_llama_cpp_cuda.sh first." >&2
  exit 1
fi

if [[ ! -f "${MODEL}" ]]; then
  echo "Model not found: ${MODEL}" >&2
  exit 1
fi

if [[ ! -f "${MMPROJ}" ]]; then
  echo "Multimodal projector not found: ${MMPROJ}" >&2
  exit 1
fi

exec "${SERVER}" \
  --model "${MODEL}" \
  --mmproj "${MMPROJ}" \
  --n-gpu-layers -1 \
  --ctx-size 8192 \
  --jinja \
  --host 127.0.0.1 \
  --port 8080 \
  "$@"
