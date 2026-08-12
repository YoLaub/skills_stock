---
name: cours-pipeline
description: >
  Construit une séance de cours complète à partir d'un thème : compétences visées
  définies avant tout contenu, exploration des bases, application ludique alignée sur
  ces compétences, vérification des acquis, support de présentation (via
  presentation-builder) et fiche de séance récapitulative pour le prof. Déclenche
  quand l'utilisateur veut "préparer un cours", "créer une séance sur [thème]",
  "automatiser ma préparation de cours", "faire un cours ludique sur [thème]", ou
  mentionne un cours à donner avec une date proche.
---

# Cours Pipeline — Skill d'orchestration

Une séance de cours, du thème brut à la fiche que le prof a sous les yeux le jour J.
Principe directeur : les compétences visées sont figées **avant** d'écrire le moindre
contenu — sinon le contenu, l'activité et l'évaluation dérivent chacun dans leur coin
et rien ne garantit que l'élève ressort avec ce qui était prévu (pédagogie par
objectifs / backward design).

## Vue d'ensemble

```
[Thème] → Phase 1 Cadrage → Phase 2 Compétences visées
                                        ↓
                    Phase 3 Bases  →  Phase 4 Application ludique
                                        ↓
                              Phase 5 Vérification des acquis
                                        ↓
                    Phase 6 Support (presentation-builder)
                                        ↓
                              Phase 7 Fiche de séance
```

Références (à lire au moment indiqué, pas avant) :
- `references/verbes-competences.md` — verbes d'action par niveau (taxonomie de
  Bloom, en français) pour formuler des compétences vérifiables. Lire en Phase 2.
- `references/activites-ludiques.md` — catalogue de formats d'application ludique par
  contrainte (durée, taille de groupe, matériel dispo). Lire en Phase 4.

## Phase 1 — Cadrage (question ouverte)

Une question ouverte pour recueillir : thème du cours, public (niveau scolaire ou
type de formation, âge/profil, taille du groupe), durée de la séance, contraintes
matérielles (salle, vidéoprojecteur, accès numérique élèves), prérequis réels des
élèves (pas supposés — demander), référentiel ou programme à respecter s'il y en a
un (mentionner son nom, ne jamais l'inventer). Écrire/mettre à jour ces infos comme
source de vérité pour la suite.

## Phase 2 — Compétences visées (BLOQUANT)

Avant toute ligne de contenu : formuler 2 à 4 compétences opérationnelles (pas plus —
au-delà, aucune séance courte ne les couvre sérieusement). Consulter
`references/verbes-competences.md` pour choisir des verbes vérifiables ("être capable
de calculer/identifier/produire/comparer...") plutôt que des verbes flous ("comprendre",
"savoir" — à bannir seuls, sans critère observable).

Chaque compétence doit être vérifiable par une observation ou une production concrète
de l'élève — si aucune activité ni évaluation ne peut la vérifier, elle est trop vague,
la reformuler avant de continuer.

Faire valider cette liste par l'utilisateur (AskUserQuestion fermé : valider / ajuster)
avant la Phase 3. **Rien n'est rédigé avant cette validation.**

## Phase 3 — Exploration des bases

Rédiger le contenu théorique structuré, du plus simple au plus complexe, uniquement ce
qui sert directement une compétence de la Phase 2 (pas de contenu "pour la culture
générale" qui gonfle la séance sans être vérifié ensuite). Exemples ancrés dans
l'univers du public visé (âge, secteur, références culturelles pertinentes).

Si le sujet est technique et évolutif (outil, techno, actualité), vérifier par
recherche web que le contenu est à jour plutôt que de supposer un état figé.

## Phase 4 — Application ludique

Consulter `references/activites-ludiques.md` pour choisir un format adapté à la durée
et à la taille du groupe. L'activité doit mobiliser **chaque** compétence de la Phase
2 de façon identifiable (pas une activité générique plaquée après coup) — si une
compétence n'est mobilisée par aucun moment de l'activité, soit l'activité est
incomplète, soit la compétence n'était pas la bonne.

Produire une fiche d'activité autonome et imprimable, séparée du support de
présentation : règles, matériel, durée, consignes exactes à donner à l'oral, variante
plus simple et variante plus difficile si le groupe est hétérogène.

## Phase 5 — Vérification des acquis

Produire une évaluation courte (formative — non notée — par défaut, sauf si
l'utilisateur précise un cadre sommatif noté), alignée **point par point** sur les
compétences de la Phase 2 : une question ou un item d'observation par compétence,
jamais un quiz générique sur le thème. C'est ce qui vérifie concrètement que l'élève
ressort avec ce qui était prévu — sans cette étape, "les compétences prévues" restent
une intention non vérifiée.

## Phase 6 — Support de présentation (presentation-builder)

Invoquer le skill `presentation-builder` pour produire le deck de la partie Phase 3
(et les consignes de l'activité Phase 4 si elles gagnent à être projetées). Dériver
son intake (étape 1 de `presentation-builder`) directement des Phases 1-2 de ce
skill plutôt que de le redemander :
- **Public** : le public défini en Phase 1.
- **Objectif** : retenir (les bases) + décider/pratiquer si le deck couvre aussi les
  consignes de l'activité.
- **Durée** : durée de la séance (Phase 1) moins le temps réservé à l'activité
  ludique et à l'évaluation.
- **Contexte** : salle projetée (Phase 1, sauf indication contraire).
- **Matériau source** : le contenu rédigé en Phase 3 (et les consignes de Phase 4 si
  concerné) — jamais reformulé à la volée sans passer par l'intake du skill.
- **Identité visuelle** : couleur/ton à demander si non fournie — ne jamais
  emprunter une charte d'établissement sans validation.

Le reste du déroulé (storyboard, visuels, notes orateur, assemblage, porte de
contrôle) suit intégralement `presentation-builder`, sans le raccourcir.

## Phase 7 — Fiche de séance

Produire le document que le prof a sous les yeux le jour du cours : déroulé minuté
(accroche → bases → activité → vérification → clôture), matériel nécessaire, liens
vers le deck et la fiche d'activité. Un seul document, lisible en une passe avant
d'entrer en salle.

## Fichiers de sortie

Tous dans `cours-pipeline/output/` (le deck lui-même suit la structure de travail de
`presentation-builder`, référencée depuis la fiche de séance) :
- `output/competences-visees.md`
- `output/contenu-bases.md`
- `output/activite-ludique.md`
- `output/evaluation.md`
- `output/fiche-seance.md`

## Notes d'orchestration

- Séance courte (< 1h) : ne pas viser 4 compétences, 2 suffisent — mieux vaut 2
  compétences réellement vérifiées que 4 survolées.
- Si l'utilisateur donne un référentiel officiel à respecter (programme, RNCP, socle
  commun...), les compétences de la Phase 2 doivent s'y rattacher explicitement, pas
  être reformulées librement à côté.
- Une séance peut être relancée à une phase donnée sans repartir de zéro, en
  fournissant le contenu déjà validé des phases précédentes.
