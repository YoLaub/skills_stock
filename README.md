# 🧠 Skills & Agents — Claude Code

Dépôt public de skills et agents réutilisables pour [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

Un **skill** décrit un pipeline ou un processus complexe. Un **agent** est un spécialiste autonome qui exécute une tâche précise. Ensemble, ils permettent à Claude Code de se comporter comme une équipe de collaborateurs spécialisés sur n'importe quel projet.

---

## Table des matières

- [Catalogue](#catalogue)
- [Notation (skill-bench)](#notation-skill-bench)
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
| `agence-emploi` | Mini agence pour l'emploi à deux voix — candidat ou RH, choisies en Phase 0. Côté candidat : analyse CV, mise en forme, email recruteur, entretiens, bilan, recherche d'offres réelles (API France Travail + navigation assistée). Côté RH : cadrage du besoin de recrutement, rédaction d'annonce, analyse comparative de candidats, grille d'entretien. |
| `cert-pipeline` | Pipeline de préparation à une certification ou titre professionnel — chargement référentiel, analyse des écarts, fiches de révision, simulation jury, bilan. |
| `cours-pipeline` | Construit une séance de cours à partir d'un thème — compétences visées définies avant le contenu, exploration des bases, application ludique alignée sur ces compétences, vérification des acquis, support de présentation (via `presentation-builder`), fiche de séance récapitulative. |
| `brain-builder` | Crée et maintient des "cerveaux projets" sous forme de vaults Obsidian structurés (architecture 3 couches : raw / wiki / reports), inspirés de l'approche LLM Wiki. |
| `skill-optimizer` | Optimise un SKILL.md existant par micro-éditions validées (approche SkillOpt) : baseline → proposition → évaluation → commit ou revert. |
| `skill-bench` | Banc de test qui évalue un ou plusieurs skills/agents contre leur objectif déclaré, produit un tableau de notation comparatif (score **et** coût estimé en tokens/$), et renvoie ceux qui échouent vers `skill-optimizer` — détecte, ne corrige jamais lui-même. |
| `greenfield-tdd-okf` | Workflow répétable pour démarrer un projet greenfield en TDD avec index OKF, en deux modes choisis en Phase 0 — **viber** (cadrage minimal, direct au bootstrap git-flow) ou **coder** (cadrage documenté en 5 fichiers `docs/`, Epics + Issues GitHub, TDD via GitHub Flow). |
| `presentation-builder` | Construit une présentation orale (soutenance, pitch, talk, démo) avec modèle assertion-preuve et design system fermé — export Marp en .pptx/PDF, schémas Mermaid et graphiques automatiques, porte de contrôle visuelle avant livraison. |
| `skill-architect` | Conçoit l'architecture d'un nouveau skill ou refactore la structure d'un skill existant — SOLID transposé aux skills, patterns (Template Method, Facade, Pipeline, Strategy), découpage par vitesse de changement, checklist de revue. |
| `vitrine-locale` | Construit un site vitrine one-page pour un commerce local en Astro + Tailwind — cadrage, recherche design, charte anti-générique, développement git-flow + TDD + index OKF. |
| `create-mcp` | Construit, durcit ou audite la sécurité d'un serveur MCP — identité par token personnel, OAuth 2.1, cloisonnement multi-tenant par tool, rate-limit, logging, mode sandbox, bearer sur le manifeste. |
| `init-projet` | Initialise un projet en rédigeant son CLAUDE.md par questions fermées (QCM), puis amorce le BRAIN du projet (`~/brain/<projet>/`) et le bloc de journalisation des erreurs. |
| `compile-rules` | Compile le journal d'erreurs (`bag.ndjson`) en règles projet : regroupement par trigger, scoring, promotion/démotion, régénération du manifeste de routage. Sur demande explicite uniquement, jamais d'écriture sans validation. |
| `send-feedback` | Envoie un retour sur ces skills en amont, sous forme d'issue GitHub sur `YoLaub/skills_stock` — reprend les mots de l'utilisateur tels quels, propose le contexte technique autour, anonymise avant publication. |

### Agents — Agence Emploi (parcours candidat)

| Agent | Description |
|-------|-------------|
| `cv-analyst` | Analyse un CV brut pour évaluer sa compatibilité ATS, identifier les mots-clés manquants et produire une version améliorée. |
| `cv-designer` | Génère un fichier HTML visuellement original format A4, prêt à imprimer ou exporter en PDF depuis le navigateur. |
| `cv-recruiter` | Rédige l'email de candidature professionnel et génère le rapport de soumission ATS final. |
| `rh-interviewer` | Simule un entretien de motivation en mode conversationnel — pose les questions, évalue les réponses, enchaîne. |
| `tech-interviewer` | Simule un entretien technique adapté au profil et à la stack — adapte le niveau et les thèmes détectés dans le CV. |
| `debrief-agent` | Synthétise toutes les étapes du parcours candidat en un bilan complet avec note, recommandation, points forts et axes d'amélioration. |
| `job-search-agent` | Recherche des offres correspondant au profil via l'API France Travail (accès libre) et une navigation assistée sur Indeed/LinkedIn/WTTJ/APEC. |

### Agents — Agence Emploi (parcours RH)

| Agent | Description |
|-------|-------------|
| `rh-needs-analyst` | Cadre le besoin de recrutement réel d'une entreprise avant toute annonce ou sélection — compétences indispensables vs souhaitables, séniorité, budget. |
| `job-posting-writer` | Rédige une annonce de poste cohérente avec le besoin RH cadré en amont. |
| `candidate-screener` | Analyse et classe un lot de candidatures reçues pour un même poste, avec justification comparative. |
| `interview-designer` | Construit une grille d'entretien structurée côté recruteur (questions, grille de notation), avec galop d'essai optionnel pour la stress-tester. |

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

## Notation (skill-bench)

Résultats du dernier passage de [`skill-bench`](skills/skill-bench/SKILL.md) sur les
skills/agents de ce dépôt : exécution bout-en-bout par un sous-agent qui incarne un
persona, jugée par un **autre** sous-agent frais (`model: opus`) contre le contrat
déclaré de la cible (Inputs/Output) et, quand il existe, contre le format attendu par
l'étape suivante du pipeline. Seuil de conformité : 70 %.

Depuis le 2026-08-14, `skill-bench` note aussi un **coût observé** (tokens +
estimation $, tarif mixte — voir `references/tarifs.md` du skill) : les scores
ci-dessous datent d'avant cet ajout et n'ont pas encore cette colonne — elle
apparaîtra au prochain passage.

**Ce tableau est une photo à une date donnée, pas une garantie permanente** — toute
modification du fichier concerné invalide son score jusqu'au prochain passage.

| Cible | Type | Score | Verdict | Testé le |
|---|---|---|---|---|
| `rh-needs-analyst` | agent | 87.5 % | ✅ Conforme | 2026-08-13 |
| `job-posting-writer` | agent | 96.2 % | ✅ Conforme | 2026-08-13 |
| `candidate-screener` | agent | 96.2 % | ✅ Conforme | 2026-08-13 |
| `interview-designer` | agent | 97.5 % | ✅ Conforme | 2026-08-13 |
| `job-search-agent` | agent | 92.5 % | ✅ Conforme | 2026-08-13 |
| `cours-pipeline` | skill | 92.3 % | ✅ Conforme | 2026-08-13 |
| `greenfield-tdd-okf` — mode viber (phases 0-4) | skill | 89.7 % | ✅ Conforme | 2026-08-13 |
| `greenfield-tdd-okf` — mode coder (Phase 1, 5 docs) | skill | 94.7 % | ✅ Conforme | 2026-08-13 |

**Audité sans score chiffré** (protocole plutôt que livrable — voir
`references/mode-coder-execution.md` du skill) :
`greenfield-tdd-okf` — protocole superviseur/sous-agents (Phase 3, mode coder) :
dry-run local des commandes `git worktree` conforme, mais l'audit structurel avait
détecté un trou de bootstrap entre les deux modes ; corrigé le 2026-08-13
([`31141b9`](commit/31141b9)) — non re-testé par `skill-bench` depuis ce correctif.

**Non testés bout-en-bout** (audit structurel seulement — le changement portait sur un
chemin de sortie ou une ligne de frontmatter, pas sur la logique) : `cv-analyst`,
`cv-designer`, `cv-recruiter`, `rh-interviewer`, `tech-interviewer`, `debrief-agent`,
`gap-analyser`, `presentation-builder`.

**Hors périmètre du banc pour l'instant** : tout le reste du catalogue (jamais passé au
banc) ; le mode coder de `greenfield-tdd-okf` au-delà de la Phase 1 (nécessite de
vraies ressources GitHub) ; `skill-bench` et `skill-optimizer` eux-mêmes (se tester
soi-même pose un problème d'angle mort, non résolu).

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
│   ├── cv-analyst.md                ← Agence Emploi, parcours candidat
│   ├── cv-designer.md
│   ├── cv-recruiter.md
│   ├── rh-interviewer.md
│   ├── tech-interviewer.md
│   ├── debrief-agent.md
│   ├── job-search-agent.md
│   ├── rh-needs-analyst.md          ← Agence Emploi, parcours RH
│   ├── job-posting-writer.md
│   ├── candidate-screener.md
│   ├── interview-designer.md
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
│   ├── agence-emploi/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── parcours-candidat.md
│   │       └── parcours-rh.md
│   ├── cert-pipeline/
│   │   └── SKILL.md
│   ├── cours-pipeline/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── brain-builder/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── skill-optimizer/
│   │   └── SKILL.md
│   ├── skill-bench/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── evals/
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
