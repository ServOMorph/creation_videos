# Changelog

## v1.0 — 2026-11-17

### Modifié
- Roadmap archivée (5 phases terminées) : `_contexte/archive/roadmap_videos_ia_locale.md` ; nouveau dossier `_contexte/archive/`.

## v0.3 — 2026-11-17

### Ajouté
- `run_phase5.py` (enchaînement sous verrou GPU), section Utilisation du `README.md`, `.claude/memory.md`.
- Section « Phase 5 » en tête de l'artefact de revue (`benchmark/build_galerie.py`).

### Modifié
- Phase 5 validée : un clip T2V et un clip I2V générés via `run.py`, jugés « Parfait ».

## v0.2 — 2026-11-17

### Ajouté
- Seconde correction du ralenti I2V (cas 5) consignée ; scripts `run.py`, `run_correction_i2v.py`.
- Règle de journal de session (`_contexte/journal_session.md`, gitignoré).

### Modifié
- Stack figée : `t2v` et `i2v` définitifs ; artefact de revue : commentaire libre à la place des notes.

## v0.1 — 2026-11-12

### Ajouté
- Roadmap `roadmap_videos_ia_locale.md` (5 phases) et critères de benchmark validés (`benchmark/criteres.md`).
- Scripts de benchmark WanGP (`bench_wangp.py`, `run_queue.py`), de génération d'images (`gen_images.py`) et d'artefact de revue (`build_galerie.py`).
- Résultats consignés dans `benchmark/resultats.md` : 8 modèles T2V, 1 modèle I2V, test de correction du ralenti.
- 5 images de référence (`benchmark/images/`).

### Modifié
- Seuil de temps par clip relevé à 1 h 30 ; Wan 2.1 Text2video 14B retenu pour le T2V.
