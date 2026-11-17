# Signals — creation_videos   (MAJ 2026-11-17)

## Actions ouvertes
<!-- ≤ 20 entrées (ligne « Backlog » exclue) ; dette et findings non urgents -> _contexte/backlog.md -->
- [P1|ouvert] Phase 5 de la roadmap : finaliser `run.py` (lancement du modèle retenu, flux T2V et I2V) et produire une vidéo de bout en bout par mode ; checkpoint `/compact` à faire avant de commencer
  - fait quand: `run.py` à la racine documenté, une vidéo T2V et une vidéo I2V générées avec lui.
  - réf: `roadmap_videos_ia_locale.md` (phase 5), `run.py` (non commité avant 308c022, contenu à relire), `benchmark/bench_wangp.py`.
- [P2|ouvert] Vérifier si le suffixe « vitesse normale » corrige le ralenti sur d'autres cas T2V (testé uniquement sur le cas 3)
  - fait quand: au moins 2 autres cas T2V régénérés avec `--suffix` et jugés par l'utilisateur.
  - réf: `benchmark/resultats.md`.
- [P2|ouvert] Limite I2V sur scène dense non résolue (cas 5) : prompt précis + négatif n'a pas supprimé les incohérences (voiture à contresens, apparitions) ; décider si on teste une scène à peu de véhicules ou un clip plus court (49 images)
  - fait quand: décision de l'utilisateur consignée, ou limite acceptée dans `benchmark/resultats.md`.
  - réf: `benchmark/resultats.md` (section « Seconde correction du ralenti I2V »).
- [P2|ouvert] Hook `.git/hooks/pre-push` (protocole VertIA v2) non installé : l'écriture a été refusée par le classificateur du mode auto ; `pre_push_check.py` est lancé à la main avant chaque push (dernier : code 0, dépôt public)
  - fait quand: l'utilisateur installe le hook ou autorise explicitement son installation.
  - réf: `D:\ServOMorph\VertIA_v3\_orchestration\protocole.md` (section Push), `D:\ServOMorph\VertIA_v3\_orchestration\pre_push_check.py`.

## Contexte chaud
- Tâches GPU : verrou obligatoire via `vram_lock.py` (protocole VertIA v2, inscrit dans `.claude/CLAUDE.md`) ; un clip I2V/T2V dure environ 55-60 min (`--long --non-interruptible`). creation_llm détient le verrou ; une demande peut attendre plusieurs heures. Pour une tâche hors VertIA_v3, la règle de l'utilisateur reste : valider avant d'utiliser la VRAM.
- Artefact de revue (images de référence, vidéos retenues, commentaire libre par vidéo en base, collection `commentaires`) : https://claude.ai/artifact/71WdwbCmL9Eu5F8tYk3s1z ; régénéré par `benchmark/build_galerie.py`, publié via `publish_files`.
- Règle journal de session appliquée (`_contexte/journal_session.md`, gitignoré).

## Dernière session (2026-11-17)
# Session du 2026-11-17

## Décisions prises
- Stack figée (phase 4 validée par l'utilisateur) : T2V `t2v` ; I2V `i2v` (480p 14B) ; limites connues : ralenti et incohérences sur scène dense.
- Règle de journal de session appliquée (CLAUDE.md, close.md, start.md), journal gitignoré.
- Artefact : notation supprimée, un commentaire libre par vidéo.
- Test I2V cas 5 clôturé après la seconde correction.

## Livrables produits ou modifiés
- `benchmark/resultats.md`, `benchmark/resultats_raw.jsonl` : seconde correction I2V consignée (3512,6 s, VRAM max 5549 Mio).
- `benchmark/build_galerie.py` : commentaires libres ; `run.py`, `run_correction_i2v.py` : scripts de lancement.
- `.claude/CLAUDE.md`, `commands/close.md`, `commands/start.md`, `.gitignore` : règle de journal.

## Hypothèses validées / invalidées
- INVALIDE : prompt précis + négatif corrige le ralenti et la marche arrière du cas 5 I2V (commentaire : incohérences persistantes).
- EN ATTENTE : cause du ralenti ; suffixe T2V sur d'autres cas.

## Prochaine étape exacte
`/compact`, puis phase 5 : finaliser `run.py` et produire une vidéo T2V et I2V.

## Question bloquante pour la session suivante
Aucune
