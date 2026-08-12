---
name: agence-emploi
description: >
  Mini agence pour l'emploi, à deux entrées — candidat ou RH — inspirée du
  fonctionnement de France Travail côté offre et demande. Demande toujours
  la voix en premier. Côté candidat : analyse de CV, mise en forme,
  simulation d'entretiens RH/technique, bilan, recherche d'offres réelles.
  Côté RH : cadrage du besoin de recrutement, rédaction d'annonce, analyse
  comparative d'une série de candidats, préparation d'une grille
  d'entretien. Déclencher quand l'utilisateur mentionne : analyser un CV,
  préparer une candidature, simuler un entretien, chercher un poste,
  recruter, définir un besoin de recrutement, rédiger une offre d'emploi,
  comparer des candidats, ou "lancer l'agence emploi".
---

# Agence Emploi — Skill d'orchestration

Deux parcours partageant la même logique de pipeline (chaque agent produit
un livrable qui alimente le suivant) mais des publics et des objectifs
opposés : le candidat cherche à être choisi, le RH cherche à choisir.

## Phase 0 — Choix de la voix (toujours, avant toute autre action)

Poser une question fermée (AskUserQuestion) : **candidat** (chercher un
poste, préparer une candidature, s'entraîner aux entretiens) ou **RH**
(recruter — cadrer un besoin, rédiger une annonce, analyser des
candidatures, préparer un entretien) ? Ne jamais deviner : si l'utilisateur
l'a déjà dit dans son message initial ("j'ai un entretien la semaine
prochaine" → candidat ; "je dois recruter un dev" → RH), sauter la
question et confirmer le choix en une phrase.

**Si candidat** → dérouler `references/parcours-candidat.md`.
**Si RH** → dérouler `references/parcours-rh.md`.

Les deux parcours peuvent tourner sur le même projet sans interférence :
chacun écrit dans son propre sous-dossier de contexte (voir chaque
référence), rien n'est partagé entre les deux voix par défaut.

## Notes d'orchestration communes aux deux parcours

- Chaque agent est autonome et peut être relancé indépendamment ou appelé
  seul, hors pipeline.
- Si une étape échoue, reprendre avec les données de contexte existantes
  plutôt que de tout redémarrer.
- Un agent qui simule une conversation (entretien candidat, galop d'essai
  RH) le fait en 4 à 6 échanges, pas plus, pour rester exploitable.
- Tous les livrables vont dans `agence-emploi/output/` (fichiers préfixés
  par le parcours si les deux tournent sur le même projet — voir chaque
  référence pour le détail).
