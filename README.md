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
| `archi-scanner` | Scanner d'architecture progressif et générique — indexe un codebase par étapes (stack, routes, controllers, services, entités) sans saturer le contexte, et produit un INDEX réutilisable. Prérequis d'`archi-diagrams`. |
| `archi-diagrams` | Génère des diagrammes Mermaid à la demande depuis l'INDEX produit par `archi-scanner` — classes, architecture, MCD, séquence, cas d'utilisation. |
| `rh-pipeline` | Pipeline RH complet multi-agents pour traiter une candidature de A à Z — analyse CV, mise en forme, email recruteur, entretiens, bilan final. |
| `cert-pipeline` | Pipeline de préparation à une certification ou titre professionnel — chargement référentiel, analyse des écarts, fiches de révision, simulation jury, bilan. |
| `brain-builder` | Crée et maintient des "cerveaux projets" sous forme de vaults Obsidian structurés (architecture 3 couches : raw / wiki / reports), inspirés de l'approche LLM Wiki. |
| `skill-optimizer` | Optimise un SKILL.md existant par micro-éditions validées (approche SkillOpt) : baseline → proposition → évaluation → commit ou revert. |
| `greenfield-tdd-okf` | Workflow répétable pour démarrer un projet greenfield en TDD avec index OKF, en deux modes choisis en Phase 0 — **viber** (cadrage minimal, direct au bootstrap git-flow) ou **coder** (cadrage documenté en 5 fichiers `docs/`, Epics + Issues GitHub, TDD via GitHub Flow). |
| `presentation-builder` | Construit une présentation orale (soutenance, pitch, talk, démo) avec modèle assertion-preuve et design system fermé — export Marp en .pptx/PDF, schémas Mermaid et graphiques automatiques, porte de contrôle visuelle avant livraison. |
| `skill-architect` | Conçoit l'architecture d'un nouveau skill ou refactore la structure d'un skill existant — SOLID transposé aux skills, patterns (Template Method, Facade, Pipeline, Strategy), découpage par vitesse de changement, checklist de revue. |
| `vitrine-locale` | Construit un site vitrine one-page pour un commerce local en Astro + Tailwind — cadrage, recherche design, charte anti-générique, développement git-flow + TDD + index OKF. |
| `create-mcp` | Construit, durcit ou audite la sécurité d'un serveur MCP — identité par token personnel, OAuth 2.1, cloisonnement multi-tenant par tool, rate-limit, logging, mode sandbox, bearer sur le manifeste. |
| `init-projet` | Initialise un projet en rédigeant son CLAUDE.md par questions fermées (QCM), puis amorce le BRAIN du projet (`~/brain/<projet>/`) et le bloc de journalisation des erreurs. |
| `compile-rules` | Compile le journal d'erreurs (`bag.ndjson`) en règles projet : regroupement par trigger, scoring, promotion/démotion, régénération du manifeste de routage. Sur demande explicite uniquement, jamais d'écriture sans validation. |
| `send-feedback` | Envoie un retour sur ces skills en amont, sous forme d'issue GitHub sur `YoLaub/skills_stock` — reprend les mots de l'utilisateur tels quels, propose le contexte technique autour, anonymise avant publication. |

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

