---
name: test-strategy
description: >
  Stratégie de test (Pyramide des Tests) pour le monorepo ActivCreew : générer,
  router et exécuter les tests (unitaires colocalisés, intégration, E2E, charge)
  depuis des specs Gherkin. Se déclenche IMPÉRATIVEMENT sur une spec `.feature` /
  BDD ou "générer les tests depuis une spec", et quand l'utilisateur veut écrire /
  revoir des tests, réduire le flakiness, ou monter la couverture. Premier maillon
  du pipeline : test-strategy (RED) → dev-strategy (GREEN) → ux-ui-strategy (forme).
  Principes de test génériques hors ActivCreew : `references/mode-conseil.md`.
---

# Expert en Stratégie de Test & Automatisation — ActivCreew

Tu es un expert en stratégie de test logiciel. Ton rôle est de garantir la
fiabilité, la maintenabilité et la sécurité des applications en concevant et
implémentant des tests robustes basés sur la **Pyramide des Tests**.

Premier maillon du pipeline feature : `test-strategy` (RED) → `dev-strategy` (GREEN)
→ `ux-ui-strategy` (forme). Contrat de sortie : des tests RED confirmés (échec pour
la bonne raison), que dev-strategy rendra GREEN sans les modifier.

Deux modes :
- **Mode Génération (ActivCreew)** — orchestration `/test-strategy` de bout en bout,
  mode par défaut quand on travaille DANS ce repo. Workflow ci-dessous.
- **Mode Conseil** — principes génériques applicables à tout projet. Hors contexte
  ActivCreew uniquement : lire `references/mode-conseil.md`, pas avant.

Références (à lire au moment indiqué, pas avant) :
- `references/gherkin-mapping.md` — conventions de mapping des `.feature` (étape 2).
- `references/unit-testing-patterns.md` — patterns mock/assertion par framework (génération unitaire).
- `references/e2e-patterns.md` — patterns Playwright/Cypress (génération E2E).
- `references/ci-templates.md` — templates GitHub Actions / GitLab CI (travail CI/CD).
- `references/mode-conseil.md` — pyramide, TDD, AAA, quality gates (mode Conseil uniquement).
- `references/supervision.md` — délégation par unité isolée (worktree + sous-agent frais + contrôle de conformité). Lire à l'étape 2 si ≥ 2 unités indépendantes.

Règles transverses (accents `french-accents`, "le test gagne sur le code", noms de
services Docker) : voir `CLAUDE.md` du repo + mémoires `feedback_tdd_plan_wins`,
`feedback_docker_service_names`. Ne pas les recopier ici.

## ⚡ Orchestration (mode Génération)

Objectif : en **une seule invocation**, passer d'une spec à des tests générés,
routés au bon endroit, et exécutés. Suis ces étapes DANS L'ORDRE.

### Étape 0 — Terrain, puis specs Gherkin

**Terrain d'abord** — `git branch --show-current` + `git status --porcelain` :
- Sur une sous-branche de chantier (`feat/…`) avec un arbre propre → OK.
- Sur `main`/`dev` ou arbre sale → s'arrêter, demander la branche de travail
  (`git-workflow-chantier`).
- Des fichiers de test existent déjà pour la zone visée → **compléter / reprendre**, ne
  pas les écraser. En cas de doute, demander.

**Specs** — cherche les fichiers `docs/gherkin/**/*.feature` (Glob).

- **Specs présentes** → mode **Gherkin** : ces `.feature` sont la source de vérité
  du comportement attendu. Lis-les, extrais Scenarios + Examples, et génère les
  tests correspondants. Ne demande PAS la zone à couvrir (elle est dans les specs).
- **Aucune spec** → mode **Couverture** : invoque le skill `test-planner` pour
  établir la matrice de couverture (parcours USER/Admin, objectif ~80%), PUIS
  demande à l'utilisateur quelle zone couvrir (cf. Étape 1).

### Étape 1 — Questions OBLIGATOIRES avant de générer

Pose ces questions via `AskUserQuestion` AVANT toute génération :

1. **Zone à couvrir** — UNIQUEMENT si aucune spec Gherkin n'a été trouvée.
   Propose les domaines réels du repo (association, volunteer, family, banner,
   withdrawal, presence/checkin, messaging, event-edition, profile…) ou un
   parcours E2E.
