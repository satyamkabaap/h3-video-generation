#!/bin/bash
# Quick image gen — FLUX.2 Klein 4B (default) ya Z-Image Turbo
# Usage:
#   bash gen.sh "prompt"                        → t2i @768x512
#   bash gen.sh "prompt" 1024 576               → custom WxH
#   bash gen.sh "edit prompt" 768 512 ref.png   → image EDIT mode
P="C:/Users/shubh/Documents/sdcpp"
BIN="$P/bin/sd-cli.exe"
M="$P/models"
OUT="$P/out/$(date +%s).png"
PROMPT="$1"; W="${2:-768}"; H="${3:-512}"; REF="$4"

ARGS=(--diffusion-model "$M/flux-2-klein-4b-Q4_0.gguf" --vae "$M/flux2_ae.safetensors"
      --llm "$M/Qwen3-4B-Q4_K_M.gguf" --steps 4 --cfg-scale 1.0
      --sampling-method euler -W "$W" -H "$H"
      --backend llm=cpu,diffusion=cuda0,vae=cuda0 --diffusion-fa)

[ -n "$REF" ] && ARGS+=(-r "$REF")

cd "$P/bin" && ./sd-cli.exe "${ARGS[@]}" -p "$PROMPT" -o "$OUT" 2>/dev/null
echo "saved: $OUT"
