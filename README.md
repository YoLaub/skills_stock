# 🧠 Skills & Agents — Claude Code

Dépôt public de skills et agents réutilisables pour [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

Un **skill** décrit un pipeline ou un processus complexe. Un **agent** est un spécialiste autonome qui exécute une tâche précise. Ensemble, ils permettent à Claude Code de se comporter comme une équipe de collaborateurs spécialisés sur n'importe quel projet.

---

## Table des matières

- [Catalogue](#catalogue)
- [Concepts](#concepts)
- [Structure du dépôt](#structure-du-dépôt)
- [Installation](#installation)
- [Intégration dans un projet](#intégration-dans-un-projet)
- [Personnalisation](#personnalisation)
- [Créer ses propres skills et agents](#créer-ses-propres-skills-et-agents)

---

## Catalogue

### Skills

| Skill | Description |
|-------|-------------|
| `rh-pipeline` | Pipeline RH complet multi-agents pour traiter une candidature de A à Z — analyse CV, mise en forme, email recruteur, entretiens, bilan final. |
| `cert-pipeline` | Pipeline de préparation à une certification ou titre professionnel — chargement référentiel, analyse des écarts, fiches de révision, simulation jury, bilan. |
| `brain-builder` | Crée et maintient des "cerveaux projets" sous forme de vaults Obsidian structurés (architecture 3 couches : raw / wiki / reports), inspirés de l'approche LLM Wiki. |
| `skill-optimizer` | Optimise un SKILL.md existant par micro-éditions validées (approche SkillOpt) : baseline → proposition → évaluation → commit ou revert. |
| `greenfield-tdd-okf` | Workflow répétable pour démarrer un projet greenfield en TDD avec index OKF : cadrage, plan validé, bootstrap monorepo git-flow, features en branches avec tests + E2E avant merge, rétro continue. |
| `presentation-builder` | Construit une présentation orale (soutenance, pitch, talk, démo) avec modèle assertion-preuve et design system fermé — export Marp en .pptx/PDF, schémas Mermaid et graphiques automatiques, porte de contrôle visuelle avant livraison. |
| `skill-architect` | Conçoit l'architecture d'un nouveau skill ou refactore la structure d'un skill existant — SOLID transposé aux skills, patterns (Template Method, Facade, Pipeline, Strategy), découpage par vitesse de changement, checklist de revue. |

### Agents — Pipeline RH

| Agent | Description |
|-------|-------------|
| `cv-analyst` | Analyse un CV brut pour évaluer sa compatibilité ATS, identifier les mots-clés manquants et produire une version améliorée. |
| `cv-designer` | Génère un fichier HTML visuellement original format A4, prêt à imprimer ou exporter en PDF depuis le navigateur. |
| `cv-recruiter` | Rédige l'email de candidature professionnel et génère le rapport de soumission ATS final. |
| `rh-interviewer` | Simule un entretien de motivation en mode conversationnel — pose les questions, évalue les réponses, enchaîne. |
| `tech-interviewer` | Simule un entretien technique adapté au profil et à la stack — adapte le niveau et les thèmes détectés dans le CV. |
| `debrief-agent` | Synthétise toutes les étapes du pipeline RH en un bilan complet avec note, recommandation, points forts et axes d'amélioration. |

### Agents — Pipeline Certification

| Agent | Description |
|-------|-------------|
| `cert-intake` | Collecte le nom de la certification visée, le profil du candidat et un compte rendu d'année synthétique (500 mots max). |
| `referentiel-loader` | Charge et résume le référentiel officiel depuis `docs/` ou via recherche web — produit un résumé structuré de 600 mots max. |
| `gap-analyser` | Croise le profil candidat avec les compétences du référentiel et produit une carte des écarts (maîtrisées / partielles / manquantes). |
| `exam-preparer` | Génère des fiches de révision ciblées et une banque de questions probables basées sur les écarts identifiés. |
| `cert-interviewer` | Simule un entretien jury en mode conversationnel, adapté au référentiel et aux lacunes détectées. |
| `cert-debrief` | Synthétise le pipeline certification en un bilan complet avec points forts, axes à consolider et probabilité estimée de validation. |

---

## Concepts

| | Skill | Agent |
|---|---|---|
| Fichier | `skills/[nom]/SKILL.md` | `agents/[nom].md` |
| Rôle | Orchestre un pipeline, définit les étapes et le contexte partagé | Exécute une tâche précise et produit un livrable |
| Déclenché par | Une intention générale (*"lance le pipeline X"*) | Une étape du pipeline ou un appel direct |
| Analogie | Chef de projet | Spécialiste métier |

Claude Code lit automatiquement tous les fichiers présents dans `.claude/agents/` et `.claude/skills/` au démarrage d'une session. Aucune configuration supplémentaire n'est nécessaire.

---

## Structure du dépôt

```
.
├── agents/
│   ├── rh/                          ← Pipeline RH (6 agents)
│   │   ├── cv-analyst.md
│   │   ├── cv-designer.md
│   │   ├── cv-recruiter.md
│   │   ├── rh-interviewer.md
│   │   ├── tech-interviewer.md
│   │   └── debrief-agent.md
│   ├── cert/                        ← Pipeline Certification (6 agents)
│   │   ├── cert-intake.md
│   │   ├── referentiel-loader.md
│   │   ├── gap-analyser.md
│   │   ├── exam-preparer.md
│   │   ├── cert-interviewer.md
│   │   └── cert-debrief.md
│   └── [domaine]/                   ← futur domaine
├── skills/
│   ├── rh-pipeline/
│   │   └── SKILL.md
│   ├── cert-pipeline/
│   │   └── SKILL.md
│   ├── brain-builder/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── skill-optimizer/
│   │   └── SKILL.md
│   ├── greenfield-tdd-okf/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── presentation-builder/
│   │   ├── SKILL.md
│   │   ├── design-system/
│   │   └── references/
│   └── skill-architect/
│       ├── SKILL.md
│       └── references/
└── README.md
```

---

## Installation

### Prérequis

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installé
- Un projet ouvert dans Claude Code

### Option 1 — Copie manuelle

Copier les fichiers souhaités dans le dossier `.claude/` de ton projet :

```bash
# Créer la structure si elle n'existe pas
mkdir -p mon-projet/.claude/agents mon-projet/.claude/skills

# Copier un agent
cp agents/[domaine]/nom-agent.md mon-projet/.claude/agents/

# Copier un skill complet
cp -r skills/nom-pipeline/ mon-projet/.claude/skills/
```

### Option 2 — Sous-module Git

Pour rester synchronisé avec les mises à jour du dépôt :

```bash
cd mon-projet
git submodule add https://github.com/YoLaub/skills_stock.git .claude/registry
```

Puis créer des symlinks vers les fichiers souhaités :

```bash
ln -s .claude/registry/agents/[domaine]/nom-agent.md .claude/agents/nom-agent.md
ln -s .claude/registry/skills/nom-pipeline .claude/skills/nom-pipeline
```

Mettre à jour plus tard :

```bash
git submodule update --remote
```

### Option 3 — Script curl

Pour installer rapidement un ensemble d'agents sans cloner le dépôt :

```bash
BASE="https://raw.githubusercontent.com/YoLaub/skills_stock/main"
mkdir -p .claude/agents .claude/skills/nom-pipeline

curl -s "$BASE/agents/[domaine]/nom-agent.md" -o .claude/agents/nom-agent.md
curl -s "$BASE/skills/nom-pipeline/SKILL.md"  -o .claude/skills/nom-pipeline/SKILL.md
```

---

## Intégration dans un projet

Une fois les fichiers copiés dans `.claude/`, la structure cible est :

```
mon-projet/
├── .claude/
│   ├── agents/
│   │   ├── nom-agent-1.md
│   │   └── nom-agent-2.md
│   ├── skills/
│   │   └── nom-pipeline/
│   │       └── SKILL.md
│   └── README.md          ← documenter les agents actifs dans le projet
├── src/
└── ...
```

Ouvrir Claude Code dans `mon-projet/` — les agents et skills sont immédiatement actifs.
Les déclencher naturellement dans le chat :

```
Lance le pipeline [nom]
```
```
Utilise l'agent [nom-agent] pour [tâche]
```

---

## Personnalisation

Les agents de ce dépôt sont **génériques par défaut**. Ils contiennent des placeholders à adapter au contexte du projet, signalés entre crochets :

```
[NOM_ENTREPRISE], [STACK_PRINCIPALE], [SECTEUR], [LANGUE_CIBLE]
```

### Adapter via Claude Code (recommandé)

Une fois les fichiers dans `.claude/`, demander à Claude Code de les modifier directement :

```
Adapte l'agent [nom].md pour notre contexte :
- Secteur : [secteur]
- Stack : [stack]
- Langue : [langue]
```

Claude Code édite le fichier sur disque. La modification est active immédiatement dans la session.

### Adapter manuellement dans l'éditeur

Ouvrir le fichier `.claude/agents/nom-agent.md` dans VSCode, Cursor ou tout éditeur.
Les zones à personnaliser sont regroupées dans les sections :

- `## Inputs attendus` — adapter les champs au projet
- `## Processus` — ajouter, retirer ou réordonner des étapes
- `## Output` — changer les chemins ou formats de sortie
- `## Passage à l'étape suivante` — recâbler l'ordre du pipeline si besoin

Sauvegarder suffit — Claude Code relit les fichiers à chaque session.

### Bonnes pratiques

- Committer les personnalisations avant une mise à jour depuis le dépôt (une mise à jour écrase les fichiers locaux)
- Documenter les changements dans `.claude/README.md` pour l'équipe
- Tester un agent seul avant de lancer un pipeline complet

---

## Créer ses propres skills et agents

### Structure minimale d'un agent

```markdown
---
name: nom-agent
description: >
  Ce que fait l'agent en une phrase.
  Intentions utilisateur qui doivent le déclencher : "...", "...", "...".
---

# Agent : nom-agent

## Rôle
[Description en 2-3 phrases]

## Inputs attendus
- `champ_1` : description
- `champ_2` : description

## Processus
1. Étape 1
2. Étape 2
3. ...

## Output
[Fichiers produits et/ou données retournées]

## Passage à l'étape suivante
[Optionnel — quel agent appeler ensuite]
```

Le champ `description:` dans le frontmatter YAML est le **déclencheur** : c'est ce que lit Claude Code pour décider quel agent activer. Il doit lister les formulations naturelles que l'utilisateur pourrait employer.

### Structure minimale d'un skill

```markdown
---
name: nom-pipeline
description: >
  Ce que fait ce pipeline. Intentions qui le déclenchent.
---

# Skill : nom-pipeline

## Vue d'ensemble
[Schéma ASCII du pipeline]

## Étapes

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 1 | `agent-1` | ... | ... |
| 2 | `agent-2` | ... | ... |

## Contexte partagé
[Structure JSON du contexte passé entre agents]

## Fichiers de sortie
[Liste des livrables produits]

## Usage
[Commandes d'exemple pour déclencher le pipeline]
```

### Conventions

- Un agent = un fichier Markdown autonome, sans dépendance externe
- Les chemins de sortie sont relatifs au projet (`output/` ou `[pipeline]/output/`)
- Chaque agent lit et écrit le contexte partagé explicitement
- Les agents peuvent être utilisés seuls, sans leur skill parent

---

*Issues et PR bienvenues.*
