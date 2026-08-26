---
name: skill-bench
description: >
  Banc de test qui évalue un ou plusieurs skills/agents de ce dépôt contre leur
  propre objectif déclaré, produit un tableau de notation comparatif, et renvoie
  ceux qui échouent vers skill-optimizer pour correction. Déclenche quand
  l'utilisateur veut "tester ce skill", "auditer les skills", "vérifier que mes
  agents produisent ce qu'il faut", "noter mes skills", "faire un banc de test",
  ou "quels skills sont à corriger". Ne fait jamais lui-même la correction —
  c'est le rôle de skill-optimizer, skill-bench se limite à détecter et noter.
---

# Skill-Bench — Banc de test des skills/agents

Détecte, ne corrige pas. `skill-bench` note un skill contre le livrable qu'il
promet de produire (pas contre une checklist générique de style), et contre la
qualité de ce livrable **pour ce qui le consomme ensuite** — un CV amélioré n'a
pas la même exigence de qualité isolé ou juste avant `cv-designer`. Quand une
cible échoue, `skill-bench` produit un `evals.json` compatible avec
`skill-optimizer` et recommande de le lancer — il ne le lance jamais lui-même
(`skill-optimizer` a ses propres portes de validation humaine, ne pas les
court-circuiter).

Un skill a aussi un coût d'utilisation (tokens, donc $) — pas seulement une
note. `skill-bench` le quantifie en Phase 5bis à partir des stats d'usage déjà
présentes dans chaque notification de sous-agent, sans appel ni calcul
supplémentaire.

Références :
- `references/rubric-guide.md` — comment construire un rubric qui juge le
  vrai objectif de la cible plutôt qu'un style générique. À lire en Phase 2.
- `references/tarifs.md` — tarifs modèles et méthode d'estimation du coût.
  À lire en Phase 5bis.

## Phase 0 — Sélection des cibles

Demander (question fermée si ambigu) : une cible précise (nom de skill ou
d'agent), une liste, ou "tout le dépôt" (scanner `agents/*.md` et
`skills/*/SKILL.md`).

Pour chaque cible, lire son contrat déclaré — jamais en deviner un :
- **Agent** (`agents/*.md`) : sections `Inputs attendus` et `Output`.
- **Skill orchestrateur** (`skills/*/SKILL.md`) : section `Fichiers de sortie`
  (ou équivalent) + les phases qui y mènent.

