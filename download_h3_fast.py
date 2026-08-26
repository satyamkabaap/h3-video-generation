"""MiniMax H3 downloader — hf_transfer (parallel chunks, resume-safe).
Target layout = ComfyUI models/ folders."""
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import hf_hub_download

MODELS = r"C:\Users\shubh\Documents\comfy\ComfyUI\models"

# (repo_id, filename_in_repo, expected_bytes, target_subfolder)
FILES = [
    ("Kijai/MiniMax-H3-experimental", "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors",
     12540858008, "diffusion_models"),
    ("Comfy-Org/MiniMax-H3", "vae/minimax_h3_video_vae_fp16.safetensors",
     5207808496, None),  # repo path already has vae/
    ("Comfy-Org/MiniMax-H3", "vae/minimax_h3_audio_vae_fp32.safetensors",
     605254808, None),
    ("Comfy-Org/MiniMax-H3", "loras/minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors",
     1956192992, None),
    ("Comfy-Org/Qwen3-VL", "text_encoders/qwen3vl_4b_fp8_scaled.safetensors",
     5242467968, None),
    ("NicoLab28/ClipProj-MiniMax-H3", "mmh3-4b-ClipProj-v3.1.safetensors",
     26256128, "clip_projections"),
    ("NicoLab28/ClipProj-MiniMax-H3", "mmh3-4b-ClipProj-v3.1-mlp.safetensors",
     503423800, "clip_projections"),
]

results = []
for repo, fname, expect, subdir in FILES:
    target_dir = os.path.join(MODELS, subdir) if subdir else MODELS
    os.makedirs(target_dir, exist_ok=True)
    final_name = fname.split("/")[-1]
    final_path = os.path.join(target_dir, final_name)

    # skip if already correct size
    if os.path.exists(final_path) and abs(os.path.getsize(final_path) - expect) < 2:
        print(f"[SKIP] {final_name} already complete", flush=True)
        results.append((final_name, "SKIP"))
        continue
    # remove corrupt/partial leftovers from curl attempts
    if os.path.exists(final_path):
        print(f"[CLEAN] removing wrong-size {final_name} ({os.path.getsize(final_path)})", flush=True)
        os.remove(final_path)

    print(f"[DL] {repo}/{fname} -> {target_dir}", flush=True)
    try:
        got = hf_hub_download(repo_id=repo, filename=fname, local_dir=target_dir)
        size = os.path.getsize(got)
        ok = abs(size - expect) < 2
        print(f"[{'OK' if ok else 'FAIL'}] {final_name}: {size} / {expect}", flush=True)
        results.append((final_name, "OK" if ok else "FAIL"))
    except Exception as e:
        print(f"[ERROR] {final_name}: {e}", flush=True)
        results.append((final_name, f"ERROR: {str(e)[:120]}"))

print("\n=== SUMMARY ===", flush=True)
for n, s in results:
    print(f"  {s:8s} {n}", flush=True)
failed = [n for n, s in results if s not in ("OK", "SKIP")]
print(f"\n=== {'ALL DONE' if not failed else f'FAILED: {failed}'} ===", flush=True)
