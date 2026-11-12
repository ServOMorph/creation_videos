import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
PY = r"D:\AI\WanGP\env_uv\Scripts\python.exe"
QUEUE = [
    ("ti2v_2_2", 121),
    ("ti2v_2_2_fastwan", 121),
    ("t2v_sf", 81),
    ("ltx2_22B_distilled_gguf_q4_k_m", 121),
    ("ltx2_distilled_gguf_q4_k_m", 121),
    ("hunyuan_1_5_480_t2v_lightx2v", 121),
    ("k5_lite_t2v_5s_distil", 121),
]
ABORT_OVER = 5400


def free_vram_ok():
    out = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], text=True
    )
    return int(out.strip().splitlines()[0]) < 3500


def main():
    log = ROOT / "queue_log.jsonl"
    for model, frames in QUEUE:
        while not free_vram_ok():
            time.sleep(60)
        t0 = time.time()
        cmd = [PY, "-I", str(ROOT / "bench_wangp.py"), "--model", model, "--cases", "1,2,3,4,5",
               "--frames", str(frames), "--abort-over", str(ABORT_OVER)]
        with open(ROOT / ("log_" + model + ".txt"), "w", encoding="utf-8") as lf:
            code = subprocess.call(cmd, cwd=r"D:\AI\WanGP", stdout=lf, stderr=subprocess.STDOUT)
        with open(log, "a", encoding="ascii") as f:
            f.write(json.dumps({"model": model, "exit": code, "seconds": round(time.time() - t0)}) + "\n")


if __name__ == "__main__":
    sys.exit(main())
