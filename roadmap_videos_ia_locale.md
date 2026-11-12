# Roadmap — Vidéos IA locales (text-to-video, image-to-video)

## Matériel (relevé le 2026-11-10)
- GPU : NVIDIA RTX 4060, 8 Go VRAM (nvidia-smi)
- RAM : 47,9 Go ; D: libre : ~1 488 Go
- Existant : `D:\AI\WanGP` (WanGP, commit ed94632 du 2026-07-30). Checkpoints présents dans `ckpts` : wan2.1 text2video 14B (quanto int8, 13,9 Go), wan2.2 animate 14B (int8, 16,7 Go), scail2 14B, flux-2-klein-4b. Aucun checkpoint image-to-video dédié repéré.

- Autres actifs repérés sur D: `D:\ServOMorph\ComfyUI-Qwen\models` (Qwen-Image 2.1 Q4_K_M, Wan2.2-TI2V-5B Q4_K_M GGUF, Z-Image Turbo Q4_K_M, VAE et text encoders associés) ; cache HF `D:\HuggingFaceCache\hub` (Lightricks LTX-Video, stable-video-diffusion-img2vid-xt-1-1) ; dépôt `D:\ServOMorph\LTX-Video`. Fonctionnement non testé.

## Plan d'action
1. Cadrer le critère de qualité : durée, résolution, temps de génération acceptables sur 8 Go VRAM.
2. Établir la liste restreinte de modèles à partir de recherches web (compatibilité 8 Go) et de la prise en charge par WanGP.
3. Définir un benchmark reproductible : N cas verrouillés (prompts et images fixes, seeds fixes), mêmes résolution et durée pour tous les modèles.
4. Installer et exécuter chaque candidat (y compris le modèle déjà présent sur D:), mesurer temps, VRAM max, échecs mémoire, qualité jugée.
5. Choisir le modèle principal (et éventuellement un secondaire pour la vitesse), figer la stack dans `contexte.md`.
6. Mettre en place un lancement reproductible (`run.py`) et un flux de travail documenté.

## Candidats (issus de la recherche web, non testés ici)
- Wan 2.2 TI2V-5B : text-to-video et image-to-video dans un seul modèle, annoncé tenant sur 8 Go avec offload.
- Wan 2.2 14B en GGUF + LoRA Lightx2v : annoncé possible sur 8 Go, mais les sources divergent sur le minimum.
- LTX-2.x (GGUF/distillé) : le plus léger et rapide, qualité annoncée inférieure à Wan 2.2 ; 8 Go annoncé au strict minimum, RAM élevée recommandée.
- Wan 2.1 14B int8 (déjà sur D:) : référence de départ.
- Prise en charge par WanGP (README lu le 2026-11-10) : Wan 2.1/2.2, LTX-2/2.3, LTXV, Hunyuan Video 1/1.5 listés. WanGP sert de frontend unique pour tous les candidats ; la disponibilité exacte de chaque checkpoint reste à confirmer dans l'interface.

Sources : insiderllm.com/guides/local-ai-video-generation, dev.to (Wan 2.2 en 8 Go), crepal.ai (LTX-2 VRAM), localaimaster.com (low VRAM). Chiffres des blogs non vérifiés sur cette machine.

## Phases

### Phase 1 — Cadrage et benchmark [FAIT]
- Fixer les critères (durée, résolution, temps max, notation qualité).
- Créer le jeu de test verrouillé (ex. 5 prompts T2V, 5 images I2V) dans `benchmark/`.
- Lire la documentation de WanGP pour lister les modèles pris en charge et les profils basse VRAM.
- Gate : critères et jeu de test écrits et validés par l'utilisateur.

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
  Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

### Phase 2 — Test du modèle existant (Wan 2.1 14B via WanGP) [FAIT]
- Lancer WanGP, exécuter le benchmark T2V (I2V si un checkpoint est disponible).
- Relever temps, VRAM, échecs, qualité.
- Gate : résultats consignés dans `benchmark/resultats.md`.

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
  Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

### Phase 3 — Test des candidats [FAIT]
- Télécharger et tester Wan 2.2 TI2V-5B, Wan 2.2 14B quantifié, LTX-2.x (un modèle à la fois, espace disque non limitant).
- Même benchmark, mêmes seeds.
- Gate : tableau comparatif complet dans `benchmark/resultats.md`.

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
  Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

### Phase 4 — Choix et stack figée [EN COURS]
- Choisir le modèle principal (et secondaire si pertinent) selon les résultats.
- Mettre à jour la section Stack de `contexte.md` (décision structurante).
- Gate : décision validée par l'utilisateur.

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
  Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.

### Phase 5 — Lancement et flux de production [TODO]
- Créer `run.py` à la racine (lancement du modèle retenu), documenter le flux T2V et I2V.
- Produire une vidéo de bout en bout pour chaque mode.
- Gate : une vidéo T2V et une vidéo I2V générées avec `run.py`.

**⏸ Checkpoint** — Demander à l'utilisateur de faire `/compact` avant de continuer.
  Attendre sa réponse écrite. Ne pas commencer la phase suivante sans confirmation.
