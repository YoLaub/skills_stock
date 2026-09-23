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
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: python3 "${CLAUDE_PLUGIN_ROOT}/hooks/gate.py" hook open green coherence@docs/maquettes
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

## Portes de vérification (non négociables)

**Aucun worker ne décide que son travail est fini, et le Team Lead non plus.** Un
worker rend « prêt pour vérification » ; « terminé » n'existe qu'après un verdict
`PASS` d'un agent frais qui n'a rien codé. Des hooks (`hooks/gate.py` du plugin) le
tiennent mécaniquement : phases `green` (et `coherence` si une maquette existe)
ouvertes à l'invocation, conclusion bloquée tant qu'elles n'ont pas de `PASS` sur
l'état exact du dépôt ; tests verrouillés au RED non modifiables.

| Porte | Quand | Agent |
|---|---|---|
| `coherence` | étape 0, si maquette — **avant** de coder | `maquette-spec-coherence` |
| `red` | étape 0, si les tests RED n'ont pas de verdict sur cette branche | `spec-conformity-gate` (mode red) |
| `green` | étape 5, après le vert | `spec-conformity-gate` (mode green) |

Outil : `${CLAUDE_PLUGIN_ROOT}/hooks/gate.py` (chemin à passer aux agents) ;
`gate.py status` pour l'état. Sur `FAIL` : renvoyer au worker concerné **la liste
exacte** des manques, puis relancer la porte. Deux `FAIL` de suite sur le même point →
`gate.py escalate green "<raison>"` et le dire à l'utilisateur : une escalade n'est pas
une validation.

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

**Portes d'entrée** (`gate.py status`) :
- **Maquette présente et `coherence` sans PASS** → lancer `maquette-spec-coherence`.
  Si specs et maquette divergent, on ne code pas : corriger les specs (et les tests
  RED qui en dépendent, via `test-strategy`), remonter les conflits à l'utilisateur,
  relancer jusqu'au `PASS`.
- **Tests RED sans verdict `red` sur la branche** (écrits hors porte) → lancer
  `spec-conformity-gate` en mode red : il vérifie qu'ils couvrent la spec et les
  **verrouille**. Un scénario sans test → retour à `test-strategy`, pas de code.

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
- Finir sur un rapport « prêt pour vérification » : fichiers touchés, critères
  (Scenario / CA) visés, commandes lancées et résultat brut. Jamais « terminé ».

**QA Checker** (boucle rapide interne — ce n'est **pas** la porte : il fait partie de
l'équipe qui a codé) :
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
> Ne jamais proposer "retirer du scope" un test qui échoue. Les tests verrouillés au
> RED sont protégés par hook : une tentative d'édition est refusée.

**Porte `green`** — le vert du QA Checker ne suffit pas : des tests verts prouvent que
le code écrit fonctionne, pas qu'il couvre tout ce que la spec demande. Lancer
`spec-conformity-gate` en mode green (sources Gherkin + `CA-XXX`, fichiers de test,
commandes de suite + build + lint, chemin de `gate.py`). Il refait la grille critère
par critère, rejoue tout, compte les skippés. `FAIL` → renvoyer les workers concernés
sur la liste exacte, relancer la porte. On ne passe à l'étape 6 qu'avec un `PASS`.

### Étape 6 — Résumé de fin de chantier

Termine par un récap structuré : conventions respectées (lecture CLAUDE.md, DRY check),
fichiers créés/modifiés avec liens et rôle SOLID, résultat des tests (X/Y unitaires,
intégration, E2E — GREEN ou ⏳ si Docker/app requis, **skippés comptés**), permissions
ajoutées, **verdict des portes tel qu'enregistré** (`gate.py status` : PASS, ou
escalade et sa raison), prochaines étapes. Un E2E ⏳ non rejoué par la porte n'est pas
vert.

## Ce qu'il ne faut jamais faire

- Modifier un fichier de test pour le faire passer — le test est la vérité
- Créer une fonction qui existe déjà ailleurs dans le codebase (DRY)
- Mettre de la logique métier dans un controller (SRP)
- Utiliser `strapi.entityService` (déprécié → `strapi.documents()`)
- Utiliser `strapi.db.connection` (Knex) pour des écritures (lifecycles non déclenchés)
- Utiliser `id` au lieu de `documentId` pour les opérations Strapi v5
- Mettre des accents natifs dans du JSX/TSX (→ `&eacute;` etc., skill `french-accents`)
- Proposer "retirer du scope" quand un test échoue
- Déclarer la feature terminée sur la foi d'un worker ou du QA Checker — seul un
  verdict `PASS` de `spec-conformity-gate` la clôt
- Contourner un hook de porte (écrire dans `.claude/gates/`, modifier un test
  verrouillé par un autre chemin)

## Évolution de ce skill

- Nouveau pattern de code éprouvé → `references/patterns-activcreew.md`.
- Nouvelle règle projet ou couche → `references/cartographie-conventions.md`.
- Règle de porte (verdict, verrou, escalade) → `hooks/gate.py` du plugin + ses tests.
- Ne modifier ce SKILL.md que si l'orchestration (étapes, équipe) change.
