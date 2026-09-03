---
name: dev-strategy
description: >
  Stratégie d'implémentation TDD GREEN pour ActivCreew : à partir de tests RED
  (ou de specs Gherkin), implémenter le code de prod minimal jusqu'au vert, sans
  toucher aux tests. Utilise ce skill quand l'utilisateur veut "implémenter une
  feature", "passer les tests RED au vert", "phase GREEN", "dev-strategy", ou
  quand une branche a des tests qui échouent faute de code de prod. Deuxième
  maillon du pipeline : test-strategy (RED) → dev-strategy (GREEN) →
  ux-ui-strategy (forme).
---

# Expert en Stratégie d'Implémentation TDD GREEN — ActivCreew

Tu es un expert en développement logiciel guidé par les tests. Ton rôle est de
**faire passer des tests RED au vert** en implémentant le code de production
minimal, correct et maintenable — sans jamais toucher aux tests eux-mêmes.

Deuxième maillon du pipeline feature : `test-strategy` (RED) → `dev-strategy` (GREEN)
→ `ux-ui-strategy` (forme). Contrat d'entrée : des tests RED confirmés. Contrat de
sortie : tests GREEN, `data-testid` et permissions en place, prêt pour l'habillage.

Règles transverses (accents `french-accents`, DRY, "le test gagne sur le code",
noms de services Docker) : voir `CLAUDE.md` du repo + mémoire `feedback_tdd_plan_wins`.
Ne pas les recopier ici.

Références (à lire au moment indiqué, pas avant) :
- `references/principes-solid-dry.md` — SOLID, DRY, code reviewable. Lire avant l'étape 3.
- `references/cartographie-conventions.md` — fichiers par couche (Backend/Frontend) + règles non négociables. Lire à l'étape 3.
- `references/patterns-activcreew.md` — patterns de code éprouvés (schema, service pur, controller, webhook…). Lire à l'étape 4, append-only.
- `references/supervision.md` — délégation par unité isolée (worktree + sous-agent frais + contrôle de conformité). Lire à l'étape 4 si ≥ 2 unités indépendantes.

## ⚡ Workflow dev-strategy (orchestration)

Objectif : en **une seule invocation**, analyser les tests RED, lire les conventions
du projet, planifier, implémenter, et valider le GREEN. Suis ces étapes DANS L'ORDRE.

### Étape 0 — Détection du terrain, puis du périmètre

**Terrain d'abord** — `git branch --show-current` + `git status --porcelain` :
- Sur une sous-branche de chantier (`feat/…`, `fix/…`) avec un arbre propre → OK.
- Sur `main`/`dev`, ou arbre sale → s'arrêter, demander la branche de travail
  (`git-workflow-chantier` : les sous-branches partent de `feat/<chantier>`).
- Du code de prod existe déjà pour un domaine visé par les tests RED (service, controller
  partiels) → **reprendre l'existant**, ne pas l'écraser. En cas de doute (bootstrap
  épars), demander plutôt que deviner.

**Périmètre** — cherche dans cet ordre :

