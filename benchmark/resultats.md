# Résultats du benchmark

Conditions : 832x480, 81 images, seed fixe par cas, 1 génération par cas, WanGP via API Python (`bench_wangp.py`), profil vidéo 5 de `wgp_config.json`. Mesures brutes : `resultats_raw.jsonl`. Notes : saisies par l'utilisateur dans l'artefact le 2026-11-10 (0 à 3).

## Wan 2.1 Text2video 14B (`t2v`) — T2V

| Cas | Temps (s) | Temps (min) | VRAM max (Mio) | Échec mémoire | Fidélité | Cohérence | Mouvement | Artefacts | Total /12 |
|-----|-----------|-------------|----------------|---------------|----------|-----------|-----------|-----------|-----------|
| 1 chat | 3636,1 | 60,6 | 7844 | non | 2 | 3 | 2 | 2 | 9 |
| 2 forêt | 3264,2 | 54,4 | 5124 | non | 3 | 3 | 3 | 2 | 11 |
| 3 rue | 3277,2 | 54,6 | 5533 | non | 3 | 3 | 2 | 3 | 11 |
| 4 vagues | 3017,6 | 50,3 | 5498 | non | 3 | 2 | 3 | 3 | 11 |
| 5 montre | 3016,9 | 50,3 | 5495 | non | 3 | 3 | 2 | 3 | 11 |
| Moyenne | 3242,4 | 54,0 | - | 0/5 | 2,8 | 2,8 | 2,4 | 2,6 | 10,6 |

