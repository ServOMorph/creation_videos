import json
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

COMFY = Path(r"D:\ServOMorph\ComfyUI-Qwen")
PY = COMFY / ".venv" / "Scripts" / "python.exe"
PORT = 8189
OUT = Path(__file__).parent / "images"

PROMPTS = {
    1: (2001, "Close-up portrait photo of a young woman with auburn hair, soft natural window light, neutral calm expression, eyes open looking at the camera, realistic, sharp details."),
    2: (2002, "Wide landscape photo of a green meadow with tall grass under a blue sky with large white clouds, distant hills, golden hour light, realistic."),
    3: (2003, "Full-body photo of a man in a dark jacket standing on an empty city sidewalk, facing the camera, centered, daylight, realistic."),
    4: (2004, "Photo of a small bird perched on a tree branch, wings folded, blurred green background, soft morning light, realistic, sharp."),
    5: (2005, "Photo of a busy city street with pedestrians on the sidewalk and cars on the road, buildings on both sides, daytime, fixed camera view, realistic."),
}


def graph(prompt, seed, prefix):
    return {
        "1": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": "qwen-image-2.1-Q4_K_M.gguf"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_8b_bf16.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "4": {"class_type": "TextEncodeQwenImage21", "inputs": {"clip": ["2", 0], "prompt": prompt, "negative_prompt": "", "resolution": 1024}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 832, "height": 480, "batch_size": 1}},
        "6": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["4", 0], "negative": ["4", 1], "latent_image": ["5", 0], "seed": seed, "steps": 25, "cfg": 1, "sampler_name": "euler", "scheduler": "simple", "denoise": 1}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["3", 0]}},
        "8": {"class_type": "SaveImage", "inputs": {"images": ["7", 0], "filename_prefix": prefix}},
    }


def call(path, data=None):
    req = urllib.request.Request("http://127.0.0.1:%d%s" % (PORT, path), data=json.dumps(data).encode() if data else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def main():
    OUT.mkdir(exist_ok=True)
    log = open(Path(__file__).parent / "log_gen_images.txt", "w", encoding="utf-8")
    srv = subprocess.Popen([str(PY), "main.py", "--port", str(PORT), "--disable-auto-launch"], cwd=str(COMFY), stdout=log, stderr=subprocess.STDOUT)
    try:
        for _ in range(180):
            try:
                call("/system_stats")
                break
            except Exception:
                time.sleep(2)
        else:
            sys.exit("ComfyUI ne repond pas")
        for n, (seed, prompt) in PROMPTS.items():
            prefix = "bench_i2v_%d" % n
            pid = call("/prompt", {"prompt": graph(prompt, seed, prefix)})["prompt_id"]
            while True:
                h = call("/history/" + pid)
                if pid in h:
                    break
                time.sleep(3)
            imgs = h[pid]["outputs"]["8"]["images"]
            src = COMFY / "output" / imgs[0].get("subfolder", "") / imgs[0]["filename"]
            shutil.copy2(src, OUT / ("image%d.png" % n))
            print("image", n, "ok")
    finally:
        srv.terminate()


if __name__ == "__main__":
    main()
