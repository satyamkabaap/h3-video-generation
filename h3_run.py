"""MiniMax H3 runner — args: --prompt --out --seed --length --width --height --steps"""
import json, time, argparse, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("--prompt", required=True)
ap.add_argument("--out", default="h3_test/gen")
ap.add_argument("--seed", type=int, default=42)
ap.add_argument("--length", type=int, default=71)      # frames @24fps (17k+5 grid)
ap.add_argument("--width", type=int, default=768)
ap.add_argument("--height", type=int, default=448)
ap.add_argument("--steps", type=int, default=6)
ap.add_argument("--shift", type=float, default=16.0)   # video sigma shift (audio stays 6) — A/B tested Aug 26: 768p+shift16 = best quality/time
args = ap.parse_args()

BASE = "http://127.0.0.1:8188"

wf = {
    "1": {"class_type": "UNETLoader", "inputs": {
        "unet_name": "minimax_h3_fl2va_pruned_w4a8_mixed.safetensors", "weight_dtype": "default"}},
    "2": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_video_vae_fp16.safetensors"}},
    "3": {"class_type": "VAELoader", "inputs": {"vae_name": "minimax_h3_audio_vae_fp32.safetensors"}},
    "4": {"class_type": "ClipProjLoader", "inputs": {
        "clip_name": "qwen3vl_4b_fp8_scaled.safetensors",
        "type": "auto",
        "projection": "mmh3-4b-ClipProj-v3.1.safetensors",
        "device": "cuda:0",
        "mode": "streaming"}},
    "5": {"class_type": "MiniMaxH3SigmaShift", "inputs": {
        "model": ["1", 0], "shift_video": args.shift, "shift_audio": 6.0}},
    "6": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {
        "clip": ["4", 0], "vae": ["2", 0], "prompt": args.prompt,
        "width": args.width, "height": args.height, "length": args.length}},
    "7": {"class_type": "LoraLoaderModelOnly", "inputs": {
        "model": ["5", 0], "lora_name": "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors",
        "strength_model": 1.0}},
    "8": {"class_type": "BasicGuider", "inputs": {"model": ["7", 0], "conditioning": ["6", 0]}},
    "9": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
    "10": {"class_type": "BasicScheduler", "inputs": {
        "model": ["7", 0], "scheduler": "simple", "steps": args.steps, "denoise": 1.0}},
    "11": {"class_type": "RandomNoise", "inputs": {"noise_seed": args.seed}},
    "12": {"class_type": "SamplerCustomAdvanced", "inputs": {
        "noise": ["11", 0], "guider": ["8", 0], "sampler": ["9", 0],
        "sigmas": ["10", 0], "latent_image": ["6", 1]}},
    "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["2", 0]}},
    "14": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["12", 1], "vae": ["3", 0]}},
    "15": {"class_type": "CreateVideo", "inputs": {"images": ["13", 0], "fps": 24.0, "audio": ["14", 0]}},
    "16": {"class_type": "SaveVideo", "inputs": {"video": ["15", 0], "filename_prefix": args.out,
                                                 "format": "auto", "codec": "h264"}},
}

req = urllib.request.Request(BASE + "/prompt", data=json.dumps({"prompt": wf}).encode(),
                             headers={"Content-Type": "application/json"})
pid = json.load(urllib.request.urlopen(req))["prompt_id"]
print("queued:", pid, flush=True)

t0 = time.time()
while True:
    time.sleep(10)
    q = json.load(urllib.request.urlopen(BASE + "/queue", timeout=10))
    if not q.get("queue_running") and not q.get("queue_pending"):
        h = json.load(urllib.request.urlopen(f"{BASE}/history/{pid}", timeout=10))
        data = h.get(pid, {})
        print(f"DONE t={int(time.time()-t0)}s STATUS:", data.get("status", {}).get("status_str"), flush=True)
        for node_id, o in data.get("outputs", {}).items():
            for key, items in o.items():
                if isinstance(items, list):
                    for it in items:
                        if isinstance(it, dict):
                            print("OUTPUT:", it.get("filename", ""), "| subfolder:", it.get("subfolder", ""), flush=True)
        for m in data.get("status", {}).get("messages", []):
            if m[0] == "execution_error":
                print("ERR:", m[1].get("node_type"), str(m[1].get("exception_message"))[:200], flush=True)
        break
