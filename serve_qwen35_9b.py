#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "llama-cpp-python[server]>=0.3.16",
# ]
# ///

"""Run the downloaded Qwen 3.5 GGUF through the llama.cpp OpenAI-compatible API."""

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = ROOT / "models" / "Qwen3.5-9B-Q4_K_M.gguf"


def parse_args() -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser(
        description="Start a llama.cpp server for Qwen3.5-9B-Q4_K_M.gguf."
    )
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--ctx-size", type=int, default=8192)
    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=-1,
        help="Number of layers to offload; -1 offloads all supported layers, 0 is CPU-only.",
    )
    return parser.parse_known_args()


def main() -> None:
    args, passthrough = parse_args()
    model = args.model.expanduser().resolve()
    if not model.is_file():
        raise SystemExit(f"Model not found: {model}")

    command = [
        sys.executable,
        "-m",
        "llama_cpp.server",
        "--model",
        str(model),
        "--host",
        args.host,
        "--port",
        str(args.port),
        "--n_ctx",
        str(args.ctx_size),
        "--n_gpu_layers",
        str(args.gpu_layers),
        *passthrough,
    ]
    print("Starting llama.cpp server:", " ".join(command), flush=True)
    os.execv(sys.executable, command)


if __name__ == "__main__":
    main()
