"""First MiniMax H3 test on RTX 3050 4GB — T2V with audio via ClipProj 4B route."""
import json, time, urllib.request

BASE = "http://127.0.0.1:8188"

PROMPT = ("A majestic eagle soaring over snowy mountains at golden sunset, "
          "cinematic lighting, wings spread wide, clouds drifting past")

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
        "model": ["1", 0], "shift_video": 12.0, "shift_audio": 6.0}},
    "6": {"class_type": "MiniMaxH3ImageToVideo", "inputs": {
        "clip": ["4", 0], "vae": ["2", 0], "prompt": PROMPT,
        "width": 608, "height": 352, "length": 71}},
    "7": {"class_type": "LoraLoaderModelOnly", "inputs": {
        "model": ["5", 0], "lora_name": "minimax_h3_fl2v_turbo_4step_v1.0_768p_comfyui_bf16.safetensors",
        "strength_model": 1.0}},
    "8": {"class_type": "BasicGuider", "inputs": {"model": ["7", 0], "conditioning": ["6", 0]}},
    "9": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "res_multistep"}},
    "10": {"class_type": "BasicScheduler", "inputs": {
        "model": ["7", 0], "scheduler": "simple", "steps": 6, "denoise": 1.0}},
    "11": {"class_type": "RandomNoise", "inputs": {"noise_seed": 42}},
    "12": {"class_type": "SamplerCustomAdvanced", "inputs": {
        "noise": ["11", 0], "guider": ["8", 0], "sampler": ["9", 0],
        "sigmas": ["10", 0], "latent_image": ["6", 1]}},
    "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["2", 0]}},
    "14": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["12", 1], "vae": ["3", 0]}},
    "15": {"class_type": "CreateVideo", "inputs": {"images": ["13", 0], "fps": 24.0, "audio": ["14", 0]}},
    "16": {"class_type": "SaveVideo", "inputs": {"video": ["15", 0], "filename_prefix": "h3_test/eagle_t2v", "format": "auto", "codec": "h264"}},
}

req = urllib.request.Request(BASE + "/prompt", data=json.dumps({"prompt": wf}).encode(),
                             headers={"Content-Type": "application/json"})
pid = json.load(urllib.request.urlopen(req))["prompt_id"]
print("queued:", pid, flush=True)

t0 = time.time()
last = ""
while True:
    time.sleep(10)
    try:
        q = json.load(urllib.request.urlopen(BASE + "/queue", timeout=10))
        running = len(q.get("queue_running", []))
        pending = len(q.get("queue_pending", []))
        status = f"t={int(time.time()-t0)}s running={running} pending={pending}"
        if status != last:
            print(status, flush=True)
            last = status
        if running == 0 and pending == 0:
            h = json.load(urllib.request.urlopen(f"{BASE}/history/{pid}", timeout=10))
            if pid in h:
                st = h[pid].get("status", {})
                print("COMPLETED:", st.get("status_str"), "| msgs:",
                      [m.get('message',{}).get('g') for m in st.get('messages',[]) if m[0]=='execution_error'] or "none")
                outs = h[pid].get("outputs", {})
                for node_id, o in outs.items():
                    for key in ("images", "video", "audio", "gifs"):
                        for item in o.get(key, []):
                            print("OUTPUT:", key, "->", item.get("filename") or item.get("fullpath") or item)
                break
    except Exception as e:
        print("poll err:", str(e)[:80], flush=True)
