#!/bin/bash
# MiniMax H3 — ClipProj 4B route (NO 32B encoder needed)
# Resume-safe: curl -C - continues partial files
BASE="C:/Users/shubh/Documents/comfy/ComfyUI/models"
cd "$BASE" || exit 1

dl() {
  local url="$1" out="$2" expect="$3"
  if [ -f "$out" ] && [ "$(stat -c%s "$out")" = "$expect" ]; then
    echo "[SKIP] $out already complete"
    return 0
  fi
  echo "[DL] $out ..."
  curl -L -C - --retry 5 --retry-delay 5 -sS -o "$out" "https://huggingface.co/$url"
  local got=$(stat -c%s "$out" 2>/dev/null || echo 0)
  if [ "$got" = "$expect" ]; then echo "[OK] $out"; else echo "[FAIL] $out: $got / $expect"; return 1; fi
}

dl "Kijai/MiniMax-H3-experimental/resolve/main/minimax_h3_fl2va_pruned_w4a8_mixed.safetensors" \
   "diffusion_models/minimax_h3_fl2va_pruned_w4a8_mixed.safetensors" "12540858008"

dl "Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_video_vae_fp16.safetensors" \
   "vae/minimax_h3_video_vae_fp16.safetensors" "5207808496"

dl "Comfy-Org/MiniMax-H3/resolve/main/vae/minimax_h3_audio_vae_fp32.safetensors" \
   "vae/minimax_h3_audio_vae_fp32.safetensors" "605254808"

dl "Comfy-Org/MiniMax-H3/resolve/main/loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors" \
   "loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors" "1956192992"

dl "Comfy-Org/Qwen3-VL/resolve/main/text_encoders/qwen3vl_4b_fp8_scaled.safetensors" \
   "text_encoders/qwen3vl_4b_fp8_scaled.safetensors" "5242467968"

dl "NicoLab28/ClipProj-MiniMax-H3/resolve/main/mmh3-4b-ClipProj-v3.1.safetensors" \
   "clip_projections/mmh3-4b-ClipProj-v3.1.safetensors" "26256128"

dl "NicoLab28/ClipProj-MiniMax-H3/resolve/main/mmh3-4b-ClipProj-v3.1-mlp.safetensors" \
   "clip_projections/mmh3-4b-ClipProj-v3.1-mlp.safetensors" "503423800"

echo "=== ALL H3 DOWNLOADS DONE (4B route) ==="
