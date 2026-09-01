---
name: greenfield-tdd-okf
description: Workflow répétable pour construire un produit en TDD avec index OKF, en deux modes — viber (rapide, direct au code) ou coder (cadrage documenté → backlog GitHub → GitHub Flow). Détecte d'abord si le dépôt est vierge ou contient déjà du code : sur un projet en cours, cartographie l'existant via archi-scanner avant de reprendre le workflow. Demande toujours le mode. Utiliser au démarrage d'un nouveau projet applicatif ou d'un gros module, comme à la reprise d'un projet non initié avec ce skill.
---

# Greenfield TDD + OKF

Workflow éprouvé sur CRM_TEAM (2026-07) et généralisé sur Survival AI (2026-08). Objectif :
livrer vite sans dette, avec un contexte relisible en quelques fichiers.

Références (à lire au moment indiqué, pas avant) :
- `references/pieges.md` — pièges connus par stack. Consulter les sections « Génériques »
  + celles de la stack du projet en phase 2 ; enrichir en phase 3/4.
- `references/okf-fiche-template.md` — format de la fiche OKF. Consulter à la première
  fiche de la phase 3 (mode viber) ou de la phase 3 coder.
- `references/mode-coder.md` — déroulé complet du mode coder (phases 1 à 4). À lire
  entièrement dès que le mode coder est choisi, pas avant.
- `references/reprise-projet.md` — reprise d'un projet existant (brownfield). À lire
  entièrement dès que la Phase 0 détecte du code préexistant, pas avant.

## Phase 0 — Détection du terrain (toujours, avant toute autre action)

Le workflow suppose un dépôt vierge ; sur un projet déjà entamé, appliquer les phases 1-2
telles quelles écraserait ou dupliquerait l'existant. Trancher d'abord :

```bash
git log --oneline -1 2>/dev/null
ls -A | grep -v '^\.git$' | head -20
find . -maxdepth 2 -name "package.json" -o -name "pyproject.toml" -o -name "go.mod" \
  -o -name "Cargo.toml" -o -name "composer.json" -o -name "Gemfile" -o -name "pom.xml" \
  2>/dev/null | grep -v node_modules | head
```

- **Nouveau projet** — dossier vide, ou seulement `.git`/README/LICENSE, aucun manifeste
  avec des dépendances, aucun code source → ne rien changer, continuer en Phase 0 bis.
- **Projet en cours** — un manifeste, du code source ou un historique git de travail réel
  → **dérouler `references/reprise-projet.md`** (cartographie via le skill `archi-scanner`,
  inventaire des acquis, choix du point de reprise) AVANT toute autre phase. Ce fichier
  renvoie ensuite vers la bonne phase du workflow.

En cas de doute (quelques fichiers épars, un bootstrap abandonné), demander à
l'utilisateur plutôt que deviner : le coût d'un scan inutile est faible, celui d'un
bootstrap par-dessus du code existant ne l'est pas.

## Phase 0 bis — Choix du mode

Poser une question fermée (AskUserQuestion) : **viber** (rapide — cadrage minimal, direct
au bootstrap puis aux features, phases 1-4 ci-dessous) ou **coder** (produit à part
entière — cadrage documenté en 5 fichiers `docs/`, Epics + Issues GitHub, TDD via GitHub
Flow, `references/mode-coder.md`) ? Ne jamais deviner : si l'utilisateur l'a déjà dit
dans son message initial, sauter la question et confirmer le choix en une phrase.

**Si coder** → dérouler intégralement `references/mode-coder.md`, ignorer les phases 1-4.
**Si viber** → continuer ci-dessous.

## Phase 1 — Recherche & cadrage (avant TOUTE ligne de code)
1. Chercher l'existant open source à imiter (web) : 2-3 références, noter stack et périmètre.
2. **Ne jamais scraper/recoder ce qui a une API officielle ou une lib réutilisable** (licence permissive → l'utiliser telle quelle).
3. Poser 3-4 questions de cadrage fermées (AskUserQuestion) : modèle à imiter, stack,
   contraintes structurantes du domaine (ex. multi-entité), options payantes.
4. Écrire le plan (contexte, décisions validées, architecture, modèle de données, étapes
   parallélisables, vérification E2E) et le faire valider.

## Phase 2 — Bootstrap (une branche `feature/bootstrap`)
- Lire `references/pieges.md` (sections « Génériques » + stack choisie) avant de configurer
  l'outillage.
- `git init -b main` → **premier commit sur main avant toute autre branche** (une branche créée
  avant le premier commit est "unborn" : le prochain commit atterrit sur la branche courante, pas
  forcément sur main) → branche `dev` depuis main → une branche par feature depuis dev. Merge
  `--no-ff` vers dev UNIQUEMENT si tests verts + E2E fait. Jamais de commit direct sur main/dev.
- Monorepo : workspaces dès le départ si un package est partagé (sinon la résolution
  bundler casse) ; docker-compose pour la base ; `.env.example` complet.
- **Lire les docs embarquées des frameworks récents** (ex. `node_modules/next/dist/docs`)
  au lieu de supposer : les conventions changent (proxy.ts vs middleware.ts…).
- CLAUDE.md : conventions, commandes, règles métier clés.
- Créer `docs/index/` (OKF) + `retro.md` immédiatement.

## Phase 3 — Chaque feature (branche dédiée, TDD)
1. Tests d'abord sur la **logique pure** (calculs, machines d'états, dédoublonnage,
   signatures) placée dans `services/` ; UI/routes = orchestration mince.
2. Toute logique est un service unique consommé par l'UI ET par les interfaces machine
   (tools MCP, API) — jamais de duplication.
3. Suite verte → build → **E2E réel** (curl sur l'API/MCP, vrai appel externe si gratuit).
4. Fiche OKF `docs/index/<feature>.md` au format `references/okf-fiche-template.md`.
   Dater les décisions.
5. Ajouter les pièges rencontrés à `retro.md` AU MOMENT où ils mordent ; si un piège est
   générique (réutilisable hors projet), l'ajouter aussi à `references/pieges.md`.
6. Commit conventionnel, merge --no-ff vers dev.

## Phase 4 — Clôture
- Rétro finale dans `retro.md`, merge dev → main (jalon stable), tag éventuel.
- Reporter les nouveaux pièges dans `references/pieges.md` (section datée par stack).
  Ne modifier ce SKILL.md que si la méthodologie elle-même change ; le déroulé détaillé
  du mode coder évolue dans `references/mode-coder.md`, ses templates dans
  `references/templates-coder/`.
