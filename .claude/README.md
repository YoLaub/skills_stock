# .claude — Pipeline RH Multi-Agents

## Structure

```
.claude/
├── agents/
│   ├── cv-analyst.md        # Agent 1 — Analyse CV + score ATS
│   ├── cv-designer.md       # Agent 2 — Mise en forme du CV
│   ├── cv-recruiter.md      # Agent 3 — Email recruteur + rapport ATS
│   ├── rh-interviewer.md    # Agent 4 — Entretien motivation (conversationnel)
│   ├── tech-interviewer.md  # Agent 5 — Entretien technique (conversationnel)
│   └── debrief-agent.md     # Agent 6 — Bilan final points forts/faibles
└── skills/
    └── rh-pipeline/
        └── SKILL.md         # Skill d'orchestration du pipeline complet
```

## Usage rapide dans Claude Code

### Pipeline complet
```
Lance le pipeline RH complet :
- Poste visé : Développeur fullstack
- CV : [coller le CV ici]
```

### Agent seul
```
Lance l'agent cv-analyst avec ce CV : [CV]
```

### Reprendre à une étape
```
Reprends le pipeline à l'étape rh-interviewer avec ce contexte : [JSON contexte]
```

## Outputs générés

Tous les livrables sont écrits dans `rh-pipeline/output/` :

| Fichier | Produit par |
|---------|------------|
| `cv-ameliore.md` | cv-analyst |
| `cv-style.md` | cv-designer |
| `email-recruteur.md` | cv-recruiter |
| `rapport-ats.md` | cv-recruiter |
| `transcript-rh.md` | rh-interviewer |
| `transcript-tech.md` | tech-interviewer |
| `bilan-final.md` | debrief-agent |
