@echo off
setlocal

set "ROOT=%~dp0"
set "SERVER=%ROOT%bin\llama-server.exe"
set "MODEL=%ROOT%models\Qwen3.5-9B-Q4_K_M.gguf"
set "MMPROJ=%ROOT%models\mmproj-Qwen3.5-9B-BF16.gguf"

if not exist "%SERVER%" (
  echo llama-server.exe not found: %SERVER%
  exit /b 1
)

if not exist "%MODEL%" (
  echo Model not found: %MODEL%
  exit /b 1
)

if not exist "%MMPROJ%" (
  echo Multimodal projector not found: %MMPROJ%
  exit /b 1
)

"%SERVER%" ^
  --model "%MODEL%" ^
  --mmproj "%MMPROJ%" ^
  --n-gpu-layers -1 ^
  --ctx-size 8192 ^
  --jinja ^
  --host 127.0.0.1 ^
  --port 8080 ^
  %*
