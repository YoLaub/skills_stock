---
name: greenfield-bootstrap
description: >
  Démarrer un NOUVEAU projet applicatif (ou gros module) en TDD avec index OKF —
  cadrage, git init + scaffold, docs/index OKF + retro.md, et (mode coder) backlog
  GitHub. Deux modes : viber (cadrage minimal, direct au code) ou coder (5 documents
  docs/ + Epics/Issues GitHub). Utiliser sur un dépôt vierge ou quasi vierge. Sur un
  projet déjà entamé, ce n'est PAS le bon skill : voir tdd-feature-okf (une feature)
  ou tdd-backlog-run (un lot d'issues). Premier maillon du trio greenfield :
  greenfield-bootstrap → tdd-feature-okf / tdd-backlog-run.
---

# Greenfield Bootstrap

Amorcer un projet pour livrer vite sans dette, avec un contexte relisible en quelques
fichiers. Éprouvé sur CRM_TEAM (2026-07) et Survival AI (2026-08).

Références (à lire au moment indiqué, pas avant) :
- `references/pieges.md` — pièges connus par stack. Sections « Génériques » + celle de la
  stack choisie, à lire en Phase 2 (bootstrap de l'outillage).
- `references/mode-coder-cadrage.md` — déroulé du mode coder (cadrage documenté + backlog
  GitHub). À lire entièrement dès que le mode coder est choisi, pas avant.
- `references/templates-coder/` — un fichier par document `docs/`, lu un par un au moment
  de rédiger le document correspondant.

## Phase 0 — Terrain (toujours, avant toute autre action)

```bash
git log --oneline -1 2>/dev/null
ls -A | grep -v '^\.git$' | head -20
find . -maxdepth 2 -name "package.json" -o -name "pyproject.toml" -o -name "go.mod" \
  -o -name "Cargo.toml" -o -name "composer.json" -o -name "Gemfile" -o -name "pom.xml" \
  2>/dev/null | grep -v node_modules | head
```

- **Dépôt vierge** — vide, ou seulement `.git`/README/LICENSE, aucun manifeste avec des
  dépendances, aucun code source → continuer en Phase 0 bis.
- **Projet en cours** — un manifeste, du code source, un historique git de travail réel →
  **ce skill n'est pas le bon** : appliquer les Phases 1-2 écraserait l'existant.
  - Tu veux implémenter une feature → `tdd-feature-okf`.
  - Tu veux dérouler un lot d'issues / un milestone → `tdd-backlog-run`.
  - Le projet a du code mais aucun plan produit → revenir ici en **mode coder** (Phase 0
    bis → coder), en rédigeant les 5 documents à partir de l'existant, pas d'une vision
    inventée.
- **Doute** (fichiers épars, bootstrap abandonné) → demander à l'utilisateur, ne pas
  deviner : le coût d'un bootstrap par-dessus du code existant n'est pas récupérable.

## Phase 0 bis — Choix du mode

Question fermée (AskUserQuestion) : **viber** (rapide — cadrage minimal, direct au
bootstrap puis aux features) ou **coder** (produit à part entière — cadrage documenté en
5 fichiers `docs/`, Epics + Issues GitHub) ? Ne jamais deviner : si l'utilisateur l'a
déjà dit, sauter la question et confirmer en une phrase.

**Si coder** → dérouler `references/mode-coder-cadrage.md`, ignorer les Phases 1-2
ci-dessous, puis hand-off vers `tdd-backlog-run` pour l'exécution.
**Si viber** → continuer.

## Phase 1 — Recherche & cadrage (avant TOUTE ligne de code)

1. Chercher l'existant open source à imiter (web) : 2-3 références, noter stack et périmètre.
2. **Ne jamais scraper/recoder ce qui a une API officielle ou une lib réutilisable**
   (licence permissive → l'utiliser telle quelle).
3. Poser 3-4 questions de cadrage fermées (AskUserQuestion) : modèle à imiter, stack,
   contraintes structurantes du domaine (ex. multi-entité), options payantes.
4. Écrire le plan (contexte, décisions validées, architecture, modèle de données, étapes
   parallélisables, vérification E2E) et le faire valider.

## Phase 2 — Bootstrap (une branche `feature/bootstrap`)

- Lire `references/pieges.md` (sections « Génériques » + stack choisie) avant de
  configurer l'outillage.
- `git init -b main` → **premier commit sur main avant toute autre branche** (une branche
  créée avant le premier commit est « unborn » : le prochain commit atterrit sur la
  branche courante, pas forcément sur main) → branche `dev` depuis main → une branche par
  feature depuis dev. Jamais de commit direct sur main/dev.
- Monorepo : workspaces dès le départ si un package est partagé (sinon la résolution
  bundler casse) ; docker-compose pour la base ; `.env.example` complet.
- **Lire les docs embarquées des frameworks récents** (ex. `node_modules/next/dist/docs`)
  au lieu de supposer : les conventions changent (proxy.ts vs middleware.ts…).
- `CLAUDE.md` : conventions, commandes, règles métier clés.
- Créer `docs/index/` (OKF) + `retro.md` immédiatement.
- Un `typecheck: tsc --noEmit` par package testable + un step CI dédié dès le bootstrap
  (cf. `pieges.md` § Génériques).

## Fin — Hand-off

Bootstrap fini (branche `feature/bootstrap` mergée `--no-ff` vers dev, tests verts) :
- pour chaque feature → **`tdd-feature-okf`** ;
- pour dérouler un backlog d'issues (mode coder) → **`tdd-backlog-run`**.

## Évolution

- Nouveau piège générique / de stack → `references/pieges.md` (**répliquer dans les 3
  skills du trio**).
- Nouveau template de document `docs/` ou section → `references/templates-coder/*.md`
  (append-only).
- Ne modifier ce SKILL.md que si la méthodologie de démarrage change.