Ce dépôt est packagé comme un **plugin Claude Code** (`yls`, servi par le marketplace
`yl-solution`) : une fois installé (voir [Installation](#installation)), Claude Code
découvre automatiquement tout `agents/`, `skills/` et `commands/` du dépôt, sans copie
manuelle ni configuration.

---

## Structure du dépôt

```
.
├── .claude-plugin/
│   ├── marketplace.json             ← marketplace "yl-solution"
│   └── plugin.json                  ← plugin "yls"
├── agents/                          ← fichiers .md à plat (pas de sous-dossier :
│   │                                  la découverte par défaut du plugin ne
│   │                                  scanne pas les sous-répertoires d'agents/)
│   ├── cv-analyst.md                ← Pipeline RH
│   ├── cv-designer.md
│   ├── cv-recruiter.md
│   ├── rh-interviewer.md
│   ├── tech-interviewer.md
│   ├── debrief-agent.md
│   ├── cert-intake.md               ← Pipeline Certification
│   ├── referentiel-loader.md
│   ├── gap-analyser.md
│   ├── exam-preparer.md
│   ├── cert-interviewer.md
│   └── cert-debrief.md
├── skills/
│   ├── archi-scanner/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── archi-diagrams/
│   │   ├── SKILL.md
│   │   └── references/
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
│   │       ├── mode-coder.md        # déroulé complet du mode coder
│   │       └── templates-coder/     # 5 templates docs/ du mode coder
│   ├── presentation-builder/
│   │   ├── SKILL.md
│   │   ├── design-system/
│   │   └── references/
│   ├── skill-architect/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── create-mcp/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── init-projet/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── compile-rules/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── vitrine-locale/
│   │   ├── SKILL.md
│   │   └── references/
│   └── send-feedback/
│       ├── SKILL.md
│       └── references/
├── commands/
│   ├── archi-diagrams.md
│   └── archi-scanner.md
└── README.md
```

---

## Installation

### Prérequis

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installé

### Marketplace de plugin (recommandé)

Zéro script, zéro copie de fichiers. Dans Claude Code :

```
/plugin marketplace add YoLaub/skills_stock
/plugin install yls@yl-solution
```

Tous les agents, skills et commandes du dépôt sont immédiatement actifs, dans
**n'importe quel projet ouvert dans Claude Code** — pas seulement celui où la commande
a été tapée. Les skills sont préfixés par le plugin : `/yls:greenfield-tdd-okf`,
`/yls:skill-architect`, etc. Un `/yls:` seul suffit à voir la liste.

Mettre à jour plus tard :

```
/plugin marketplace update yl-solution
```

Retirer :

```
/plugin uninstall yls
```

### Développement — plugin en place (pour modifier un skill et voir l'effet tout de suite)

Si tu as cloné ce dépôt et veux éditer un skill directement, sans réinstaller à chaque
changement : pointe `~/.claude/skills/` vers le clone avec un lien symbolique.

```bash
ln -s /chemin/vers/skills_stock ~/.claude/skills/yl-solution
```

Le dossier est chargé en place (`yls@skills-dir`) au lieu d'être copié — chaque édition
du fichier source est immédiatement active, `/reload-plugins` recharge en cours de
session. Alternative sans toucher `~/.claude/skills` : `claude --plugin-dir <clone>`
pour une session isolée.

### Copie manuelle (cas particulier : un seul skill ou agent, sans plugin)

```bash
mkdir -p mon-projet/.claude/agents mon-projet/.claude/skills
cp agents/nom-agent.md mon-projet/.claude/agents/
cp -r skills/nom-pipeline/ mon-projet/.claude/skills/
```

À adapter ensuite : les skills de ce dépôt utilisent des contrats partagés
(`skills/_shared/`, `agents/_shared/` s'il y en a) résolus par chemin relatif — extraire
un seul dossier peut casser cette résolution. Vérifier ses éventuelles dépendances
avant de l'isoler.

---

## Intégration dans un projet

Une fois le plugin installé, ses skills et agents sont actifs dans toute session
Claude Code. Les déclencher naturellement dans le chat :

```
Lance le pipeline [nom]
```
```
Utilise l'agent [nom-agent] pour [tâche]
```
```
/yls:nom-du-skill
```

---

## Personnalisation

Les agents de ce dépôt sont **génériques par défaut**. Ils contiennent des placeholders à adapter au contexte du projet, signalés entre crochets :

```
[NOM_ENTREPRISE], [STACK_PRINCIPALE], [SECTEUR], [LANGUE_CIBLE]
```

Un skill installé via le plugin marketplace vit dans le cache des plugins, pas dans le
projet : pour le personnaliser durablement, éditer le clone du dépôt (mode
développement ci-dessus) plutôt que le fichier installé, qui sera écrasé au prochain
`/plugin marketplace update`. Pour une personnalisation ponctuelle propre à un seul
projet, copier le fichier concerné dans `.claude/skills/` de ce projet (voir "Copie
manuelle" ci-dessus) — la copie locale prend le pas sur le plugin.

### Bonnes pratiques

- Personnaliser dans le clone (mode développement), jamais dans le cache des plugins
- Documenter les changements notables dans ce README pour les autres utilisateurs
- Tester un agent seul avant de lancer un pipeline complet
- Un skill qui a mal réagi ou qu'il manque quelque chose → `/yls:send-feedback`

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
