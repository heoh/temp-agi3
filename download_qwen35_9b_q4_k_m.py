#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "huggingface_hub>=0.30",
# ]
# ///

import os
from pathlib import Path
import traceback

# Use the standard resumable HTTP downloader. This avoids delegating the transfer
# to the separate hf-xet process, which may not share this script's network access.
os.environ["HF_HUB_DISABLE_XET"] = "1"

from huggingface_hub import hf_hub_download


REPO_ID = "lmstudio-community/Qwen3.5-9B-GGUF"
FILENAMES = [
    "Qwen3.5-9B-Q4_K_M.gguf",
    "mmproj-Qwen3.5-9B-BF16.gguf",
]
LOCAL_DIR = Path("models")


try:
    paths = [
        hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            local_dir=LOCAL_DIR,
        )
        for filename in FILENAMES
    ]
except Exception:
    traceback.print_exc()
    raise
else:
    print("\n".join(paths))
