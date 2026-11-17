# Signals — creation_videos   (MAJ 2026-11-17)

## Actions ouvertes
<!-- ≤ 20 entrées (ligne « Backlog » exclue) ; dette et findings non urgents -> _contexte/backlog.md -->
- [P2|ouvert] Vérifier si le suffixe « vitesse normale » corrige le ralenti sur d'autres cas T2V (testé uniquement sur le cas 3)
  - fait quand: au moins 2 autres cas T2V régénérés avec `--suffix` et jugés par l'utilisateur.
  - réf: `benchmark/resultats.md`.
- [P2|ouvert] Limite I2V sur scène dense non résolue (cas 5) : prompt précis + négatif n'a pas supprimé les incohérences (voiture à contresens, apparitions) ; décider si on teste une scène à peu de véhicules ou un clip plus court (49 images)
  - fait quand: décision de l'utilisateur consignée, ou limite acceptée dans `benchmark/resultats.md`.
  - réf: `benchmark/resultats.md` (section « Seconde correction du ralenti I2V »).
- [P2|ouvert] Hook `.git/hooks/pre-push` (protocole VertIA v2) non installé : l'écriture a été refusée par le classificateur du mode auto ; `pre_push_check.py` est lancé à la main avant chaque push (dernier : code 0, dépôt public, 2026-11-17)
  - fait quand: l'utilisateur installe le hook ou autorise explicitement son installation.
  - réf: `D:\ServOMorph\VertIA_v3\_orchestration\protocole.md` (section Push), `D:\ServOMorph\VertIA_v3\_orchestration\pre_push_check.py`.

## Contexte chaud
- Tâches GPU : verrou obligatoire via `vram_lock.py` (protocole VertIA v2, inscrit dans `.claude/CLAUDE.md`) ; un clip dure environ 55-60 min ; une demande de verrou peut attendre plusieurs heures. Pour une tâche hors VertIA_v3, la règle de l'utilisateur reste : valider avant d'utiliser la VRAM.
- Flux de production : `run.py` (modes `t2v`/`i2v`) documenté dans `README.md` ; `run_phase5.py` montre l'enchaînement sous verrou.
- Artefact de revue (vidéos phase 5 en tête, commentaire libre par vidéo, collection `commentaires`) : https://claude.ai/artifact/71WdwbCmL9Eu5F8tYk3s1z ; régénéré par `benchmark/build_galerie.py`, publié via `publish_files`. Toute nouvelle vidéo générée est placée en premier dans l'artefact (`.claude/memory.md`).
- Règle journal de session appliquée (`_contexte/journal_session.md`, gitignoré).

## Dernière session (2026-11-17, phase 5)
# Session du 2026-11-17

## Décisions prises
- Phase 5 validée par l'utilisateur après visionnage : un clip T2V et un clip I2V jugés « Parfait ».
- Règle mémoire : toute vidéo générée est placée en premier dans l'artefact (`.claude/memory.md`).

## Livrables produits ou modifiés
- `run_phase5.py` : enchaînement verrou GPU, T2V (3476 s), I2V (3406 s), libération du verrou.
- `benchmark/build_galerie.py` : section « Phase 5 » en tête de galerie ; artefact republié.
- `README.md` : section Utilisation (commandes T2V et I2V). `.claude/memory.md` : créé.

## Hypothèses validées / invalidées
- VALIDE : `run.py` génère une vidéo T2V et une I2V de bout en bout.
- EN ATTENTE : suffixe « vitesse normale » sur d'autres cas T2V ; limite I2V sur scène dense.

## Prochaine étape exacte
Aucune étape planifiée ; choisir parmi les actions ouvertes (suffixe T2V, scène dense I2V, hook pre-push).

## Question bloquante pour la session suivante
Aucune
