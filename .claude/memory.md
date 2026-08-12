# Mémoire — Intégration de pipelines dans skills_stock

## Règle d'intégration d'un nouveau pipeline

Depuis le passage en plugin Claude Code (`yls@yl-solution`, 2026-08), l'installation
est automatique : publier un skill ou un agent, c'est committer son fichier au bon
endroit. Il n'y a plus de `install.sh`, plus de `CATALOGUE`, plus de `BUNDLES` à
maintenir.

---

## Structure cible d'un pipeline (racine du dépôt, pas `.claude/`)

```
agents/
├── agent-1.md              ← à plat, PAS de sous-dossier par domaine
├── agent-2.md
└── ...
skills/
└── [nom-pipeline]/
    └── SKILL.md
```

**Piège vérifié (2026-08)** : la découverte par défaut du plugin scanne `agents/` à
plat — un fichier dans `agents/[domaine]/agent.md` n'est PAS découvert
(`claude plugin details yls@yl-solution` le confirme : 0 agent tant que les fichiers
sont nichés, 12 dès qu'ils sont remontés à la racine de `agents/`). `skills/`, lui,
attend bien un sous-dossier par skill (`skills/[nom]/SKILL.md`) — l'asymétrie est
réelle, pas une erreur de manip.

**Convention de nommage :**
- Le dossier skill porte le nom du pipeline avec suffixe `-pipeline` (`cert-pipeline`…),
  sauf quand le skill a plusieurs voix/publics distincts (ex. `agence-emploi` : voix
  candidat + voix RH) — dans ce cas le nom décrit le domaine, pas un pipeline linéaire,
  et chaque voix a sa propre référence dans `skills/[nom]/references/parcours-*.md`.
- Les agents sont nommés en kebab-case, préfixés par le domaine si nécessaire pour
  éviter une collision de nom entre pipelines (`cert-intake`, `cv-analyst`…) —
  puisqu'ils sont désormais tous au même niveau, le préfixe est ce qui évite les
  collisions, pas un sous-dossier.

---

## Checklist d'intégration

### 1. Copier les fichiers

```bash
mkdir -p skills/[nom-pipeline]
cp /source/agents/*.md agents/
cp /source/skills/[nom-pipeline]/SKILL.md skills/[nom-pipeline]/
```

### 2. Mettre à jour `README.md` (racine)

Dans la section **Catalogue**, ajouter une ligne pour le skill et une par agent.
Dans la section **Structure du dépôt**, ajouter les nouveaux fichiers dans l'arbre
(`agents/` reste une liste à plat).

### 3. Mettre à jour `.claude/README.md`

Ajouter le pipeline avec :
- Usage rapide (commande de déclenchement)
- Tableau des outputs avec `[pipeline]/output/` comme dossier cible

### 4. Valider

```bash
claude plugin validate .
claude plugin marketplace add ./           # une fois, si pas déjà fait localement
claude plugin install yls@yl-solution
claude plugin details yls@yl-solution      # vérifier le compte Skills/Agents
claude plugin uninstall yls                # nettoyer après vérif
claude plugin marketplace remove yl-solution
```

L'inventaire est le vrai test — un manifeste peut valider tout en découvrant zéro
composant (c'est exactement ce que fait un fichier mal placé).

---

## Pipelines actifs

| Pipeline | Agents | Skill |
|----------|--------|-------|
| Agence Emploi | `cv-analyst`, `cv-designer`, `cv-recruiter`, `rh-interviewer`, `tech-interviewer`, `debrief-agent`, `job-search-agent` (parcours candidat) ; `rh-needs-analyst`, `job-posting-writer`, `candidate-screener`, `interview-designer` (parcours RH) | `agence-emploi` |
| Cert Pipeline | `cert-intake`, `referentiel-loader`, `gap-analyser`, `exam-preparer`, `cert-interviewer`, `cert-debrief` | `cert-pipeline` |
| Cours Pipeline | aucun agent dédié — skill à phases séquentielles (comme `greenfield-tdd-okf`/`vitrine-locale`), invoque `presentation-builder` en Phase 6 | `cours-pipeline` |

---

## Règles de structuration des agents

Un agent `.md` suit toujours ce gabarit (frontmatter YAML obligatoire) :

```markdown
---
name: [nom-agent]
description: >
  Ce que fait l'agent.
  Intentions utilisateur qui doivent le déclencher : "...", "...".
---

# Agent : [nom-agent]

## Rôle
## Inputs attendus
## Processus
## Output
## Passage à l'étape suivante  ← optionnel
```

Le champ `description:` est le **déclencheur** lu par Claude Code. Il doit lister les formulations naturelles de l'utilisateur.

## Règles de structuration du SKILL.md

```markdown
---
name: [nom-pipeline]
description: >
  Ce que fait le pipeline. Intentions déclenchantes.
---

# [Nom] Pipeline — Skill d'orchestration

## Vue d'ensemble     ← schéma ASCII du flux
## Étapes du pipeline ← tableau # | Agent | Input | Output
## Contexte partagé  ← JSON de l'état partagé entre agents
## Comment lancer le pipeline
```
