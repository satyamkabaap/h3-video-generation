#!/bin/bash
# Klein 4B vs Z-Image Turbo benchmark — RTX 3050 4GB
# Usage: bash ~/Documents/sdcpp/bench.sh <prompt>
BIN="C:/Users/shubh/Documents/sdcpp/bin"
MODELS="C:/Users/shubh/Documents/sdcpp/models"
ZIMG="C:/Users/shubh/Documents/comfy/ComfyUI/models"
PROMPT="${1:-cinematic photo of a lone wolf on a snowy mountain at dusk, dramatic lighting, highly detailed}"
OUT="C:/Users/shubh/Documents/sdcpp/out"
mkdir -p "$OUT"

echo "=== GPU before ==="
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader

echo ""
echo "=== TEST 1: FLUX.2 Klein 4B Q4_0 @768x512, 4 steps ==="
cd "$BIN"
START=$(date +%s)
./sd-cli.exe --diffusion-model "$MODELS/flux-2-klein-4b-Q4_0.gguf" \
  --vae "$MODELS/flux2_ae.safetensors" \
  --llm "$MODELS/Qwen3-4B-Q4_K_M.gguf" \
  -p "$PROMPT" -o "$OUT/klein_768x512.png" \
  --steps 4 --cfg-scale 1.0 --sampling-method euler \
  -H 512 -W 768 --backend llm=cpu,diffusion=cuda0,vae=cuda0 \
  --diffusion-fa -v > "$OUT/klein_log.txt" 2>&1
END=$(date +%s)
echo "Klein total: $((END-START))s (exit $?)"
grep -aE "compute buffer|completed|error|failed" "$OUT/klein_log.txt" | tail -8

echo ""
echo "=== TEST 2: Z-Image Turbo Q3_K @768x512, 8 steps ==="
START=$(date +%s)
./sd-cli.exe --diffusion-model "$MODELS/z_image_turbo-Q3_K.gguf" \
  --vae "$MODELS/flux_ae.safetensors" \
  --llm "$MODELS/Qwen3-4B-Instruct-2507-Q4_K_M.gguf" \
  -p "$PROMPT" -o "$OUT/zimage_768x512.png" \
  --steps 8 --cfg-scale 1.0 --sampling-method euler --scheduler simple \
  -H 512 -W 768 --backend llm=cpu,diffusion=cuda0,vae=cuda0 \
  --diffusion-fa -v > "$OUT/zimage_log.txt" 2>&1
END=$(date +%s)
echo "Z-Image total: $((END-START))s (exit $?)"
grep -aE "compute buffer|completed|error|failed" "$OUT/zimage_log.txt" | tail -8

echo ""
echo "=== Results ==="
ls -la "$OUT"/*.png 2>/dev/null
