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
FILENAME = "Qwen3.5-9B-Q4_K_M.gguf"
LOCAL_DIR = Path("models")


try:
    path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        local_dir=LOCAL_DIR,
    )
except Exception:
    traceback.print_exc()
    raise
else:
    print(path)