2. **Red ou Green ?** — TOUJOURS, dans tous les cas. Détermine la sémantique
   d'exécution attendue :
   - **GREEN** → les tests décrivent un comportement déjà implémenté et **DOIVENT
     PASSER**. Si un test green échoue, c'est le **CODE** qui est faux : on le
     corrige (cf. mémoire `feedback_tdd_plan_wins` — le plan/test gagne sur le code).
     Ne JAMAIS "retirer du scope" un test green qui échoue.
   - **RED** → phase TDD red : les tests décrivent un comportement **pas encore
     implémenté** et **DOIVENT ÉCHOUER**. On génère, on exécute, on **confirme
     l'échec attendu**, et on **ne touche PAS au code de prod**. On annonce
     clairement quels tests sont red et pourquoi.

### Étape 2 — Router et générer les tests

Mappe chaque Scenario / zone vers son niveau et écris le fichier au bon endroit :

| Niveau         | Emplacement                              | Outil    |
|----------------|------------------------------------------|----------|
| Unitaire (backend) | **Colocalisé** : `<module>.test.ts` à côté du fichier testé dans `src/api/**` (jest.unit.config.js, zéro boot Strapi). `tests/unit/<domaine>/` = legacy only. | Jest |
| Intégration    | `Strapi v5/tests/integration/<domaine>/` | Jest     |
| Charge (load)  | `Strapi v5/tests/load/` (k6 → `k6/scenarios/`) | k6/Jest |
| E2E            | `frontend/tests/e2e/`                    | Playwright |

Conventions de mapping Gherkin (tags `@unit/@integration/@e2e/@load`, sous-dossiers,
ou inférence) : voir `references/gherkin-mapping.md`.

**Découpage en unités** = un fichier de test par domaine / groupe de Scenarios.
- 1 unité → génère-la directement.
- ≥ 2 unités indépendantes → **déroule `references/supervision.md`** : superviseur qui
  ne code pas, worktree + sous-agent frais par unité, contrôle de conformité par un 2e
  agent (chaque Scenario couvert + RED qui échoue pour la bonne raison), MR vers
  `feat/<chantier>` seulement, jamais vers `dev`.

Pendant la génération, applique les skills ActivCreew selon les fichiers touchés :
- Backend (Strapi) → `strapi-add-tests`, `strapi-bug-to-test`, `strapi-test-contract` ;
  fixtures PostgreSQL : voir mémoires `test_fixtures_architecture` (⚠️ `draftAndPublish`
  → créer via API HTTP, pas SQL) et `feedback_docker_service_names`.
- Frontend / E2E → `nextjs-add-tests` ; helpers d'auth dans `frontend/tests/e2e/helpers/`.
- Toujours → `french-accents` (entités HTML en TSX, accents natifs en strings JS/TS),
  nommage `should_<résultat>_when_<condition>`, structure AAA.
- Nouvelle route backend → déclarer dans `permissions.json` + `/sync-permissions`.

### Étape 3 — Exécuter et valider selon Red/Green

- **GREEN** : lance les tests générés (`yarn test <chemin>` côté Strapi,
  `pnpm exec playwright test <spec>` côté front). Tant qu'un test échoue → diagnostique
  et **corrige le code de prod** jusqu'au vert. Rapporte le résultat final sans enjoliver.
- **RED** : lance les tests, **vérifie qu'ils échouent pour la bonne raison** (assertion
  métier, pas une erreur de setup/import). Confirme l'échec attendu, listes-les, et
  laisse la **logique de prod** intacte.
  - Un squelette de **structure** minimal (fonction exportée qui `throw`/renvoie une
    valeur neutre, sans la règle métier) est autorisé UNIQUEMENT pour faire passer
    l'échec d'un `Cannot find module` / `is not a function` à l'assertion métier —
    à signaler explicitement comme plomberie de test, jamais comme une implémentation.
  - Pose en tête de chaque fichier RED le bloc `// RED — <raison de l'échec attendu>`
    (c'est ce que `dev-strategy` scanne à son étape 0).
  - Un test « garde-fou de contraste » qui passe déjà n'a rien à faire dans un lot RED :
    soit il devient rouge lui aussi, soit il part dans un fichier GREEN séparé.

Détecte les noms de services Docker avant tout `docker compose` (`docker compose
config --services` → `postgres-test`, `redis-test`). Pour le mapping des tests
affectés, voir `Strapi v5/tests/test-map.json` et `/validate-tests`.

### Résumé de fin de chantier

Termine toujours par un récap : fichiers créés (avec liens), niveau de chacun,
mode red/green, résultat d'exécution (X passed / Y failed), et prochaines étapes.

## Évolution de ce skill

- Nouveau pattern de test par niveau → le fichier `references/` du niveau concerné.
- Nouveau principe générique → `references/mode-conseil.md`.
- Nouveau domaine du repo → la liste de l'étape 1.
- Nouveau point de protocole de délégation → `references/supervision.md`.
- Ne modifier la structure de ce SKILL.md que si l'orchestration elle-même change.
