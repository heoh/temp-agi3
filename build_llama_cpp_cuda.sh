#!/usr/bin/env bash
# Build the pinned llama.cpp server with CUDA for an RTX 3080 Ti (SM 8.6).
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD="b10621"
SOURCE_DIR="${ROOT_DIR}/.local/llama.cpp-${BUILD}"
BUILD_DIR="${SOURCE_DIR}/build-cuda"

for command in git cmake; do
  if ! command -v "${command}" >/dev/null 2>&1; then
    echo "Required command not found: ${command}" >&2
    echo "Install Git and CMake, then run this script again." >&2
    exit 1
  fi
done

NVCC="${CUDACXX:-$(command -v nvcc || true)}"
if [[ -z "${NVCC}" ]]; then
  for candidate in /usr/local/cuda/bin/nvcc /usr/local/cuda-*/bin/nvcc; do
    if [[ -x "${candidate}" ]]; then
      NVCC="${candidate}"
      break
    fi
  done
fi

if [[ -z "${NVCC}" || ! -x "${NVCC}" ]]; then
  echo "CUDA compiler (nvcc) not found. Install the NVIDIA CUDA Toolkit first." >&2
  exit 1
fi

echo "Using CUDA compiler: ${NVCC}"

if [[ ! -d "${SOURCE_DIR}/.git" ]]; then
  mkdir -p "${ROOT_DIR}/.local"
  git clone --depth 1 --branch "${BUILD}" \
    https://github.com/ggml-org/llama.cpp.git "${SOURCE_DIR}"
fi

cmake -S "${SOURCE_DIR}" -B "${BUILD_DIR}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DGGML_CUDA=ON \
  -DCMAKE_CUDA_COMPILER="${NVCC}" \
  -DCMAKE_CUDA_ARCHITECTURES=86

cmake --build "${BUILD_DIR}" --target llama-server --parallel "$(nproc)"

SERVER="${BUILD_DIR}/bin/llama-server"
echo
echo "Built CUDA server: ${SERVER}"
echo "Verify with: ${SERVER} --list-devices"
