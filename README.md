# creation_videos

## Objectif
Création de vidéo avec IA locale sur ce PC (text-to-video, image-to-video).

## Stack
- RTX 4060 8 Go VRAM ; frontend WanGP (`D:\AI\WanGP`) piloté par son API Python.
- T2V : Wan 2.1 Text2video 14B. I2V : Wan 2.1 Image2video 480p 14B.
- Images de référence : Qwen-Image 2.1 via ComfyUI-Qwen.

## Structure
- `roadmap_videos_ia_locale.md` : plan en 5 phases.
- `benchmark/` : critères, scripts, images de référence, résultats (`resultats.md`).

## État actuel
Stack figée le 2026-11-17 : `t2v` (T2V) et `i2v` (I2V). Limites connues : vidéos au ralenti, incohérences en I2V sur scène dense. Reste : phase 5 (`run.py`, une vidéo par mode).
