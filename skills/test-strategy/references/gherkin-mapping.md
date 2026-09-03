# Mapping Gherkin → Tests (ActivCreew)

Comment transformer un fichier `docs/gherkin/**/*.feature` en tests générés et
routés au bon endroit. Utilisé par le **Mode Génération** du skill `test-strategy`.

---

## 1. Déterminer le niveau de chaque Scenario

Ordre de priorité pour décider du niveau (unit / integration / e2e / load) :

### a. Tag explicite (prioritaire)

Un tag sur la `Feature` ou le `Scenario` force le niveau :

```gherkin
@integration @domaine:association
Feature: Rejoindre une association

  @e2e
  Scenario: Un bénévole accepte une invitation depuis l'UI
    ...
```

Tags reconnus : `@unit`, `@integration`, `@e2e`, `@load`.
Tag de domaine optionnel : `@domaine:<nom>` (ex. `@domaine:withdrawal`) → choisit
le sous-dossier de destination.

### b. Sous-dossier de `docs/gherkin/`

Si pas de tag, le sous-dossier porte le niveau :

```
docs/gherkin/
  unit/...
  integration/...
  e2e/...
  load/...
```

### c. Inférence (dernier recours)

Si ni tag ni sous-dossier ne tranchent, déduis depuis la nature du scénario :

| Indices dans le scénario                                   | Niveau       |
|------------------------------------------------------------|--------------|
| Logique pure, calcul, validation, transformation, edge case| unitaire     |
| Appel API + DB/Redis, contrat de route, lifecycle, policy  | intégration  |
| Parcours navigateur, clics, navigation multi-pages, login  | e2e          |
| Débit, concurrence, rush stock, N utilisateurs simultanés  | charge (load)|

En cas de doute réel, demande à l'utilisateur — ne devine pas en silence.

---

## 2. Emplacement de sortie

| Niveau       | Fichier généré                                            |
|--------------|-----------------------------------------------------------|
| Unitaire     | **Colocalisé** : `Strapi v5/src/api/<module>/services/<x>.test.ts` à côté du code testé (jest.unit.config.js). `tests/unit/<domaine>/` = legacy uniquement. |
| Intégration  | `Strapi v5/tests/integration/<domaine>/<feature>.test.js` |
| Charge       | `Strapi v5/tests/load/k6/scenarios/<feature>.js` (k6) ou `Strapi v5/tests/load/<feature>.js` |
| E2E          | `frontend/tests/e2e/<feature>.spec.ts`                    |

`<domaine>` = un des dossiers existants : `association`, `volunteer`, `family`,
`banner`, `withdrawal`, `presence`/`checkin`, `messaging`, `event-edition`,
`profile`, `auth`, `responsibility`, `assignment`. Réutilise un dossier existant
plutôt que d'en créer un nouveau.

---

## 3. Traduire la structure Gherkin → AAA

| Gherkin               | Test                                            |
|-----------------------|-------------------------------------------------|
| `Feature`             | `describe('<Feature>')`                          |
| `Scenario`            | `it('should_… when_…')` (nommage explicite)      |
| `Background`          | `beforeEach` (fixtures, seed, auth)              |
| `Given`               | **Arrange** (setup, fixtures, état initial)      |
| `When`                | **Act** (l'action testée)                        |
| `Then` / `And` / `But`| **Assert** (`expect(...).toBe(...)` précis)      |
| `Scenario Outline` + `Examples` | `it.each([...])` / `test.describe.parallel` paramétré |

Garde la phrase Gherkin en commentaire au-dessus du bloc correspondant pour la
traçabilité spec → test.

---

## 4. Sémantique Red / Green (demandée à l'Étape 1)

- **GREEN** — comportement déjà implémenté → le test **doit PASSER**. Échec ⇒ le
  code est faux, on le corrige (cf. mémoire `feedback_tdd_plan_wins`). Ne jamais
  affaiblir l'assertion ni retirer le test du scope.
- **RED** — comportement pas encore implémenté → le test **doit ÉCHOUER** sur une
  assertion métier (pas sur un import/setup cassé). On confirme l'échec, on ne
  touche pas au code de prod. Optionnel : marquer avec un commentaire `// RED:
  attendu tant que <feature> n'est pas implémentée` (ne pas utiliser `.skip`,
  sinon le test ne s'exécute pas et ne prouve rien).

Un même `.feature` peut contenir des scénarios green ET red ; le tag/réponse
s'applique scénario par scénario si l'utilisateur le précise.

---

## 5. Rappels ActivCreew critiques pour la génération

- **Fixtures PostgreSQL** : entité `draftAndPublish: true` → créer via API HTTP,
  pas en SQL direct (sinon `findMany/findOne` renvoie 0). Voir mémoire
  `test_fixtures_architecture`.
- **documentId** (UUID), jamais `id`, pour tout CRUD Strapi v5.
- **Cookies SSR** : tout fetch Next→Strapi en SSR transmet `cookies().toString()`.
- **Services Docker** : `docker compose config --services` avant tout restart
  (`postgres-test`, `redis-test`). Voir `feedback_docker_service_names`.
- **moduleNameMapper Jest** : `^@workspace/kernel/(.*)$` AVANT le catch-all.
  Voir `feedback_jest_workspace_mapping`.
- **Assertions texte** : jsdom décode les entités HTML → préférer
  `toMatch(/pattern/i)` à `toContain('chaîne exacte')` pour les textes accentués.
- **E2E** : sélecteurs `data-testid`, waits explicites (jamais `sleep`), helpers
  d'auth dans `frontend/tests/e2e/helpers/`, nettoyage via `scripts/seed-e2e.js --cleanup`.
