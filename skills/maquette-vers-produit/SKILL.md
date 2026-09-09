---
name: maquette-vers-produit
description: >
  Porter une maquette (doc Claude design, Figma, HTML exporté) dans un produit qui
  EXISTE DÉJÀ, exhaustivement : inventaire écran par écran, extraction de toute la
  logique, vérification du câblage backend à trois niveaux, backlog de specs, puis
  livraison jusqu'à reproduire fonctionnellement la maquette. Déclenche quand
  l'utilisateur dit : "reprends cette maquette", "porte ce design", "extrais les specs
  de la maquette", "on est encore loin du design", "quelles routes backend manquent",
  "audite l'écart avec la maquette", "refonte du design", "il faut rédiger des specs
  pour le back". Ne pas confondre avec greenfield-bootstrap (amorcer un produit NEUF sur
  un dépôt vierge) ni avec tdd-backlog-run / tdd-feature-okf, à qui ce skill-ci délègue
  l'implémentation en phase 4, ni avec le skill figma (accéder au contenu d'un fichier
  Figma — ici la maquette est supposée déjà lisible). Sur un dépôt vierge avec une maquette en main, seule la phase
  d'inventaire s'applique : elle alimente le cadrage du projet, et l'audit d'écart
  attend qu'il y ait du code.
---

# Maquette → produit

Méthode éprouvée sur la refonte LOAR (2026-09) : 27 écrans maquettés, 18 specs backend
manquantes trouvées, 13 écrans codés mais inatteignables.

**Premier principe : l'exhaustivité ne se constate pas, elle s'écrit.** Une revue « à
l'œil » sous-compte toujours — sur LOAR, 5 écrans morts trouvés à la main contre 13 par
un parcours de graphe. Chaque phase produit un fichier de cases à cocher ; « j'ai tout
vérifié » se dit à la dernière case, et aucun compte ne s'annonce sans relire le fichier.

**Second principe, issu d'un reproche réel : un trou backend se signale, il ne se
contourne pas.** Adapter l'écran à ce que le back sait déjà faire produit une v0.1
plausible et fausse. Une case sans donnée derrière est une spec à rédiger, pas une
fonctionnalité à raboter.

Références (à lire au moment indiqué, pas avant) :
- `references/phase-1-inventaire.md` — protocole d'inventaire et d'extraction. Phase 1.
- `references/phase-2-cablage.md` — les trois niveaux de vérification backend. Phase 2.
- `references/phase-3-backlog.md` — format des issues de spec, arbitrages. Phase 3.
- `references/gardes-de-depot.md` — catalogue des tests-gardes à installer. Phases 1 et 5.
- `references/pieges.md` — pièges connus. Lire en phase 1, enrichir dès qu'un mord.

## Porte d'entrée — le produit existe-t-il ?

Ce skill ne porte pas une maquette dans le vide : **il mesure un écart** entre une
maquette et une implémentation. Trancher cette question avant toute chose, parce qu'elle
décide quelles phases s'appliquent.

### Branche A — le produit existe (refonte, portage, « on est loin du design »)

Cas nominal : les phases 0 à 5 s'enchaînent telles qu'écrites. Vérifier d'abord trois
préconditions, et le dire si l'une manque plutôt que de démarrer quand même :
l'application se lance sur la plateforme cible, une suite de tests existe et passe, le
backend est joignable. Sans elles, la phase 2 ne peut rien vérifier et la phase 5 ne peut
rien regarder.

### Branche B — le produit n'existe pas encore (maquette en main, dépôt vierge)

**Seule la phase 1 s'applique.** La phase 0 n'a pas de coque à réparer, la phase 2
répondrait « non » à ses trois niveaux sur chaque ligne, la phase 5 n'a pas d'écran à
regarder. Les lancer produirait des fichiers vides qui ressemblent à du travail fait.

Quatre règles propres à cette branche :

- **L'extraction ne couvre que les écrans du périmètre.** Si un cadrage existe (cahier
  des charges, CLAUDE.md), c'est lui qui dit lesquels ; extraire les six questions sur un
  écran que le périmètre coupe est du travail jeté.