Verdict sur les seuils (seuil de temps passé à 1 h 30 par l'utilisateur le 2026-11-10) : échecs mémoire 0/5 ; temps moyen 54 min par clip, sous le seuil de 1 h 30 : NON REJETÉ. Qualité bonne (moyenne 10,6/12). Modèle conservé par l'utilisateur (« ce modèle me plaît bien »).

Limites : une seule génération par cas ; VRAM mesurée par nvidia-smi toutes les secondes, qui inclut les 0,9 à 1,8 Go déjà occupés par le système ; RAM max non mesurée ; I2V non testé (checkpoint `i2v` absent de `ckpts`, images de référence non générées).

## Autres modeles - T2V (mesures automatiques, run nocturne 2026-11-11)

Conditions identiques (832x480, seeds 1001-1005). Images : 121 pour tous sauf Wan 2.1 Lightning 14B (81). Notes de qualite : en attente, a saisir dans l'artefact.
Le cas 1 inclut le chargement (et le telechargement eventuel) du modele : a ne pas comparer aux cas 2 a 5.

| Modele | id WanGP | Cas 1 (s) | Cas 2-5 moyen (s) | VRAM max (Mio) | Echecs |
|---|---|---|---|---|---|
| Wan 2.2 TI2V-5B | ti2v_2_2 | 1784.7 | 854 | 4605 | 0/5 |
| Wan 2.2 TI2V-5B FastWan | ti2v_2_2_fastwan | 251.0 | 186 | 4605 | 0/5 |
| Wan 2.1 T2V Lightning 14B | t2v_sf | 1642.9 | 246 | 5142 | 0/5 |
| LTX-2 2.3 Distilled GGUF Q4_K_M 22B | ltx2_22B_distilled_gguf_q4_k_m | 3769.4 | 181 | 6410 | 0/5 |
| LTX-2 2.0 Distilled GGUF Q4_K_M 19B | ltx2_distilled_gguf_q4_k_m | 2255.4 | 99 | 6636 | 0/5 |
| Hunyuan Video 1.5 T2V 480p Lightx2v 8B | hunyuan_1_5_480_t2v_lightx2v | 2711.6 | 365 | 4719 | 0/5 |
| Kandinsky 5 Lite T2V Distilled 5s 2B | k5_lite_t2v_5s_distil | 1298.3 | 411 | 7513 | 0/5 |


## Décision (2026-11-11)
Modèle retenu par l'utilisateur pour le T2V : Wan 2.1 Text2video 14B (`t2v`), jugé meilleur que les 7 autres candidats testés. Les autres modèles sont écartés sur la qualité, selon l'utilisateur (notes détaillées non saisies pour eux).

## Wan 2.1 Image2video 480p 14B (`i2v`) — I2V (2026-11-12)

Images sources : Qwen-Image 2.1 Q4_K_M via ComfyUI-Qwen (`images/image1-5.png`, seeds 2001-2005). Clips : 81 images, seeds 3001-3005, 832x480. Le test a été interrompu après le cas 4 (fin de session) puis le cas 5 relancé seul.

| Cas | Temps (s) | Temps (min) | VRAM max (Mio) | Échec mémoire |
|-----|-----------|-------------|----------------|---------------|
| 1 portrait | 3392,0 | 56,5 | 5660 | non |
| 2 paysage | 3103,3 | 51,7 | 5558 | non |
| 3 personnage | 3097,0 | 51,6 | 5557 | non |
| 4 oiseau | 3118,1 | 52,0 | 5552 | non |
| 5 scène urbaine | 3422,6 | 57,0 | 5200 | non |
| Moyenne | 3226,6 | 53,8 | - | 0/5 | 

Sous le seuil de 1 h 30 : non rejeté. Notes de qualité : en attente (à saisir dans l'artefact).

## Notes de qualité I2V — Wan 2.1 Image2video 480p 14B (`i2v`), saisies par l'utilisateur le 2026-11-12

| Cas | Fidélité | Cohérence | Mouvement | Artefacts | Total /12 |
|-----|----------|-----------|-----------|-----------|-----------|
| 1 portrait | 3 | 2 | 2 | 2 | 9 |
| 2 paysage | 2 | 2 | 1 | 2 | 7 |
| 3 personnage | 3 | 3 | 2 | 2 | 10 |
| 4 oiseau | 3 | 1 | 3 | 2 | 9 |
| 5 scène urbaine | 2 | 2 | 1 | 0 | 5 |
| Moyenne | 2,6 | 2,0 | 1,8 | 1,6 | 8,0 |

Remarques de l'utilisateur : toutes les vidéos (T2V et I2V) sont au ralenti ; dans le cas 5 I2V, une voiture roule en marche arrière. Défaut non traité à ce stade ; cause et correction non testées.

## Notes de qualité des autres modèles (saisies dans l'artefact avant son nettoyage, moyennes calculées)

| Modèle | Cas notés | Fidélité | Cohérence | Mouvement | Artefacts | Total /12 |
|--------|-----------|----------|-----------|-----------|-----------|-----------|
| Wan 2.2 TI2V-5B | 5/5 | 1,4 | 2,0 | 0,8 | 1,6 | 5,8 |
| Wan 2.2 TI2V-5B FastWan | 5/5 | 1,6 | 1,4 | 1,2 | 2,0 | 6,2 |
| LTX-2 2.3 Distilled GGUF 22B | 1/5 (cas 1 seul) | 1 | 2 | 1 | 2 | 6 |
| Wan 2.1 T2V Lightning 14B, LTX-2 19B, Hunyuan 1.5, Kandinsky 5 Lite | non notés | - | - | - | - | - |

Référence : Wan 2.1 T2V 14B (`t2v`) = 10,6/12.

## Test de correction du ralenti (2026-11-12)

Suffixe ajouté au prompt, même seed et même image : « Cars drive forward in the direction they face. Everything moves at normal real-time speed, not slow motion. » (une génération par cas).

| Cas | Modèle | Temps (s) | VRAM max (Mio) | Verdict de l'utilisateur |
|-----|--------|-----------|----------------|--------------------------|
| 5 scène urbaine | `i2v` | 3333,6 | 5138 | encore au ralenti |
| 3 femme dans la rue | `t2v` | 3224,9 | 5121 | ralenti corrigé |

Limite : un seul cas par modèle ; le sens de circulation des voitures du cas 5 I2V n'a pas été commenté. Le suffixe ne peut pas être généralisé sans test sur d'autres cas.

## Seconde correction du ralenti I2V, cas 5 (2026-11-14)

Prompt complet réécrit (sens de circulation, allure des piétons, caméra fixe) + prompt négatif « slow motion, reversed motion, cars driving backward, static image » ; même image, seed 3005, 81 images (`i2v_vitesse2`).

| Cas | Modèle | Temps (s) | VRAM max (Mio) | Verdict de l'utilisateur |
|-----|--------|-----------|----------------|--------------------------|
| 5 scène urbaine | `i2v` | 3512,6 | 5549 | à noter |
