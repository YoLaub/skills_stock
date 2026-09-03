# Mode Conseil — socle générique de stratégie de test

À lire uniquement en mode Conseil (hors orchestration ActivCreew) : principes de la
Pyramide des Tests, TDD, CI/CD et workflow de réponse applicables à tout projet.

## Principes fondamentaux

### 1. Approche Test-First (TDD)

Propose systématiquement une approche TDD quand le contexte le permet :

1. **Red** — Écrire un test qui échoue et qui décrit le comportement attendu
2. **Green** — Écrire le code minimal pour faire passer le test
3. **Refactor** — Nettoyer le code tout en gardant les tests verts

Si l'utilisateur fournit du code existant sans tests, commence par analyser
sa testabilité avant d'écrire les tests. Si le code n'est pas testable en l'état
(couplage fort, effets de bord, pas d'injection de dépendances), propose d'abord
une refactorisation ciblée, explique pourquoi, puis écris les tests.

### 2. Structure AAA obligatoire

Organise chaque test selon la structure **Arrange → Act → Assert** :

```
// Arrange — Préparer les données et dépendances
// Act — Exécuter l'action à tester
// Assert — Vérifier le résultat
```

### 3. Nommage explicite

Chaque test doit porter un nom qui décrit le comportement attendu et le contexte.
Le pattern recommandé est : `should_<résultat>_when_<condition>`

**Exemples :**
- `should_return_400_when_email_is_invalid`
- `should_create_user_when_all_fields_are_valid`
- `should_throw_timeout_error_when_api_is_unreachable`

### 4. Code testable

Écrire du code testable signifie appliquer ces principes :
- **Injection de dépendances** — Ne jamais instancier les dépendances en dur
- **Fonctions pures** — Privilégier les fonctions sans effets de bord
- **Séparation des préoccupations** — Un module = une responsabilité
- **Interfaces explicites** — Des contrats clairs entre modules

## La Pyramide des Tests

Applique la pyramide dans cet ordre de priorité. Commence toujours par la base
(unitaires) puis remonte vers le sommet (E2E). Le ratio cible est environ
70% unitaires / 20% intégration / 10% E2E.

### Niveau 1 : Tests Unitaires (le socle)

C'est la fondation. Ils sont rapides, isolés, et nombreux.

**Quand les écrire :**
- Logique métier et règles de gestion
- Algorithmes et transformations de données
- Validations et cas limites (edge cases)
- Fonctions utilitaires

**Comment les écrire :**
- Isoler via le mocking des dépendances externes (DB, API, filesystem)
- Tester les cas nominaux ET les cas limites (null, vide, overflow, formats invalides)
- Viser une couverture pertinente : couvrir les branches critiques, pas juste le %
- Envisager le mutation testing pour valider la qualité des assertions

**Détection du framework :**
Avant d'écrire des tests, inspecte le projet pour déterminer le stack :
- `package.json` → Jest, Vitest, Mocha
- `pyproject.toml` / `setup.cfg` / `requirements.txt` → Pytest, unittest
- `pom.xml` / `build.gradle` → JUnit, Mockito
- `Package.swift` / `*.xcodeproj` → XCTest
- Si rien n'est détecté, demande à l'utilisateur ou recommande le choix le plus
  adapté au langage du projet

Pour les patterns de mocking et d'assertion spécifiques à chaque framework,
consulte `unit-testing-patterns.md`.

### Niveau 2 : Tests d'Intégration

Vérifient que les modules communiquent correctement entre eux.

**Quand les écrire :**
- Communication API ↔ Base de données
- Appels entre microservices
- Intégration avec des services tiers (paiement, auth, stockage)
- Migrations de base de données

**Comment les écrire :**
- Utiliser des conteneurs éphémères (Testcontainers) pour des environnements réalistes
- Tester les contrats d'interface (requêtes/réponses attendues)
- Vérifier la gestion des erreurs réseau (timeout, retry, circuit breaker)
- Valider l'intégrité des données à travers les couches

### Niveau 3 : Tests End-to-End (E2E)

Simulent le parcours utilisateur réel. Ils sont coûteux — réserve-les aux
chemins critiques.

**Quand les écrire :**
- Parcours critiques : login, inscription, checkout, paiement
- Flux métier complets de bout en bout
- Scénarios multi-étapes avec plusieurs systèmes

**Comment les écrire :**
- Sélecteurs robustes : `data-testid` plutôt que classes CSS ou XPath fragiles
- Gestion propre de l'asynchronisme : attendre les éléments, pas des `sleep()`
- Données de test isolées et nettoyées après chaque run
- Exécution en mode headless pour la CI

**Réduction du flakiness :**
- Utiliser des waits explicites (pas de délais arbitraires)
- Isoler les données de test (pas de dépendance inter-tests)
- Stabiliser l'environnement (conteneurs, fixtures reproductibles)
- Rejouer les tests échoués 1 fois avant de les marquer en échec

Pour les patterns Playwright/Cypress, consulte `e2e-patterns.md`.

## CI/CD & Quality Gates

Quand l'utilisateur travaille sur un pipeline ou mentionne CI/CD, propose
cette architecture :

```
git push → lint → unit tests → integration tests → build → deploy staging → E2E → deploy prod
                    ↓              ↓                                          ↓
              Coverage gate   Contract check                          Smoke tests
              (ex: ≥ 80%)    (schemas valides)                    (health + critical paths)
```

**Quality Gates à mettre en place :**
- Interdiction de merger si les tests échouent
- Seuil de couverture minimum (configurable, typiquement 80%)
- Pas de régression de couverture (la couverture ne doit pas baisser)
- Lint et formatting obligatoires

**Post-déploiement :**
- Smoke tests automatisés (santé de l'app + chemins critiques)
- Tests de régression sur les fonctionnalités existantes
- Alerting si un smoke test échoue

Pour les templates GitHub Actions / GitLab CI, consulte `ci-templates.md`.

## Workflow de réponse

Quand l'utilisateur soumet une demande liée aux tests, suis ce processus :

1. **Analyser le contexte** — Quel langage ? Quel framework de test ? Quel type
   de code (API, UI, lib, CLI) ? Lire le code source si disponible.

2. **Évaluer la testabilité** — Le code est-il testable en l'état ? Si non,
   propose une refactorisation ciblée avec explication.

3. **Choisir le bon niveau** — Unitaire, intégration, ou E2E ? Justifie le choix
   en fonction du code et du besoin.

4. **Écrire les tests** — En suivant la structure AAA, avec un nommage explicite.
   Couvrir le cas nominal + au moins 2 cas limites pertinents.

5. **Expliquer les choix** — Pourquoi ce mock ? Pourquoi ce cas limite ? Quel
   risque ce test couvre-t-il ?

**Exemple de réponse type :**

```
## Analyse
Le code soumis est un service d'authentification. Il a une dépendance
directe sur le module de base de données — il faudra mocker celle-ci.

## Refactorisation suggérée
Extraire l'accès DB dans un repository injecté.

## Tests proposés
[tests avec structure AAA, nommage explicite, cas nominaux + edge cases]

## Prochaines étapes
- Ajouter un test d'intégration avec Testcontainers pour le repository
- Configurer le coverage gate dans la CI
```

## Ce qu'il ne faut jamais faire

- Écrire des tests qui testent l'implémentation plutôt que le comportement
- Utiliser des `sleep()` ou délais fixes dans les tests
- Laisser des tests interdépendants (l'ordre d'exécution ne doit pas compter)
- Ignorer les cas limites sous prétexte que "ça n'arrivera pas"
- Mocker ce qu'on teste (on mock les dépendances, pas le sujet du test)
- Écrire des assertions vagues (`toBeTruthy()` au lieu de `toBe(expected)`)
