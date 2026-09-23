---
name: dev-strategy
description: >
  Stratégie d'implémentation TDD GREEN pour ActivCreew. Orchestre la phase de
  développement à partir de specs Gherkin et/ou tests RED existants. Utilise ce
  skill dès que l'utilisateur veut implémenter une feature, passer des tests RED
  au vert, ou demande "dev-strategy", "implementer", "coder la feature",
  "faire passer les tests", "phase GREEN", "TDD green". Se déclenche aussi
  quand une branche contient des tests qui échouent et que le code de prod est
  manquant. Fonctionne en binôme avec test-strategy : test-strategy génère les
  tests RED, dev-strategy les rend GREEN.
---

# Expert en Stratégie d'Implémentation TDD GREEN — ActivCreew

Tu es un expert en développement logiciel guidé par les tests. Ton rôle est de
**faire passer des tests RED au vert** en implémentant le code de production
minimal, correct et maintenable — sans jamais toucher aux tests eux-mêmes.

Deuxième maillon du pipeline feature : `test-strategy` (RED) → `dev-strategy` (GREEN)
→ `ux-ui-strategy` (forme). Contrat d'entrée : des tests RED confirmés. Contrat de
sortie : tests GREEN, `data-testid` et permissions en place, prêt pour l'habillage.

Références (à lire au moment indiqué, pas avant) :
- `references/principes-solid-dry.md` — SOLID, DRY, code reviewable. Lire avant l'étape 3.
- `references/cartographie-conventions.md` — fichiers par couche (Backend/Frontend) + règles non négociables. Lire à l'étape 3.
- `references/patterns-activcreew.md` — patterns de code éprouvés (schema, service pur, controller, webhook…). Lire à l'étape 4, append-only.

## ⚡ Workflow dev-strategy (orchestration)

Objectif : en **une seule invocation**, analyser les tests RED, lire les conventions
du projet, planifier, implémenter, et valider le GREEN. Suis ces étapes DANS L'ORDRE.

### Étape 0 — Détection du périmètre

Cherche dans cet ordre :

1. **Tests RED** — `Strapi v5/tests/**/*.test.js` et `frontend/tests/e2e/**/*.spec.ts`
   contenant `Ces tests sont des tests RED` ou `// RED`.
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
2. **Stack** — Backend seul / Frontend seul / Full-stack → calibre l'équipe d'agents.
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

### Étape 4 — Implémentation par équipe d'agents

Structure l'équipe selon le périmètre (étape 3) :

```
Team Lead (coordination uniquement — ne code pas)
  ├── Worker Backend 1 — Schema + Services purs         (Sonnet, parallèle)
  ├── Worker Backend 2 — Routes + Controllers           (Sonnet, parallèle)
  ├── Worker Backend 3 — Lifecycles + Permissions       (Sonnet, après Backend 2)
  ├── Worker Frontend  — Composants + Hooks + Pages     (Sonnet, parallèle avec Backend)
  └── QA Checker       — build TS + lint + tests        (en dernier, après tous)
```

**Contrat de chaque worker** :
- Lire les conventions projet avant d'écrire (étape 1 ci-dessus)
- Suivre les patterns de `references/patterns-activcreew.md` et les skills de son
  domaine (`strapi-routes`, `nextjs-component`, `french-accents`…)
- Appliquer SOLID et DRY : vérifier que la logique n'existe pas ailleurs avant de la créer
- Ne pas toucher aux fichiers des autres workers
- Déclarer les nouvelles routes dans `permissions.json`

**QA Checker** :
- `yarn tsc --noEmit` dans `Strapi v5/` → 0 erreurs
- `pnpm build` dans `frontend/` → 0 erreurs
- `yarn test tests/unit/<domaine>/` → tous GREEN
- `yarn test tests/integration/<domaine>/` → tous GREEN (si Docker dispo)

### Étape 5 — Exécution et validation GREEN

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

## Ce qu'il ne faut jamais faire

- Modifier un fichier de test pour le faire passer — le test est la vérité
- Créer une fonction qui existe déjà ailleurs dans le codebase (DRY)
- Mettre de la logique métier dans un controller (SRP)
- Utiliser `strapi.entityService` (déprécié → `strapi.documents()`)
- Utiliser `strapi.db.connection` (Knex) pour des écritures (lifecycles non déclenchés)
- Utiliser `id` au lieu de `documentId` pour les opérations Strapi v5
- Mettre des accents natifs dans du JSX/TSX (→ `&eacute;` etc., skill `french-accents`)
- Proposer "retirer du scope" quand un test échoue

## Évolution de ce skill

- Nouveau pattern de code éprouvé → `references/patterns-activcreew.md`.
- Nouvelle règle projet ou couche → `references/cartographie-conventions.md`.
- Ne modifier ce SKILL.md que si l'orchestration (étapes, équipe) change.
