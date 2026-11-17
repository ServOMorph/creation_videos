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

## Utilisation
Environnement : `D:\AI\WanGP\env_uv\Scripts\python.exe -I run.py` depuis `D:\AI\WanGP`. Durée : environ 55-60 min par clip (832x480, 81 images).
- T2V : `run.py t2v --prompt "<texte anglais>" --seed N [--negative "<texte>"]`
- I2V : `run.py i2v --prompt "<texte anglais>" --seed N --image <chemin.png> [--negative "<texte>"]`
- Sortie : chemin du fichier mp4 imprimé, écrit dans `D:\AI\WanGP\outputs\`.
- Conseil : ajouter « real-time speed, natural motion » au prompt pour limiter le ralenti.
- GPU partagée : `run_phase5.py` montre l'enchaînement avec verrou `vram_lock.py` (acquire, génération, release).

## État actuel
Stack figée le 2026-11-17 : `t2v` (T2V) et `i2v` (I2V). Limites connues : vidéos au ralenti, incohérences en I2V sur scène dense. Phase 5 validée le 2026-11-17 : un clip T2V et un clip I2V générés via `run.py`, jugés « Parfait ». Toutes les phases de la roadmap sont terminées.
