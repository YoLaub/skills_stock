---
name: agent-optimizer
description: >
  Optimise un agent existant (agents/*.md) par micro-éditions validées, guidées
  par un corpus d'anti-patterns (mémoire fictive, quantification sans
  provenance, redondance canonique, absence d'échelle de réponse, règles en
  tension, métriques décoratives, persona-lore, description non opérante,
  absence de porte d'intake) et mesurées avant/après via skill-bench.
  Déclenche ce skill quand l'utilisateur demande : "optimise cet agent", "cet
  agent dérive / hallucine", "réduis / compresse cet agent", "améliore [nom
  d'agent]", ou quand skill-bench renvoie une cible de type agent en
  "À corriger" (sa Phase 7).
  Ne pas déclencher sur un SKILL.md (→ skill-optimizer, seul habilité à corriger
  un skill), ni pour créer un agent from scratch (→ skill-architect), ni pour
  simplement noter un agent sans le corriger (→ skill-bench seul).
---

# Agent-Optimizer

Traite un fichier `agents/*.md` comme du code soumis à un cycle mesuré :
diagnostic contre un corpus d'anti-patterns → micro-édition → mesure via
`skill-bench` → commit ou revert. Jamais de réécriture complète en un coup.

Dépend entièrement de `skill-bench` pour la mesure — ce skill ne réinvente pas
de harnais d'exécution/jugement et ne juge jamais lui-même la qualité d'une
sortie : il viendrait juste après avoir fait la modification, biais garanti.
Si `skill-bench` n'est pas installé dans ce dépôt, l'installer avant de
continuer plutôt que de bricoler une mesure maison.

---

## Phase 0 — Classification agent vs skill

Avant tout : le fichier cible est-il vraiment un agent ? Indices dans le
frontmatter : `emoji`, `color`, `vibe`, `tools`, `model` → agent. `name` +
`description` seuls → c'est un skill, rediriger vers `skill-optimizer`.

Voir `references/anti-patterns.md` §0 pour le détail. Si le classement est
ambigu, remonter la question à l'utilisateur plutôt que trancher seul.

## Phase 1 — Diagnostic contre le corpus

Lire le fichier cible en entier, puis appliquer systématiquement le corpus
dans `references/anti-patterns.md` :

1. **Test de contrefactualité (§1)** sur chaque bloc — discriminant / redondant /
   décoratif.
2. **AP-01 à AP-09** — chercher les signaux de chaque anti-pattern (mémoire
   fictive, quantification sans provenance, redondance canonique, absence
   d'échelle, règles en tension, métriques décoratives, persona-lore,
   description non opérante, absence de porte d'intake).
3. **Grille de scoring** (fin du corpus) — noter 0-2 par axe. Un total ≤10/18
   signale une réécriture de fond nécessaire avant toute compression.

Produire un diagnostic court et le présenter à l'utilisateur avant de
continuer :

```
Agent analysé : [nom]
Taille actuelle : ~[N] lignes / [N] tokens
Score grille (corpus) : [X]/18
Anti-patterns détectés : [AP-xx, AP-yy, ...] avec localisation (section/ligne)
Hypothèse principale de sous-performance : [...]
```

## Phase 2 — Baseline via skill-bench

Invoquer `skill-bench` sur ce seul agent (Phase 0 de skill-bench : cible
précise, pas "tout le dépôt"). Il produit :
- `skill-bench/evals/<cible>-evals.json`
- `skill-bench/runs/<cible>/aggregate.json` (+ détail par scénario)

`skill-bench` **écrase** `skill-bench/runs/<cible>/` à chaque exécution.
Archiver immédiatement son contenu avant de continuer :

```bash
mkdir -p agent-optimizer/agent-workspace/<slug>/bench-0/
cp -r skill-bench/runs/<cible>/* agent-optimizer/agent-workspace/<slug>/bench-0/
```

C'est ce `bench-0/aggregate.json` archivé qui sert de score de référence.
Aucune édition n'est conservée si elle ne le fait pas progresser.

## Phase 3 — Micro-éditions, dans l'ordre des passes

L'ordre n'est pas indifférent (voir corpus, "Ordre des passes") :

1. **Fond** — AP-01, AP-02, AP-09 (sorties fausses)
2. **Contrôle** — AP-04, AP-05 (sorties mal calibrées)
3. **Compression** — AP-03, AP-06, AP-07 (volume)
4. **Déclenchement** — AP-08, en dernier, sur le contenu stabilisé

Budget : 1 à 4 micro-éditions par itération. Si l'envie d'en faire plus se
présente, c'est le signal qu'il faut mieux comprendre le problème avant
d'agir — revenir au diagnostic.

Format obligatoire par micro-édition :

```
MICRO-ÉDITION #1
Anti-pattern visé : AP-0x (ou "test de contrefactualité")
Zone : [section touchée]
Type : [ajout / suppression / reformulation / remplacement]
Motivation : [quel défaut concret ça corrige, et sur quel(s) scénario(s) du bench]
---
AVANT : [texte actuel]
---
APRÈS : [texte proposé]
---
```

Présenter à l'utilisateur, attendre confirmation. **Ne jamais trancher seul**
les points listés dans le corpus ("Ce que l'optimiseur ne décide pas seul") :
capacité déclarée qui pourrait correspondre à un mécanisme externe invisible,
classement agent/skill ambigu, règle métier sans justification écrite,
frontières d'exclusion de la `description` (qui dépendent des autres agents
du parc).

Si validé :

```bash
python skills/agent-optimizer/scripts/snapshot.py snapshot --agent <chemin/vers/agent.md> \
  --workspace agent-optimizer/agent-workspace/<slug>/ --iteration <N>
```

Puis appliquer la modification via édition directe du fichier.

## Phase 4 — Validation

Relancer `skill-bench` sur le même agent, puis archiver de nouveau :

```bash
mkdir -p agent-optimizer/agent-workspace/<slug>/bench-<N>/
cp -r skill-bench/runs/<cible>/* agent-optimizer/agent-workspace/<slug>/bench-<N>/
```

```bash
python skills/agent-optimizer/scripts/compare_bench_runs.py \
  --before agent-optimizer/agent-workspace/<slug>/bench-<N-1>/aggregate.json \
  --after  agent-optimizer/agent-workspace/<slug>/bench-<N>/aggregate.json
```

Décision automatique :
- **COMMIT** — delta positif, aucune régression de scénario, et **aucun
  scénario encore en échec** après l'édition (un scénario qui reste sous son
  `seuil_succes` ne peut jamais donner un COMMIT, même à delta global positif
  — typiquement un critère bloquant toujours violé, cf. corpus AP-02)
- **DISCUSSION** — delta positif mais régression et/ou scénario(s) encore en
  échec → trancher avec l'utilisateur
- **REVERT** — delta nul ou négatif → restaurer :
  ```bash
  cp agent-optimizer/agent-workspace/<slug>/iteration-<N-1>/<nom-agent>.md <chemin/vers/agent.md>
  ```
  puis formuler une nouvelle hypothèse à partir du diagnostic, pas un deuxième
  essai à l'aveugle.

## Phase 5 — Itération

Répéter Phases 3-4 jusqu'à :
- l'utilisateur est satisfait,
- le score skill-bench atteint un plateau sur 2 itérations consécutives,
- ou tous les anti-patterns détectés en Phase 1 sont traités.

## Phase 6 — Rapport final

Résumer, dans le même esprit que le tableau "Résultat sur le cas source" du
corpus :

| | Avant | Après |
|---|---|---|
| Lignes | [N] | [N] |
| Défauts de fond (AP-01/02/09) | [N] | [N] |
| Score skill-bench | [X]% | [Y]% |
| Règles conservées telles quelles | — | [liste] |
| Règles ajoutées | — | [liste] |

---

## Fichiers de sortie

```
agent-optimizer/agent-workspace/<slug>/
├── iteration-0/<nom-agent>.md   ← snapshot avant micro-édition #1
├── bench-0/{aggregate.json, ...}  ← skill-bench archivé, baseline
├── iteration-1/{<nom-agent>.md, diff.md}
├── bench-1/{aggregate.json, decision.json, ...}
├── ...
```

`skill-bench/evals/<cible>-evals.json` et `skill-bench/runs/<cible>/` restent
la propriété de `skill-bench` — ne pas les modifier directement, ne
retoucher que via une nouvelle invocation de `skill-bench`.
