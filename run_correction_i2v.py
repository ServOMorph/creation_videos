import subprocess
import sys

LOCK = r"D:\ServOMorph\VertIA_v3\_orchestration\vram_lock.py"
PY = r"D:\AI\WanGP\env_uv\Scripts\python.exe"
BENCH = r"d:\ServOMorph\creation_videos\benchmark\bench_wangp.py"
PROMPT = (
    "Cars drive forward from left to right along the street in the direction they face, "
    "pedestrians walk on the sidewalk at a normal pace. Real-time speed, natural motion, fixed camera."
)
NEGATIVE = "slow motion, reversed motion, cars driving backward, static image"


def main():
    code = 1
    try:
        code = subprocess.call(
            [PY, "-I", BENCH, "--model", "i2v", "--i2v", "--cases", "5", "--frames", "81",
             "--prompt-full", PROMPT, "--negative", NEGATIVE, "--tag", "_vitesse2", "--abort-over", "5400"],
            cwd=r"D:\AI\WanGP",
        )
    finally:
        rel = subprocess.call([sys.executable, LOCK, "release", "creation_videos"])
        if rel == 5:
            print("RELEASE CODE 5: VRAM non liberee")
    return code


if __name__ == "__main__":
    sys.exit(main())
