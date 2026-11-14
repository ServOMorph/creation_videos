import argparse
import sys
from pathlib import Path

WANGP = Path(r"D:\AI\WanGP")
RESOLUTION = "832x480"
FRAMES = 81
MODEL_IDS = {"t2v": "t2v", "i2v": "i2v"}


class VideoService:
    def __init__(self):
        self.session = None

    def load(self):
        sys.path.insert(0, str(WANGP))
        from shared.api import init
        self.session = init(console_output=False)

    def health(self):
        return {
            "loaded": self.session is not None,
            "models": sorted(MODEL_IDS),
            "resolution": RESOLUTION,
            "frames": FRAMES,
        }

    def generate(self, mode, prompt, seed, image=None, negative=""):
        if self.session is None:
            self.load()
        if mode not in MODEL_IDS:
            raise ValueError("mode inconnu : " + mode)
        s = self.session.get_default_settings(MODEL_IDS[mode])
        if mode == "i2v":
            if not image:
                raise ValueError("image requise en i2v")
            s.update({"image_prompt_type": "S", "image_start": [str(Path(image).resolve())]})
        if negative:
            s["negative_prompt"] = negative
        s.update({"prompt": prompt, "seed": seed, "resolution": RESOLUTION, "video_length": FRAMES})
        result = self.session.run_task(s)
        files = [str(f) for f in result.generated_files]
        if not files:
            raise RuntimeError("aucune sortie : " + "; ".join(str(e) for e in result.errors))
        return files

    def free(self):
        self.session = None

    def stop(self):
        self.free()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=sorted(MODEL_IDS))
    p.add_argument("--prompt", required=True)
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--image", default="")
    p.add_argument("--negative", default="")
    a = p.parse_args()

    service = VideoService()
    for f in service.generate(a.mode, a.prompt, a.seed, image=a.image or None, negative=a.negative):
        print(f)
    service.stop()


if __name__ == "__main__":
    main()
