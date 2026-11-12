# Critères et jeu de test — VALIDÉS par l'utilisateur (2026-11-10)

Images I2V : générées avec Qwen-Image 2.1 (Q4_K_M GGUF) via `D:\ServOMorph\ComfyUI-Qwen`. Seuils, résolution et durée ci-dessous validés tels quels.

## Conditions communes (tous les modèles)
- Résolution : 832x480 (480p). Une passe 720p optionnelle pour le finaliste.
- Durée : ~5 s par clip (valeur exacte selon les fps natifs du modèle, notée dans les résultats).
- Seed fixe par cas (cas 1 = seed 1001, cas 2 = 1002, ...).
- 1 génération par cas et par modèle. Même prompt, même image, mêmes réglages de profil basse VRAM de WanGP.
- Navigateur sans accélération GPU (gain de VRAM documenté par WanGP).

## Mesures
- Automatiques : temps de génération, VRAM max, RAM max, échec mémoire (oui/non).
- Qualité, note 0 à 3 par critère : fidélité au prompt, cohérence temporelle, qualité du mouvement, absence d'artefacts.

## Seuils de rejet (modifiés par l'utilisateur le 2026-11-10 : la qualité prime sur le temps)
- Échec mémoire sur plus de 2 cas sur 10.
- Temps supérieur à 1 h 30 par clip de 5 s (était 15 min).

## Cas text-to-video (5)
1. Plan fixe : un chat roux assis sur un rebord de fenêtre, lumière du matin, il tourne la tête vers la caméra.
2. Mouvement de caméra : travelling avant dans une forêt brumeuse à l'aube, rayons de soleil entre les arbres.
3. Humain en action : une femme marche dans une rue pluvieuse la nuit, néons reflétés sur le sol mouillé.
4. Fluide : vagues qui se brisent sur des rochers, ralenti, eau et écume détaillées.
5. Objet mécanique : gros plan d'une montre mécanique dont les rouages tournent, éclairage studio.

## Cas image-to-video (5)
Images sources à fournir ou à générer (option : flux-2-klein déjà présent dans `D:\AI\WanGP\ckpts`), stockées dans `benchmark/images/`.
1. Portrait : clignement des yeux et léger sourire.
2. Paysage : nuages qui avancent, herbe qui bouge au vent.
3. Personnage en pied : il fait quelques pas vers la caméra.
4. Animal : un oiseau prend son envol.
5. Scène urbaine : passants et voitures en mouvement, caméra fixe.

## Décisions à confirmer
- Résolution et durée ci-dessus.
- Seuils de rejet.
- Source des 5 images I2V (fournies par vous, ou générées).
