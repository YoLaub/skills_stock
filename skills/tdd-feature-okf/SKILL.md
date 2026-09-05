---
name: tdd-feature-okf
description: >
  Implémenter UNE feature en TDD sur un projet qui suit les conventions greenfield
  (branche dédiée depuis dev, logique pure testée en premier dans services/, un service
  unique consommé par l'UI ET les interfaces machine, fiche OKF, retro.md, merge --no-ff).
  Point de ré-entrée quand on redémarre le contexte sur un projet en cours. Utiliser pour
  « implémente la feature X en TDD », « reprends la feature en cours », « continue le
  TDD », « ajoute une feature ». Deuxième maillon du trio greenfield :
  greenfield-bootstrap → tdd-feature-okf → (lot d'issues) tdd-backlog-run.
---

# TDD Feature + OKF

La boucle qui se répète : une feature, test-first, documentée en une fiche OKF relisible
en une lecture. Invocable à froid — pas besoin d'avoir déroulé `greenfield-bootstrap`
dans la même session.

Références (à lire au moment indiqué, pas avant) :
- `references/pieges.md` — pièges connus par stack. Sections « Génériques » + celle de la
  stack du projet, à consulter quand un choix d'outillage se pose ; enrichir au fil de l'eau.
- `references/okf-fiche-template.md` — format de la fiche OKF. À consulter avant d'écrire
  la fiche de la feature.
- `references/orientation.md` — se réorienter dans un projet en cours (archi-scanner +
  inventaire des acquis). À lire seulement si la Phase 0 en a besoin.

## Phase 0 — Terrain / réorientation

```bash
git branch --show-current
git status --porcelain
```

- **Dépôt vierge** (aucun code, aucun manifeste) → ce n'est pas le bon skill :
  `greenfield-bootstrap` d'abord.
- **Sur `main` / `dev`, ou arbre sale** → s'arrêter, créer/rejoindre une branche de
  feature depuis `dev` avant de coder.
- **Tu sais quelle feature implémenter et où en est le projet** → Phase 1 directement.
- **Contexte redémarré, tu ne sais plus où en est le projet** → dérouler
  `references/orientation.md` (archi-scanner, lire `archi-output/INDEX.md` +
  `docs/index/*` + `retro.md`, faire tourner la suite de tests), PUIS Phase 1.

## Phase 1 — La boucle (branche dédiée, TDD)

1. **Tests d'abord sur la logique pure** (calculs, machines d'états, dédoublonnage,
   signatures) placée dans `services/` ; UI/routes = orchestration mince.
2. **Toute logique est un service unique** consommé par l'UI ET par les interfaces
   machine (tools MCP, API) — jamais de duplication.
3. Suite verte → build → **E2E réel** (curl sur l'API/MCP, vrai appel externe si gratuit).
4. Fiche OKF `docs/index/<feature>.md` au format `references/okf-fiche-template.md`.
   Dater les décisions (date absolue).
5. Ajouter les pièges rencontrés à `retro.md` **au moment où ils mordent** ; si un piège
   est générique (réutilisable hors projet), l'ajouter aussi à `references/pieges.md`
   (**répliquer dans les 3 skills du trio**).
6. Commit conventionnel, merge `--no-ff` vers `dev` **uniquement si** tests verts + E2E
   fait. Jamais de commit direct sur main/dev.

Jalon stable : quand un ensemble de features forme un tout cohérent, merge `dev → main`
(rétro finale dans `retro.md`, tag éventuel).

## Périmètre à plusieurs unités

Une seule feature → cette boucle. **Plusieurs features / issues indépendantes à traiter
en parallèle** (typiquement le backlog d'un milestone) → `tdd-backlog-run` : superviseur
+ worktree + sous-agent frais par issue + porte de conformité avant merge.

## Évolution

- Nouveau piège → `references/pieges.md` (répliquer dans les 3 skills du trio).
- Nouveau champ ou règle de fiche → `references/okf-fiche-template.md`.
- Nouvelle logique de réorientation brownfield → `references/orientation.md` (répliquer
  dans `tdd-backlog-run`).
- Ne modifier ce SKILL.md que si la boucle TDD elle-même change.
