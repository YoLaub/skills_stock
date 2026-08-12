# .claude — Skills & Agents actifs

## Structure

```
.claude/
├── agents/
│   ├── rh/
│   │   ├── cv-analyst.md        # Agent 1 — Analyse CV + score ATS
│   │   ├── cv-designer.md       # Agent 2 — Mise en forme du CV
│   │   ├── cv-recruiter.md      # Agent 3 — Email recruteur + rapport ATS
│   │   ├── rh-interviewer.md    # Agent 4 — Entretien motivation (conversationnel)
│   │   ├── tech-interviewer.md  # Agent 5 — Entretien technique (conversationnel)
│   │   └── debrief-agent.md     # Agent 6 — Bilan final points forts/faibles
│   └── cert/
│       ├── cert-intake.md       # Agent 1 — Collecte certification + profil candidat
│       ├── referentiel-loader.md# Agent 2 — Chargement docs/ ou recherche web
│       ├── gap-analyser.md      # Agent 3 — Croisement profil vs compétences
│       ├── exam-preparer.md     # Agent 4 — Fiches révision + questions probables
│       ├── cert-interviewer.md  # Agent 5 — Simulation entretien jury
│       └── cert-debrief.md      # Agent 6 — Bilan + probabilité de validation
└── skills/
    ├── agence-emploi/
    │   ├── SKILL.md             # Orchestrateur, choix voix candidat/RH
    │   └── references/
    │       ├── parcours-candidat.md
    │       └── parcours-rh.md
    ├── cert-pipeline/
    │   └── SKILL.md             # Orchestrateur pipeline Certification
    ├── cours-pipeline/
    │   ├── SKILL.md             # Orchestrateur pipeline Cours (utilise presentation-builder)
    │   └── references/
    ├── archi-scanner/
    │   ├── SKILL.md             # Scanner d'architecture progressif (5 phases)
    │   └── references/
    │       └── stack-detection.md  # Heuristiques par framework/techno
    └── archi-diagrams/
        ├── SKILL.md             # Générateur de diagrammes Mermaid
        └── references/
            └── mermaid-reference.md  # Syntaxe et pièges Mermaid

```

---

## Agence Emploi

Deux voix, choisies en Phase 0 du skill : candidat ou RH.

### Usage rapide
```
Lance l'agence emploi, côté candidat :
- Poste visé : Développeur fullstack
- CV : [coller le CV ici]
```
```
Lance l'agence emploi, côté RH, pour recruter un [poste].
```

### Outputs — `agence-emploi/output/`

Parcours candidat :

| Fichier | Produit par |
|---------|------------|
| `cv-ameliore.md` | cv-analyst |
| `cv-style.md` | cv-designer |
| `email-recruteur.md` | cv-recruiter |
| `rapport-ats.md` | cv-recruiter |
| `transcript-rh.md` | rh-interviewer |
| `transcript-tech.md` | tech-interviewer |
| `bilan-final.md` | debrief-agent |
| `offres-emploi.md` | job-search-agent |

Parcours RH :

| Fichier | Produit par |
|---------|------------|
| `besoin-rh.md` | rh-needs-analyst |
| `annonce-poste.md` | job-posting-writer |
| `screening-candidats.md` | candidate-screener |
| `grille-entretien.md` | interview-designer |

---

## Pipeline Certification

### Avant de lancer

Déposer le référentiel officiel dans `docs/` si disponible :
```
docs/
└── referentiel-[NOM-CERTIFICATION].pdf
```

### Usage rapide
```
Lance le pipeline certification.
```

### Outputs — `cert-pipeline/output/`

| Fichier | Produit par |
|---------|------------|
| `fiche-candidat.md` | cert-intake |
| `referentiel-resume.md` | referentiel-loader |
| `gap-analysis.md` | gap-analyser |
| `fiches-revision.md` | exam-preparer |
| `questions-probables.md` | exam-preparer |
| `transcript-jury.md` | cert-interviewer |
| `bilan-final.md` | cert-debrief |

---

## Cours Pipeline

Compétences visées définies avant tout contenu ; utilise `presentation-builder` en
Phase 6 pour le support projeté.

### Usage rapide
```
Prépare un cours sur [thème] pour [public], durée [X].
```

### Outputs — `cours-pipeline/output/`

| Fichier | Produit en |
|---------|------------|
| `competences-visees.md` | Phase 2 |
| `contenu-bases.md` | Phase 3 |
| `activite-ludique.md` | Phase 4 |
| `evaluation.md` | Phase 5 |
| `fiche-seance.md` | Phase 7 |

Le deck lui-même (Phase 6) suit la structure de travail de `presentation-builder`,
référencée depuis `fiche-seance.md`.

---

## Archi-Scanner

Scanner d'architecture progressif et générique. Indexe un codebase en 5 phases
sans exploser le context window. Prérequis pour `archi-diagrams`.

### Usage rapide
```
Scanne le projet / Indexe l'architecture / Analyse le codebase
```

### Workflow — 5 phases

```
Phase 1 : Détection du stack (configs + manifestes)
Phase 2 : Extraction des routes (squelette)
Phase 3 : Chaînage Controllers → Services → Entités
Phase 4 : Scan des couches transversales (hooks, utils, middleware)
Phase 5 : Génération de l'index
```

### Outputs — `archi-output/`

| Fichier | Description |
|---------|-------------|
| `INDEX.md` | Référence complète (stack, routes, modules, transversal) |
| `PROJECT_MEMORY.md` | Résumé < 200 lignes pour les autres skills |

---

## Archi-Diagrams

Génère des diagrammes Mermaid à partir de `archi-output/INDEX.md`.
Jamais tout d'un coup — toujours sur demande explicite.

### Prérequis
`archi-output/INDEX.md` doit exister (lancer `archi-scanner` d'abord).

### Usage rapide
```
Génère un diagramme d'architecture / MCD / diagramme de classes / séquence login
```

### Diagrammes disponibles

| # | Type | Source dans l'index |
|---|------|---------------------|
| 1 | Architecture | Stack + Modules + Transversal |
| 2 | Classes | Modules (controllers, services, entités) |
| 3 | MCD | Entités + schemas |
| 4 | Séquence | Routes + Controllers + Services (parcours précis) |
| 5 | Cas d'utilisation | Routes + Modules |

### Outputs — `archi-output/diagrams/`

| Fichier | Description |
|---------|-------------|
| `architecture.mmd` | Vue macro des composants |
| `classes-[module].mmd` | Structure des modules |
| `mcd.mmd` | Modèle conceptuel de données |
| `sequence-[parcours].mmd` | Flow d'un parcours |
| `use-cases.mmd` | Acteurs et fonctionnalités |
