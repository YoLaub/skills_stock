---
name: test-strategy
description: >
  Expert en stratégie de test et automatisation basé sur la Pyramide des Tests,
  spécialisé pour le monorepo ActivCreew. Utilise ce skill dès que l'utilisateur
  demande d'écrire, générer, améliorer ou revoir des tests (unitaires, intégration,
  E2E, charge), de mettre en place une stratégie de test, du TDD, de la couverture
  de code, du mutation testing, ou de configurer un pipeline CI/CD avec quality
  gates. Se déclenche IMPÉRATIVEMENT quand l'utilisateur mentionne des specs
  Gherkin / fichiers .feature / BDD, ou veut "générer les tests" depuis une spec.
  Se déclenche aussi quand l'utilisateur soumet du code à tester, demande une revue
  de testabilité, veut réduire le flakiness, ou mentionne Jest, Vitest, Pytest,
  Playwright, Cypress, k6, GitHub Actions, GitLab CI. Même sans le mot "test", si
  le code manque de tests ou qu'il demande de la fiabilité/qualité, propose
  proactivement une stratégie de test adaptée.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: python3 "${CLAUDE_PLUGIN_ROOT}/hooks/gate.py" hook open coherence@docs/maquettes
          once: true
    - matcher: "Edit|Write|MultiEdit|NotebookEdit|Bash"
      hooks:
        - type: command
          command: python3 "${CLAUDE_PLUGIN_ROOT}/hooks/gate.py" hook guard
  Stop:
    - hooks:
        - type: command
          command: python3 "${CLAUDE_PLUGIN_ROOT}/hooks/gate.py" hook stop
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

## Portes de vérification (non négociables en mode Génération)

Celui qui écrit les tests ne décide pas qu'ils sont bons. Deux portes, chacune tenue
par un agent frais qui n'a rien écrit — et par des hooks (`hooks/gate.py` du plugin) :
tant qu'une phase ouverte n'a pas de verdict `PASS` sur l'état exact du dépôt, la
skill ne peut pas conclure.

| Porte | Quand | Agent | Si FAIL |
|---|---|---|---|
| `coherence` | étape 0, si une maquette existe — **avant** d'écrire un test | `maquette-spec-coherence` | corriger les specs, relancer ; un conflit → l'utilisateur |
| `red` / `green` | étape 3, après exécution | `spec-conformity-gate` | compléter les tests manquants, relancer |

Chemin de l'outil : `${CLAUDE_PLUGIN_ROOT}/hooks/gate.py` (à passer tel quel aux
agents). `gate.py status` montre où on en est. Si un PASS est hors d'atteinte (conflit
à arbitrer, spec ambiguë), rendre la main : `gate.py escalate <phase> "<raison>"`, et
le dire en toutes lettres — une escalade n'est pas une validation. Deux FAIL de suite
sur le même point → escalade, pas de troisième tour.

## ⚡ Orchestration (mode Génération)

Objectif : en **une seule invocation**, passer d'une spec à des tests générés,
routés au bon endroit, et exécutés. Suis ces étapes DANS L'ORDRE.

### Étape 0 — Détecter les specs Gherkin

Cherche les fichiers `docs/gherkin/**/*.feature` (Glob).

- **Specs présentes** → mode **Gherkin** : ces `.feature` sont la source de vérité
  du comportement attendu. Lis-les, extrais Scenarios + Examples, et génère les
  tests correspondants. Ne demande PAS la zone à couvrir (elle est dans les specs).
- **Aucune spec** → mode **Couverture** : invoque le skill `test-planner` pour
  établir la matrice de couverture (parcours USER/Admin, objectif ~80%), PUIS
  demande à l'utilisateur quelle zone couvrir (cf. Étape 1).

**Porte `coherence`** — si une maquette couvre le périmètre (`docs/maquettes/**`),
lancer `maquette-spec-coherence` (maquette, specs, `--scope` = dossiers maquette +
specs) **avant toute génération**. Des tests écrits sur une spec qui contredit la
maquette figent l'erreur : on corrige d'abord les specs (orphelins, écarts de mots),
on remonte les conflits à l'utilisateur, puis on relance l'agent jusqu'au `PASS`.

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

Dès la réponse connue, ouvrir la phase correspondante :
`python3 "${CLAUDE_PLUGIN_ROOT}/hooks/gate.py" open red` (ou `open green`).

### Étape 2 — Router et générer les tests

Mappe chaque Scenario / zone vers son niveau et écris le fichier au bon endroit :

| Niveau         | Emplacement                              | Outil    |
|----------------|------------------------------------------|----------|
| Unitaire       | `Strapi v5/tests/unit/<domaine>/`        | Jest     |
| Intégration    | `Strapi v5/tests/integration/<domaine>/` | Jest     |
| Charge (load)  | `Strapi v5/tests/load/` (k6 → `k6/scenarios/`) | k6/Jest |
| E2E            | `frontend/tests/e2e/`                    | Playwright |

Conventions de mapping Gherkin (tags `@unit/@integration/@e2e/@load`, sous-dossiers,
ou inférence) : voir `references/gherkin-mapping.md`.

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
  laisse le code de prod intact.

**Porte `red` / `green`** — ton propre constat ne suffit pas. Lancer
`spec-conformity-gate` (mode `red` ou `green`, sources de spec, fichiers de test,
commandes, chemin de `gate.py`). En RED, il vérifie qu'**un test existe par
Scenario / ligne d'Examples / CA**, qu'il échoue sur une assertion métier, et il
**verrouille** les tests validés : `dev-strategy` ne pourra plus les modifier. `FAIL` →
compléter exactement les manques qu'il liste, relancer l'agent.

Détecte les noms de services Docker avant tout `docker compose` (`docker compose
config --services` → `postgres-test`, `redis-test`). Pour le mapping des tests
affectés, voir `Strapi v5/tests/test-map.json` et `/validate-tests`.

### Résumé de fin de chantier

Termine toujours par un récap : fichiers créés (avec liens), niveau de chacun,
mode red/green, résultat d'exécution (X passed / Y failed / Z skipped), **verdict de
chaque porte tel qu'enregistré** (`gate.py status` — PASS, ou escalade et pourquoi),
et prochaines étapes. Jamais « terminé » sans PASS.

## Évolution de ce skill

- Nouveau pattern de test par niveau → le fichier `references/` du niveau concerné.
- Nouveau principe générique → `references/mode-conseil.md`.
- Nouveau domaine du repo → la liste de l'étape 1.
- Règle de porte (verdict, verrou, escalade) → `hooks/gate.py` du plugin + ses tests.
- Ne modifier la structure de ce SKILL.md que si l'orchestration elle-même change.
