import subprocess
import sys
import time
from pathlib import Path

LOCK = r"D:\ServOMorph\VertIA_v3\_orchestration\vram_lock.py"
PY = r"D:\AI\WanGP\env_uv\Scripts\python.exe"
RUN = r"d:\ServOMorph\creation_videos\run.py"
IMAGE = r"d:\ServOMorph\creation_videos\benchmark\images\image1.png"
OUT = Path(r"d:\ServOMorph\creation_videos\phase5_sortie.txt")

T2V_PROMPT = (
    "A fishing boat sails across a calm bay at sunrise, gentle waves, seagulls flying, "
    "real-time speed, natural motion, steady camera."
)
I2V_PROMPT = "The scene comes to life with natural motion at normal speed, steady camera."
NEGATIVE = "slow motion, static image, distorted, blurry"


def run(args):
    t = time.time()
    p = subprocess.run([PY, "-I", RUN] + args, cwd=r"D:\AI\WanGP", capture_output=True, text=True)
    with OUT.open("a", encoding="utf-8") as f:
        f.write("ARGS %s\nCODE %d\nDUREE %.0f s\n%s\n%s\n" % (args[0], p.returncode, time.time() - t, p.stdout, p.stderr[-2000:]))
    return p.returncode


def main():
    code = subprocess.call([sys.executable, LOCK, "acquire", "creation_videos", "--gb", "7", "--minutes", "135",
                            "--long", "--note", "phase 5 : T2V puis I2V", "--wait", "--timeout", "14400"])
    if code != 0:
        print("verrou non obtenu, code", code)
        return code
    try:
        run(["t2v", "--prompt", T2V_PROMPT, "--seed", "1", "--negative", NEGATIVE])
        run(["i2v", "--prompt", I2V_PROMPT, "--seed", "1", "--image", IMAGE, "--negative", NEGATIVE])
    finally:
        rel = subprocess.call([sys.executable, LOCK, "release", "creation_videos"])
        if rel == 5:
            print("RELEASE CODE 5: VRAM non liberee")
    return 0


if __name__ == "__main__":
    sys.exit(main())
