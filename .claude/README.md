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
    ├── rh-pipeline/
    │   └── SKILL.md             # Orchestrateur pipeline RH
    └── cert-pipeline/
        └── SKILL.md             # Orchestrateur pipeline Certification

```

---

## Pipeline RH

### Usage rapide
```
Lance le pipeline RH complet :
- Poste visé : Développeur fullstack
- CV : [coller le CV ici]
```

### Outputs — `rh-pipeline/output/`

| Fichier | Produit par |
|---------|------------|
| `cv-ameliore.md` | cv-analyst |
| `cv-style.md` | cv-designer |
| `email-recruteur.md` | cv-recruiter |
| `rapport-ats.md` | cv-recruiter |
| `transcript-rh.md` | rh-interviewer |
| `transcript-tech.md` | tech-interviewer |
| `bilan-final.md` | debrief-agent |

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
