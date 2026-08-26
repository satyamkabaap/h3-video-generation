#!/bin/bash
# Wan2.1 T2V 1.3B video gen models — sequential download (parallel throttles!)
MODELS="C:/Users/shubh/Documents/sdcpp/models"
cd "$MODELS" || exit 1

dl() {
  local url="$1" out="$2" expect="$3"
  if [ -f "$out" ] && [ "$(stat -c%s "$out")" = "$expect" ]; then
    echo "[SKIP] $out already complete ($(numfmt --to=iec $expect))"
    return 0
  fi
  echo "[DL] $out ..."
  curl -L -C - --retry 5 --retry-delay 5 -o "$out" "$url" -sS
  local got=$(stat -c%s "$out" 2>/dev/null || echo 0)
  if [ "$got" = "$expect" ]; then
    echo "[OK] $out complete"
  else
    echo "[FAIL] $out: got $got expected $expect"
    return 1
  fi
}

dl "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/vae/wan_2.1_vae.safetensors" \
   "wan_2.1_vae.safetensors" "253815318"

dl "https://huggingface.co/city96/umt5-xxl-encoder-gguf/resolve/main/umt5-xxl-encoder-Q4_K_M.gguf" \
   "umt5-xxl-encoder-Q4_K_M.gguf" "3655145312"

dl "https://huggingface.co/Comfy-Org/Wan_2.1_ComfyUI_repackaged/resolve/main/split_files/diffusion_models/wan2.1_t2v_1.3B_fp16.safetensors" \
   "wan2.1_t2v_1.3B_fp16.safetensors" "2838303560"

echo "=== ALL DOWNLOADS DONE ==="
ls -la wan*.safetensors umt5*Q4_K_M.gguf 2>/dev/null
