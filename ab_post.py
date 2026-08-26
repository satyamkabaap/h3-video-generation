"""Post-process H3 clips: CAS sharpen + side-by-side GIF previews.
Usage: python ab_post.py <clip1> <clip2> ...   (creates <clip>_cas.mp4 + previews/ab_*.gif)
"""
import sys, os, subprocess

OUT = "C:/Users/shubh/Documents/comfy/ComfyUI/output"
PREV = os.path.join(OUT, "previews")
os.makedirs(PREV, exist_ok=True)

def cas(src):
    """Contrast Adaptive Sharpen pass, re-encode h264+aac copy. ~3-5s."""
    dst = src.rsplit(".", 1)[0] + "_cas.mp4"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", src,
           "-vf", "cas=strength=0.6", "-c:v", "libx264", "-preset", "fast",
           "-crf", "18", "-c:a", "copy", dst]
    subprocess.run(cmd, check=True)
    return dst

def gif_pair(a, b, label):
    """Side-by-side GIF @10fps, 480px wide total."""
    out = os.path.join(PREV, f"ab_{label}.gif")
    vf = ("[0:v]scale=240:-1,fps=10[a];[1:v]scale=240:-1,fps=10[b];"
          "[a][b]hstack")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-i", a, "-i", b, "-filter_complex", vf,
           "-frames:v", "100", out]
    subprocess.run(cmd, check=True)
    return out

if __name__ == "__main__":
    clips = [os.path.join(OUT, p) if not os.path.isabs(p) else p for p in sys.argv[1:]]
    for c in clips:
        print("CAS:", cas(c))
    # pair first two for A/B gif
    if len(clips) >= 2:
        label = "_vs_".join(os.path.basename(c).split("_")[0:2])[:40]
        print("GIF:", gif_pair(clips[0], clips[1], label or "pair"))
