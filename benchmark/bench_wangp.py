import argparse
import json
import subprocess
import sys
import threading
import time
from pathlib import Path

WANGP = Path(r"D:\AI\WanGP")
sys.path.insert(0, str(WANGP))

T2V_CASES = {
    1: (1001, "A ginger cat sitting on a window ledge in soft morning light, it slowly turns its head toward the camera. Fixed shot, realistic."),
    2: (1002, "Forward tracking shot through a misty forest at dawn, sun rays filtering between the trees. Cinematic."),
    3: (1003, "A woman walks down a rainy street at night, neon lights reflected on the wet ground. Cinematic, realistic."),
    4: (1004, "Waves crashing on rocks in slow motion, detailed water and foam. Realistic."),
    5: (1005, "Extreme close-up of a mechanical watch with turning gears, studio lighting. Macro, sharp."),
}


I2V_CASES = {
    1: (3001, "The woman blinks slowly and smiles slightly. Subtle natural motion, fixed camera."),
    2: (3002, "Clouds drift slowly across the sky and the tall grass sways in the wind. Fixed camera."),
    3: (3003, "The man takes a few steps toward the camera. Natural walking motion, fixed camera."),
    4: (3004, "The bird spreads its wings and takes off from the branch. Natural motion."),
    5: (3005, "Pedestrians walk on the sidewalk and cars drive along the street. Fixed camera."),
}


class Monitor(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.vram = 0
        self.stop = False

    def run(self):
        while not self.stop:
            try:
                out = subprocess.check_output(
                    ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], text=True
                )
                self.vram = max(self.vram, int(out.strip().splitlines()[0]))
            except Exception:
                pass
            time.sleep(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--cases", default="1")
    p.add_argument("--frames", type=int, default=81)
    p.add_argument("--steps", type=int, default=0)
    p.add_argument("--abort-over", type=float, default=0)
    p.add_argument("--i2v", action="store_true")
    p.add_argument("--suffix", default="")
    p.add_argument("--prompt-full", default="")
    p.add_argument("--negative", default="")
    p.add_argument("--tag", default="")
    p.add_argument("--out", default=str(Path(__file__).parent / "resultats_raw.jsonl"))
    a = p.parse_args()

    from shared.api import init

    session = init(console_output=False)
    for c in [int(x) for x in a.cases.split(",")]:
        s = session.get_default_settings(a.model)
        if a.i2v:
            seed, prompt = I2V_CASES[c]
            s.update({"image_prompt_type": "S", "image_start": [str(Path(__file__).parent / "images" / ("image%d.png" % c))]})
        else:
            seed, prompt = T2V_CASES[c]
        if a.prompt_full:
            prompt = a.prompt_full
        if a.suffix:
            prompt = prompt + " " + a.suffix
        if a.negative:
            s["negative_prompt"] = a.negative
        s.update({"prompt": prompt, "seed": seed, "resolution": "832x480", "video_length": a.frames})
        if a.steps:
            s["num_inference_steps"] = a.steps
        mon = Monitor()
        mon.start()
        t0 = time.time()
        try:
            result = session.run_task(s)
            files = [str(f) for f in result.generated_files]
            errors = [str(e) for e in result.errors]
        except Exception as ex:
            files = []
            errors = ["EXCEPTION: " + repr(ex)]
        dt = time.time() - t0
        mon.stop = True
        rec = {
            "model": a.model + a.tag,
            "prompt": prompt,
            "case": c,
            "seed": seed,
            "frames": a.frames,
            "seconds": round(dt, 1),
            "vram_max_mib": mon.vram,
            "files": files,
            "errors": errors,
        }
        print(json.dumps(rec, ensure_ascii=True))
        with open(a.out, "a", encoding="ascii") as f:
            f.write(json.dumps(rec, ensure_ascii=True) + "\n")
        if a.abort_over and dt > a.abort_over:
            print("ABORT: first case above limit")
            break
        if errors and not files:
            print("ABORT: failure without output")
            break


if __name__ == "__main__":
    main()
