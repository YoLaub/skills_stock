# Parcours candidat

Traite une candidature de A à Z, jusqu'à la recherche d'offres réelles.

## Vue d'ensemble

```
[CV brut] → cv-analyst → cv-designer → cv-recruiter
                                              ↓
                              rh-interviewer → tech-interviewer
                                              ↓
                                        debrief-agent → job-search-agent
```

## Étapes

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 1 | `cv-analyst` | CV brut + poste visé | Score ATS, mots-clés, CV amélioré |
| 2 | `cv-designer` | CV amélioré + style souhaité | CV mis en forme |
| 3 | `cv-recruiter` | CV stylisé + email recruteur + ATS | Email envoi + rapport ATS |
| 4 | `rh-interviewer` | Profil candidat | Transcript entretien motivation |
| 5 | `tech-interviewer` | Profil + stack technique | Transcript entretien technique |
| 6 | `debrief-agent` | Tous les transcripts + scores | Bilan complet avec recommandation |
| 7 | `job-search-agent` | Profil candidat + poste visé | Offres correspondantes (France Travail + navigation assistée) |

`job-search-agent` est indépendant du reste : il peut être lancé seul, à
n'importe quel moment, sans avoir fait les étapes 1-6.

## Comment lancer

### Pipeline complet (recommandé)
```
Lance le parcours candidat complet pour ce profil :
- Poste visé : [POSTE]
- CV : [CONTENU CV]
```

### Agent unique
```
Lance uniquement l'agent [NOM_AGENT] avec ces données : [DONNÉES]
```

### Reprendre à une étape
```
Reprends le parcours candidat à l'étape [cv-designer / cv-recruiter /
rh-interviewer / tech-interviewer / debrief-agent / job-search-agent]
avec les données de contexte suivantes : [CONTEXTE]
```

## Contexte partagé

Chaque agent lit et écrit dans le contexte partagé suivant (en mémoire ou
dans `agence-emploi/context-candidat.json`) :

```json
{
  "candidat": {
    "nom": "",
    "poste_vise": "",
    "localisation": "",
    "cv_brut": "",
    "cv_ameliore": "",
    "cv_style": ""
  },
  "scores": {
    "ats": 0,
    "impact": 0,
    "mots_cles_manquants": [],
    "problemes_structure": []
  },
  "recrutement": {
    "email_recruteur": "",
    "ats_cible": "",
    "email_envoye": "",
    "rapport_ats": ""
  },
  "entretiens": {
    "rh_transcript": [],
    "tech_transcript": []
  },
  "bilan": {
    "note_globale": 0,
    "recommandation": "",
    "points_forts": [],
    "axes_amelioration": [],
    "conclusion": ""
  },
  "offres": {
    "sources_interrogees": [],
    "liste": []
  }
}
```

## Fichiers de sortie

Tous dans `agence-emploi/output/` :
- `output/cv-ameliore.md` — CV optimisé ATS
- `output/cv-style.md` — CV mis en forme
- `output/email-recruteur.md` — Email de soumission
- `output/rapport-ats.md` — Rapport compatibilité ATS
- `output/transcript-rh.md` — Transcript entretien RH
- `output/transcript-tech.md` — Transcript entretien tech
- `output/bilan-final.md` — Bilan complet avec recommandation
- `output/offres-emploi.md` — Offres correspondantes trouvées

## Notes spécifiques

- Le bilan final (`debrief-agent`) ne se génère pas sans au moins
  l'analyse CV ET un entretien complété.
- `job-search-agent` nécessite `FRANCE_TRAVAIL_CLIENT_ID` /
  `FRANCE_TRAVAIL_CLIENT_SECRET` en variable d'environnement pour la
  recherche API réelle (gratuit, à créer sur francetravail.io) ; sans ces
  identifiants il bascule sur la navigation assistée seule via
  `claude-in-chrome`, à charger si pas déjà disponible.