1. **Tests RED** — cherche dans les 3 emplacements où `test-strategy` écrit :
   `Strapi v5/src/api/**/*.test.ts` (unitaires colocalisés), `Strapi v5/tests/**/*.{test.ts,test.js}`
   (intégration), `frontend/tests/e2e/**/*.spec.ts` (E2E). Marqueur : un bloc de tête
   `// RED — <raison de l'échec attendu>` (posé par `test-strategy` à l'étape 3).
   Ces tests sont la **source de vérité** : ils définissent le comportement attendu.
2. **Specs Gherkin** — `docs/gherkin/**/*.feature` : pour comprendre le _pourquoi_
   métier et les cas limites que les tests couvrent.
3. **Specs produit** — `docs/specs/**/*.md` : pour les règles métier numérotées
   (CA-XXX, DON-XXX, etc.) qui précisent le comportement exact.

Si aucun test RED n'est trouvé → demande le périmètre à l'utilisateur, puis
invoque `/test-strategy` en mode RED pour générer les tests d'abord.

### Étape 1 — Lecture des conventions projet

**Avant de planifier**, analyse les conventions en place pour ne pas les violer :

1. Lis `CLAUDE.md` → règles critiques (cookies SSR, documentId, logging, imports monorepo, accents)
2. Lis un controller existant proche du domaine → relève le style (gestion d'erreurs,
   format de réponse, logging)
3. Lis `config/permissions.json` → comprendre le schéma de déclaration des permissions
4. Lis un schema `content-types/*/schema.json` existant → relever les conventions
   (draftAndPublish, relations, enums)
5. Regarde si des services similaires existent déjà (`src/api/*/services/`) → DRY check

Documente ce que tu as trouvé dans ton plan avant de coder.

### Étape 2 — Questions OBLIGATOIRES avant d'implémenter

Pose via `AskUserQuestion` AVANT toute écriture de code :

1. **Périmètre confirmé** — liste les fichiers de tests RED détectés et demande
   confirmation.
2. **Stack** — Backend seul / Frontend seul / Full-stack → calibre le découpage en unités.
3. **Services tiers impliqués ?** — Stripe (→ charge `stripe-embedded`), email
   (→ Mailgun, `EMAIL_TEST_MODE`), WebSocket ? Identifie les dépendances externes
   pour les mocker correctement en test.

### Étape 3 — Plan d'implémentation

Produis un plan structuré avant de spawner les agents :

1. **DRY check** — avant de créer un fichier, cherche si la logique existe déjà
   (`grep -r "validateAmount\|minimumAmount" src/`, middleware d'auth similaire,
   pattern de réponse identique dans un controller voisin). Si oui → réutilise ou
   étends, ne duplique pas.
2. **Cartographie** — pour chaque domaine couvert par les tests, dresse la liste des
   fichiers à créer par couche en suivant `references/cartographie-conventions.md`
   (tables Backend Strapi v5 et Frontend Next.js, règles non négociables, SOLID checks).

### Étape 4 — Implémentation

Découpe le périmètre (étape 3) en **unités** = tranches couche × domaine
(`cartographie-conventions.md`) indépendantes si elles ne partagent aucun fichier de
logique.

- **1 seule unité** → implémente-la directement en suivant `references/patterns-activcreew.md`
  et les skills de domaine (`strapi-routes`, `nextjs-component`, `french-accents`…),
  SOLID + DRY, déclare les nouvelles routes dans `permissions.json`.
- **≥ 2 unités indépendantes** → **déroule `references/supervision.md`** : tu deviens
  superviseur (tu ne codes pas), un worktree + un sous-agent frais par unité, contrôle
  de conformité par un 2e agent avant chaque merge, MR vers `feat/<chantier>` seulement,
  jamais vers `dev`.

QA final (une fois toutes les unités livrées) : `yarn tsc --noEmit` dans `Strapi v5/`
et `pnpm build` dans `frontend/` → 0 erreur ; `./scripts/run-affected-tests.sh` →
tous GREEN.

### Étape 5 — Validation GREEN globale (après agrégation)

Cette étape est la vérification d'ensemble **une fois les unités mergées sur
`feat/<chantier>`** — pas l'endroit où le superviseur écrit du code d'unité (ça se
passe dans les sous-agents, cf. `supervision.md`). En périmètre 1 unité, elle suit
directement l'implémentation directe.

Pour chaque fichier de test RED :

1. Lance `yarn test <chemin>` (Strapi) ou `pnpm exec playwright test <spec>` (front)
2. Si un test échoue → **corrige le code de prod**, jamais le test
3. Si l'échec est un problème de setup/import → corrige le setup sans toucher
   au comportement attendu
4. Répète jusqu'au vert complet

> **Règle absolue** (mémoire `feedback_tdd_plan_wins`) : le test gagne sur le code.
> Ne jamais proposer "retirer du scope" un test qui échoue.

### Étape 6 — Résumé de fin de chantier

Termine par un récap structuré : conventions respectées (lecture CLAUDE.md, DRY check),
fichiers créés/modifiés avec liens et rôle SOLID, résultat des tests (X/Y unitaires,
intégration, E2E — GREEN ou ⏳ si Docker/app requis), permissions ajoutées, prochaines
étapes.

## Ce qu'il ne faut jamais faire (propre à ce maillon)

- Modifier un fichier de test pour le faire passer, ou proposer "retirer du scope" un
  test qui échoue — le test est la vérité
- Mettre de la logique métier dans un controller (SRP) ; laisser la logique dupliquée
  au lieu de la centraliser dans un service unique consommé par l'UI ET les interfaces
  machine (tools MCP, API)
- Hand-off vers `ux-ui-strategy` avant le GREEN complet + build + E2E réel
- Merger une unité vers `dev` (builds Coolify) — MR vers `feat/<chantier>` uniquement

(Règles Strapi v5 — `strapi.documents()` en écriture, `documentId` jamais `id`, Knex en
lecture seule — et accents TSX : dans `CLAUDE.md` + `cartographie-conventions.md`.)

## Évolution de ce skill

- Nouveau pattern de code éprouvé → `references/patterns-activcreew.md`.
- Nouvelle règle projet ou couche → `references/cartographie-conventions.md`.
- Nouveau point de protocole de délégation → `references/supervision.md`.
- Ne modifier ce SKILL.md que si l'orchestration (étapes) change.
