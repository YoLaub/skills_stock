# Parcours RH

Traite un recrutement de A à Z, du cadrage du besoin à la préparation de
l'entretien — jamais de sélection ni de rédaction d'annonce sans besoin
cadré en amont.

## Vue d'ensemble

```
[Demande brute] → rh-needs-analyst → job-posting-writer
                                              ↓
                                    (diffusion externe au skill)
                                              ↓
                                    candidate-screener → interview-designer
```

## Étapes

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 1 | `rh-needs-analyst` | Demande de recrutement brute | Besoin cadré (compétences, séniorité, contraintes) |
| 2 | `job-posting-writer` | Besoin RH | Annonce de poste |
| 3 | `candidate-screener` | Lot de CV reçus + besoin/annonce | Classement argumenté des candidats |
| 4 | `interview-designer` | Besoin/annonce + profil(s) retenu(s) | Grille d'entretien structurée |

Entre l'étape 2 et 3, la diffusion de l'annonce et la réception des
candidatures se font hors du skill (le recruteur poste l'annonce, reçoit
des CV) — le pipeline reprend dès qu'il y a des candidatures à comparer.

## Comment lancer

### Pipeline complet (recommandé)
```
Lance le parcours RH complet pour ce recrutement :
- Poste à pourvoir : [POSTE]
- Contexte : [DESCRIPTION LIBRE]
```

### Agent unique
```
Lance uniquement l'agent [NOM_AGENT] avec ces données : [DONNÉES]
```

Cas fréquent : arriver directement sur `candidate-screener` avec plusieurs
CV en main, sans être passé par `rh-needs-analyst`/`job-posting-writer` —
dans ce cas demander au moins les compétences indispensables du poste
avant de noter quoi que ce soit (voir `candidate-screener`).

### Reprendre à une étape
```
Reprends le parcours RH à l'étape [job-posting-writer / candidate-screener
/ interview-designer] avec les données de contexte suivantes : [CONTEXTE]
```

## Contexte partagé

Chaque agent lit et écrit dans le contexte partagé suivant (en mémoire ou
dans `agence-emploi/context-rh.json`) :

```json
{
  "besoin": {
    "poste": "",
    "entreprise": "",
    "competences_indispensables": [],
    "competences_souhaitables": [],
    "seniorite": "",
    "contraintes": {
      "budget": "",
      "localisation": "",
      "contrat": "",
      "urgence": ""
    },
    "points_vigilance": []
  },
  "annonce": {
    "texte": ""
  },
  "screening": {
    "candidats_evalues": 0,
    "classement": [],
    "candidat_recommande": ""
  },
  "entretien": {
    "grille": "",
    "retour_galop_essai": ""
  }
}
```

## Fichiers de sortie

Tous dans `agence-emploi/output/` :
- `output/besoin-rh.md` — Besoin de recrutement cadré
- `output/annonce-poste.md` — Annonce publiable
- `output/screening-candidats.md` — Classement argumenté des candidats
- `output/grille-entretien.md` — Grille d'entretien + retour de galop d'essai

## Notes spécifiques

- `rh-needs-analyst` bloque volontairement sur les incohérences détectées
  (ex. séniorité vs budget) plutôt que de les lisser — les faire trancher
  par l'utilisateur avant de continuer.
- `candidate-screener` refuse un lot d'un seul candidat (rediriger vers
  `cv-analyst`, parcours candidat, qui répond à une question différente).
- `interview-designer` n'est pas `rh-interviewer`/`tech-interviewer` du
  parcours candidat : il outille le recruteur, il ne simule pas
  l'entretien à sa place (sauf demande explicite de galop d'essai pour
  tester la grille elle-même, pas pour juger un vrai candidat).
