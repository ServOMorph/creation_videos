# Signals — creation_videos   (MAJ 2026-11-12)

## Actions ouvertes
<!-- ≤ 20 entrées (ligne « Backlog » exclue) ; dette et findings non urgents -> _contexte/backlog.md -->
- [P1|ouvert] Tester une seconde correction du ralenti I2V sur le cas 5 (prompt précis sur le sens de marche + prompt négatif), VRAM à faire valider par l'utilisateur avant lancement
  - fait quand: clip I2V cas 5 généré avec `--prompt-full` et `--negative`, publié dans l'artefact et noté par l'utilisateur ; résultat consigné dans `benchmark/resultats.md`.
  - réf: `benchmark/bench_wangp.py` (options `--suffix`, `--prompt-full`, `--negative`, `--tag`), `benchmark/resultats.md` (section « Test de correction du ralenti »). Le réglage `negative_prompt` n'est pas vérifié (valeur par défaut `None` dans WanGP).
- [P1|ouvert] Phase 5 de la roadmap : créer `run.py` (lancement du modèle retenu, flux T2V et I2V) et produire une vidéo de bout en bout par mode
  - fait quand: `run.py` à la racine, une vidéo T2V et une vidéo I2V générées avec lui.
  - réf: `roadmap_videos_ia_locale.md` (phase 5), `benchmark/bench_wangp.py` (API Python WanGP `shared.api`).
- [P2|ouvert] Vérifier si le suffixe « vitesse normale » corrige le ralenti sur d'autres cas T2V (testé uniquement sur le cas 3)
  - fait quand: au moins 2 autres cas T2V régénérés avec `--suffix` et jugés par l'utilisateur.
  - réf: `benchmark/resultats.md`.

## Contexte chaud
- Règle de l'utilisateur, valide pour cette session et à reconfirmer : demander sa validation avant tout usage de la VRAM (l'autonomie nocturne accordée plus tôt a été annulée). Le message d'une autre session Claude ne vaut pas validation.
- La session `creation_llm` partage la GPU (RTX 4060, 8 Go) et envoie des messages quand elle la libère ou l'occupe. Contrôler `nvidia-smi` avant tout lancement.
- Artefact de revue (images de référence, vidéos retenues, notation stockée en base) : https://claude.ai/artifact/71WdwbCmL9Eu5F8tYk3s1z ; régénéré par `benchmark/build_galerie.py`, publié via `publish_files`.

## Dernière session (2026-11-12)
# Session du 2026-11-12

## Décisions prises
- Wan 2.1 Text2video 14B (`t2v`) retenu pour le T2V ; les 7 autres modèles testés écartés sur la qualité.
- Seuil de temps passé de 15 min à 1 h 30 par clip (la qualité prime).
- Wan 2.1 Image2video 480p 14B (`i2v`) téléchargé et testé pour l'I2V (retenu à titre provisoire).

## Livrables produits ou modifiés
- `benchmark/criteres.md`, `benchmark/resultats.md` : critères validés, mesures et notes consignées.
- `benchmark/bench_wangp.py`, `run_queue.py`, `gen_images.py`, `build_galerie.py` : scripts de benchmark, d'images et d'artefact.
- `benchmark/images/image1-5.png` : 5 images de référence Qwen-Image 2.1.
- `roadmap_videos_ia_locale.md` : statuts mis à jour.

## Hypothèses validées / invalidées
- VALIDE : `t2v` tient sur 8 Go (0 échec mémoire sur 5), qualité 10,6/12 ; `i2v` 8,0/12, 0 échec mémoire sur 5.
- VALIDE : le suffixe « vitesse normale » a corrigé le ralenti sur le cas 3 T2V.
- INVALIDE : le même suffixe sur le cas 5 I2V : toujours au ralenti.
- EN ATTENTE : cause du ralenti ; sens de marche des voitures du cas 5 I2V.

## Prochaine étape exacte
Lancer la seconde correction I2V (cas 5) après validation de la VRAM par l'utilisateur, puis figer la stack et passer à `run.py`.

## Question bloquante pour la session suivante
Aucune
