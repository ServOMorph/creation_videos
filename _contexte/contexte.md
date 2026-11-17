# Contexte — creation_videos

## Objectif (immuable sauf décision explicite)
Création de vidéo avec IA locale sur ce PC (text-to-video, image-to-video)

## Stack / contraintes techniques (stable, rarement modifié)
- Matériel : RTX 4060 8 Go VRAM, 47,9 Go de RAM ; la GPU est partagée avec la session `creation_llm`.
- Frontend : WanGP (`D:\AI\WanGP`, environnement `env_uv`), piloté par son API Python `shared.api`.
- T2V : Wan 2.1 Text2video 14B (`t2v`, quanto int8), 832x480, 81 images, environ 54 min par clip.
- I2V : Wan 2.1 Image2video 480p 14B (`i2v`), retenu, environ 55-60 min par clip.
- Images de référence : Qwen-Image 2.1 Q4_K_M via `D:\ServOMorph\ComfyUI-Qwen`.

## État actuel (réécrit intégralement à chaque /close)
Phase 4 validée le 2026-11-17 : stack figée (`t2v`, `i2v`), résultats dans `benchmark/resultats.md`.
Limites connues : vidéos au ralenti (corrigé en T2V sur le cas 3 seulement) ; I2V incohérent sur scène dense (cas 5).
Reste : phase 5 (`run.py`, une vidéo T2V et une I2V). GPU sous verrou `vram_lock.py` (protocole VertIA v2).

## Décisions structurantes (append only — 10 entrées max, 5 lignes max/entrée, archiver au-delà)
- 2026-11-10 : Initialisation du protocole vibecoding.
- 2026-11-12 : Modèle T2V retenu = Wan 2.1 Text2video 14B (`t2v`), les 7 autres écartés sur la qualité ; I2V = Wan 2.1 Image2video 14B (`i2v`), provisoire. Seuil de temps relevé à 1 h 30 par clip. Détail : `benchmark/resultats.md`.
- 2026-11-17 : Stack validée par l'utilisateur : `t2v` (T2V) et `i2v` (I2V) définitifs ; ralenti et incohérences sur scène dense consignés comme limites. Détail : `benchmark/resultats.md`.