- **La garde d'accessibilité est reportée**, pas oubliée : il n'y a pas encore de graphe
  de navigation à parcourir. Elle s'installe au premier retour en phase 5.
- **Aucune issue n'est ouverte ici.** Le fichier d'extraction est une *entrée* du cadrage
  du projet, pas un backlog concurrent. Deux backlogs pour un produit, et plus personne
  ne sait lequel fait foi.
- **Le vocabulaire part en premier.** Les mots exacts de la maquette nomment le code dès
  le premier commit ; les renommer après coup ne se fait jamais.

Puis passer la main au bootstrap du projet, en lui donnant le fichier d'extraction comme
matière de cadrage — le skill `greenfield-bootstrap` s'il est disponible, sinon la
méthode de démarrage du dépôt. Revenir aux **phases 2 et 5** quand il y a du code et un
backend à auditer : c'est là que ce skill reprend sa valeur.

Un cadrage déjà écrit rend le cadrage documenté du bootstrap largement redondant : ne pas
réécrire en cinq documents ce qu'un cahier des charges validé dit déjà.

## Phase 0 — La coque, avant les écrans

1. Nommer la source de vérité et **ouvrir le bon fichier** : un export contient souvent
   un rendu bundlé illisible à côté du source lisible. Écrire dans CLAUDE.md lequel fait
   foi, et pour quels thèmes (jour / nuit).
2. Corriger d'abord ce que TOUS les écrans héritent : zone sûre et insets, gouttière
   latérale, échelle typographique, barre de navigation. Sur LOAR, « les écrans manquent
   de padding » était **un** défaut de coque, pas 27 défauts d'écran. Auditer au-dessus
   d'une coque cassée fabrique un ticket par écran pour une cause unique : ne pas
   commencer la phase 1 avant qu'elle tienne.

## Phase 1 — Inventaire exhaustif (`references/phase-1-inventaire.md`)

Lister TOUS les écrans et blocs de la maquette dans un fichier de cases à cocher, puis,
écran par écran : extraire la logique, cocher, relire la liste. Installer au passage les
gardes de `references/gardes-de-depot.md`, à commencer par l'accessibilité des écrans :
un écran codé et testé peut être injoignable, et seul un parcours de graphe le voit.

## Phase 2 — Câblage backend (`references/phase-2-cablage.md`)

Pour chaque donnée affichée, répondre aux TROIS questions : la route existe-t-elle, le
client l'appelle-t-il, la réponse porte-t-elle vraiment le champ ? S'arrêter à la
première, c'est livrer à moitié. Chercher le point d'extension dormant avant de modéliser
du neuf.

## Phase 3 — Backlog de specs (`references/phase-3-backlog.md`)

Une issue par écart, avec la citation de la maquette qui la motive et son critère
d'acceptation. La maquette gagne sur le vocabulaire. Un conflit entre la maquette et un
document de cadrage existant **remonte à l'utilisateur** : ce n'est pas un arbitrage de
développeur.

## Phase 4 — Livraison

Déléguer la boucle d'implémentation : `tdd-backlog-run` pour dérouler le lot d'issues de
la phase 3, `tdd-feature-okf` pour un écart isolé (TDD, service unique consommé par l'UI
et par les interfaces machine, E2E réel, fiche OKF, rétro) — ce skill-ci n'en redéfinit
pas les étapes. Trois points propres au portage : une PR par spec, mergée sans traîner ;
les issues se ferment à la main quand les PR visent une autre branche que la branche par
défaut ; une suite se lit au couple (passés, **skippés**).

## Phase 5 — Revue visuelle

Faire tourner l'app sur la plateforme cible et regarder : un moteur de rendu de test ne
met pas en page, et les branches propres à une plateforme lui sont invisibles. Chaque
défaut trouvé ici devient un garde (`references/gardes-de-depot.md`), sinon il revient.

## Évolution de ce skill

Un piège rencontré → `references/pieges.md` (append-only, daté). Un nouveau garde →
`references/gardes-de-depot.md`. Un format qui change → le fichier de phase concerné. Ne
modifier ce SKILL.md **que si la méthode elle-même change**.
