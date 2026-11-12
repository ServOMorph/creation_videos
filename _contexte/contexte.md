# Contexte — creation_videos

## Objectif (immuable sauf décision explicite)
Création de vidéo avec IA locale sur ce PC (text-to-video, image-to-video)

## Stack / contraintes techniques (stable, rarement modifié)
- Matériel : RTX 4060 8 Go VRAM, 47,9 Go de RAM ; la GPU est partagée avec la session `creation_llm`.
- Frontend : WanGP (`D:\AI\WanGP`, environnement `env_uv`), piloté par son API Python `shared.api`.
- T2V : Wan 2.1 Text2video 14B (`t2v`, quanto int8), 832x480, 81 images, environ 54 min par clip.
- I2V : Wan 2.1 Image2video 480p 14B (`i2v`), retenu à titre provisoire, environ 54 min par clip.
- Images de référence : Qwen-Image 2.1 Q4_K_M via `D:\ServOMorph\ComfyUI-Qwen`.

## État actuel (réécrit intégralement à chaque /close)
Benchmark T2V (8 modèles) et I2V (1 modèle) terminés, résultats dans `benchmark/resultats.md`.
`t2v` retenu ; `i2v` provisoire. Défaut ouvert : vidéos au ralenti (corrigé en T2V sur le cas 3, pas en I2V).
Reste : seconde correction I2V, puis `run.py` (phase 5). Stack figée provisoirement.

## Décisions structurantes (append only — 10 entrées max, 5 lignes max/entrée, archiver au-delà)
- 2026-11-10 : Initialisation du protocole vibecoding.
- 2026-11-12 : Modèle T2V retenu = Wan 2.1 Text2video 14B (`t2v`), les 7 autres écartés sur la qualité ; I2V = Wan 2.1 Image2video 14B (`i2v`), provisoire. Seuil de temps relevé à 1 h 30 par clip. Détail : `benchmark/resultats.md`.