Noter le **type** de chaque cible (agent à contrat clair vs skill orchestrateur
interactif) — ça ne change pas le mode de test (toujours bout-en-bout, voir
Phase 2) mais ça change ce que le rubric doit vérifier : un agent est jugé sur
la conformité de son livrable unique, un skill orchestrateur sur l'ensemble de
ses livrables ET sur le respect de ses portes de validation (ex. ne pas
rédiger de contenu avant qu'une étape bloquante soit validée).

## Phase 1 — Repérer l'aval

Pour chaque cible, chercher si un autre agent/skill du dépôt consomme son
livrable — section `Passage à l'étape suivante` du fichier cible, ou table
`Étapes` du skill parent s'il y en a une. Si un consommateur existe, lire
**son** `Inputs attendus` : c'est le format réel attendu en aval, pas une
supposition. S'il n'y en a pas (cible terminale, ex. `debrief-agent`,
`fiche-seance.md`), le rubric jugera la qualité intrinsèque seulement.

## Phase 2 — Scénarios de test

Pour chaque cible, construire 2 à 3 scénarios au format
`evals/eval-template.json` (même schéma que `skill-optimizer`, avec un champ
`persona` en plus) :
- **Nominal** : cas d'usage principal, persona réaliste et complet.
- **Limite** : persona qui fournit une entrée ambiguë ou incomplète — vérifie
  que la cible demande une clarification plutôt que d'halluciner.
- **Aval** (si un consommateur a été identifié en Phase 1) : rubric qui inclut
  explicitement un critère "le livrable est directement exploitable par
  [consommateur] sans reformulation" — poids au moins égal aux autres critères,
  jamais un bonus mineur.

Consulter `references/rubric-guide.md` avant de pondérer les critères.

Sauvegarder chaque jeu dans `skill-bench/evals/<cible>-evals.json`.

## Phase 3 — Exécution (sous-agent frais par scénario)

Pour chaque scénario : dispatcher un sous-agent frais dont les instructions
sont le contenu intégral du fichier cible (`agent.md` ou `SKILL.md` + ses
références citées), plus le persona et le prompt du scénario. Consigne
explicite au sous-agent : incarner le persona pour toute question fermée que
la cible poserait, jusqu'à produire le(s) livrable(s) déclaré(s) — jamais
s'arrêter en attente d'un humain réel.

**Sandboxing obligatoire** : si la cible a accès à des outils d'écriture
(`Write`, `Edit`, ou équivalent — vérifier son frontmatter `tools`), ajouter
explicitement à la consigne : « n'utilise aucun outil pour lire ou modifier
un vrai fichier du dépôt pendant ce test ; produis ton livrable complet
uniquement comme texte de ta réponse finale ». Un incident réel l'a révélé :
sans cette consigne, un agent testé avec Write/Edit a effectivement modifié
un fichier de décision réel du dépôt en croyant traiter une vraie demande —
`skill-bench` doit rester un test isolé, jamais une action qui touche le
dépôt de la cible qu'il évalue.

Sauvegarder la sortie brute dans `skill-bench/runs/<cible>/eval-<id>/`, ainsi
que les stats d'usage renvoyées par la notification de fin d'agent
(`subagent_tokens`, `tool_uses`, `duration_ms`) dans
`skill-bench/runs/<cible>/eval-<id>/usage-execution.json` — c'est la donnée
brute et gratuite (déjà présente dans chaque notification, rien à calculer)
qui alimente le coût observé en Phase 5bis.

## Phase 4 — Jugement (sous-agent frais, distinct de l'exécution)

Pour chaque scénario : dispatcher un **autre** sous-agent frais (jamais celui
qui a produit le livrable — même logique que la porte de contrôle de
`presentation-builder`), avec pour seules instructions le rubric du scénario,
le livrable produit, et — si applicable — le contrat `Inputs attendus` du
consommateur identifié en Phase 1. Dispatcher ce sous-agent avec `model:
opus` (paramètre `model` de l'outil Agent) — un juge moins capable que ce
qu'il évalue a des angles morts (pattern LLM-judge classique) ; la Phase 3
(exécution) reste sur le modèle par défaut de la session, l'écart de qualité
n'y justifie pas le surcoût systématique.

Il remplit `skill-bench/runs/<cible>/eval-<id>/scores-eval-<id>.json`, au
format exact attendu par `skill-optimizer` (`score_obtenu` par critère avec
justification, `score_max`, `seuil_succes`). Même capture d'usage qu'en
Phase 3, sauvegardée dans `usage-jugement.json` du même dossier — le coût du
jugement fait partie du coût total de la cible, pas seulement celui de
l'exécution.

## Phase 5 — Agrégation

Réutiliser tel quel `skills/skill-optimizer/scripts/score_eval.py --aggregate
skill-bench/runs/<cible>/` pour chaque cible (ne pas réécrire cette logique).
Produit `aggregate.json` par cible avec `pct_global`, `passed`, `failed`.

## Phase 5bis — Coût observé

Un skill a un coût d'utilisation, pas seulement une note de qualité — cette
phase le quantifie pour repérer, en plus des cibles à corriger, celles qui
coûtent cher à faire tourner (candidates à un futur passage
`skill-optimizer` orienté compacité, ou à un override de modèle plus léger —
voir `TODO-model-override.md` du skill concerné s'il existe).

Pour chaque cible : sommer les `subagent_tokens` de tous les
`usage-execution.json` et `usage-jugement.json` de ses scénarios (Phase 3 +
Phase 4). Consulter `references/tarifs.md` pour le tarif mixte par modèle
(exécution = modèle par défaut de la session, jugement = `claude-opus-5`) et
calculer un coût estimé. Sauvegarder dans
`skill-bench/runs/<cible>/couts.json` :

```json
{
  "tokens_execution": 0,
  "tokens_jugement": 0,
  "tokens_total": 0,
  "cout_estime_usd": 0.0
}
```

**C'est une estimation** (tarif mixte, pas la vraie répartition
input/output — voir `references/tarifs.md`) — ne jamais la présenter comme
un coût facturé.

## Phase 6 — Tableau de notation

Compiler un tableau unique, toutes cibles confondues :

| Cible | Type | Scénarios passés | Score global | Tokens observés | Coût estimé | Verdict |
|---|---|---|---|---|---|---|
| `cv-analyst` | agent | 2/3 | 74% | 42 000 | ~0.28 $ | À corriger |
| `job-posting-writer` | agent | 3/3 | 91% | 18 500 | ~0.12 $ | Conforme |
| ... | | | | | | |

Verdict `Conforme` si `pct_global` ≥ 70 (seuil déjà utilisé par défaut dans
`score_eval.py` — cohérence avec `skill-optimizer`), sinon `À corriger`.
Préciser en note sous le tableau : « Coût estimé, pas facturé — tarif mixte
70/30 input/output, voir `references/tarifs.md` ». Présenter le tableau à
l'utilisateur.

Une cible bien notée mais chère (score ≥ 70 et coût nettement au-dessus des
autres cibles du même type) est un signal différent d'une cible mal notée —
ne pas la classer `À corriger` pour ça seul (Phase 7 reste pilotée par le
score), mais le signaler explicitement dans le résumé remis à l'utilisateur.

## Phase 7 — Retour à l'usine

Pour chaque cible `À corriger` :
1. Copier `skill-bench/evals/<cible>-evals.json` vers
   `skill-optimizer/optimization-workspace/iteration-0/` du skill concerné, et
   les `scores-eval-*.json` de la Phase 4 au même endroit — `skill-bench` sert
   alors directement de baseline (Phase 3 de `skill-optimizer`), pas besoin de
   la rejouer.
2. Recommander explicitement : « lancer `skill-optimizer` sur `<cible>` » —
   **ne jamais l'invoquer automatiquement** : ses portes de validation humaine
   (eval set à valider, micro-éditions à confirmer) doivent rester déclenchées
   par l'utilisateur, pas court-circuitées par un enchaînement automatique.

## Fichiers de sortie

```
skill-bench/
├── evals/
│   └── <cible>-evals.json
├── runs/
│   └── <cible>/
│       ├── eval-<id>/
│       │   ├── livrable produit
│       │   ├── scores-eval-<id>.json
│       │   ├── usage-execution.json
│       │   └── usage-jugement.json
│       └── couts.json
└── tableau-notation.md
```

## Notes d'orchestration

- Ne jamais tester une cible sans avoir lu son contrat déclaré en Phase 0 —
  un rubric inventé sans lire l'`Output` réel juge contre une attente
  fantasme, pas contre l'objectif du skill.
- Rejouer `skill-bench` régulièrement (pas qu'une fois) : un skill corrigé par
  `skill-optimizer` doit repasser le banc pour confirmer le score, et un
  nouveau skill ajouté au dépôt (voir `skill-architect`) devrait passer le
  banc avant sa première utilisation réelle.
- Le persona par scénario reste cohérent d'une phase à l'autre : c'est le
  sous-agent d'exécution (Phase 3) qui l'incarne, jamais le juge (Phase 4).
