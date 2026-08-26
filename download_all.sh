#!/bin/bash
# Sequential model downloader - one file at a time, resume-capable
cd ~/Documents/sdcpp

dl() {
  local url="$1" out="$2"
  # skip if already complete (>10MB and grew in last check not needed; rely on size check below)
  echo "[$(date +%H:%M:%S)] START $out"
  curl -sL -C - --retry 8 --retry-delay 3 --retry-all-errors -o "$out" "$url"
  local rc=$?
  echo "[$(date +%H:%M:%S)] DONE($rc) $out size=$(stat -c%s "$out" 2>/dev/null)"
}

# order: small first so binaries unlock testing early
dl "https://github.com/leejet/stable-diffusion.cpp/releases/download/master-829-0a565f2/sd-master-0a565f2-bin-win-cuda12-x64.zip" "sd.zip"
dl "https://github.com/leejet/stable-diffusion.cpp/releases/download/master-829-0a565f2/cudart-sd-bin-win-cu12-x64.zip" "cudart.zip"

cd models
dl "https://huggingface.co/leejet/Z-Image-Turbo-GGUF/resolve/main/z_image_turbo-Q3_K.gguf" "z_image_turbo-Q3_K.gguf"
dl "https://huggingface.co/leejet/FLUX.2-klein-4B-GGUF/resolve/main/flux-2-klein-4b-Q4_0.gguf" "flux-2-klein-4b-Q4_0.gguf"
dl "https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF/resolve/main/Qwen3-4B-Instruct-2507-Q4_K_M.gguf" "Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
dl "https://huggingface.co/unsloth/Qwen3-4B-GGUF/resolve/main/Qwen3-4B-Q4_K_M.gguf" "Qwen3-4B-Q4_K_M.gguf"
dl "https://huggingface.co/black-forest-labs/FLUX.2-dev/resolve/main/ae.safetensors" "flux2_ae.safetensors"
dl "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors" "flux_ae.safetensors"

echo "[$(date +%H:%M:%S)] ALL DOWNLOADS FINISHED"
ls -la ~/Documents/sdcpp/models/
