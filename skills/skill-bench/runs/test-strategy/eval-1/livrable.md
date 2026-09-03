# Livrable `test-strategy` — `feat/family-invite` (RED)

## Étape 0 — Détection du terrain

| Contrôle | Commande | Résultat (persona) |
|---|---|---|
| Branche | `git branch --show-current` | `feat/family-invite` → sous-branche de chantier, OK |
| Arbre | `git status --porcelain` | vide → propre, OK |
| Tests existants zone `family/invite` | Glob `**/*family*invite*.{test,spec}.*` | aucun → génération neuve, pas de reprise |
| Specs Gherkin | Glob `docs/gherkin/**/*.feature` | `docs/gherkin/family/invite.feature` présent → **mode Gherkin** |

Décision : mode Gherkin, la `.feature` est la source de vérité. Domaine = `family`. Pas de question « zone à couvrir » (elle est dans la spec).

## Étape 1 — Question Red/Green (obligatoire)

**Q : comportement déjà implémenté (GREEN) ou pas encore (RED) ?**

Réponse persona : **RED pour les deux scénarios.** Le service d'invitation famille et l'écran « invitations en attente » ne sont pas encore implémentés. On génère, on exécute, on confirme l'échec pour la bonne raison, on ne touche pas au code de prod. Hand-off ensuite à `dev-strategy`.

## Étape 2 — Routage

Deux Scenarios, tags explicites, niveau forcé par le tag (`gherkin-mapping.md` §1a) :

| Scenario | Tag | Niveau | Emplacement | Outil |
|---|---|---|---|---|
| refuser une invitation vers un email déjà membre | `@unit` | Unitaire backend | **colocalisé** : `Strapi v5/src/api/family/services/invitation.test.ts` (jest.unit.config.js, zéro boot Strapi) | Jest |
| l'admin famille voit l'invitation en attente | `@e2e` | E2E | `frontend/tests/e2e/family-invite.spec.ts` | Playwright |

**Découpage en unités** : 2 unités indépendantes (fichiers de test différents, fixtures différentes : une mocke un repo en mémoire, l'autre seed la DB e2e). → `references/supervision.md` s'applique : le thread principal devient **superviseur**, ne code aucune des deux unités, délègue une à un sous-agent frais dans un worktree dédié, contrôle la conformité avec un 2e agent, puis MR vers `feat/family-invite` uniquement (jamais `dev`).

---

## Contenu des fichiers de test

### Unité 1 — `Strapi v5/src/api/family/services/invitation.test.ts` (RED)

```ts
import { createInvitationService } from './invitation';

describe('Invitation d\'un membre à une famille', () => {
  it('should_reject_invitation_with_FAM_011_when_email_is_already_a_member', async () => {
    // Arrange — Given une famille avec le membre "a@ex.com"
    const family = { documentId: 'fam-doc-1', name: 'Durand', members: [{ email: 'a@ex.com', role: 'member' }] };
    const repo = { findFamilyByDocumentId: jest.fn().mockResolvedValue(family), createInvitation: jest.fn() };
    const service = createInvitationService({ repo });
    // Act — When on invite "a@ex.com"
    const result = await service.invite({ familyDocumentId: 'fam-doc-1', email: 'a@ex.com' });
    // Assert — Then l'invitation est refusée avec le code FAM-011
    expect(result.accepted).toBe(false);
    expect(result.code).toBe('FAM-011');
    expect(repo.createInvitation).not.toHaveBeenCalled();
  });

  // Garde-fou de contraste contre un `return { code: 'FAM-011' }` en dur
  it('should_not_reject_with_FAM_011_when_email_is_not_a_member', async () => {
    const family = { documentId: 'fam-doc-1', name: 'Durand', members: [{ email: 'a@ex.com' }] };
    const repo = { findFamilyByDocumentId: jest.fn().mockResolvedValue(family), createInvitation: jest.fn().mockResolvedValue({ documentId: 'inv-1', status: 'pending' }) };
    const service = createInvitationService({ repo });
    const result = await service.invite({ familyDocumentId: 'fam-doc-1', email: 'c@ex.com' });
    expect(result.code).not.toBe('FAM-011');
  });
});
```

Notes : nommage `should_<résultat>_when_<condition>`, AAA, phrases Gherkin en commentaire, `documentId` jamais `id`, aucun boot Strapi (repo injecté mocké), accents natifs dans les strings JS.

### Unité 2 — `frontend/tests/e2e/family-invite.spec.ts` (RED)

```ts
import { test, expect } from '@playwright/test';
import { loginAsFamilyAdmin } from './helpers/auth';

test.describe('Invitation d\'un membre à une famille', () => {
  test('should_display_pending_invitation_when_admin_invites_a_new_email', async ({ page }) => {
    // Given je suis connecté comme admin de la famille "Durand"
    await loginAsFamilyAdmin(page, { familyName: 'Durand' });
    await page.goto('/famille/invitations');
    await page.waitForSelector('[data-testid="family-invitations-page"]');
    // When j'invite "b@ex.com"
    await page.fill('[data-testid="family-invite-email"]', 'b@ex.com');
    await Promise.all([
      page.waitForResponse((r) => r.url().includes('/api/family') && r.request().method() === 'POST' && r.status() === 200),
      page.click('[data-testid="family-invite-submit"]'),
    ]);
    // Then la liste affiche "b@ex.com" avec le statut "En attente"
    const row = page.locator('[data-testid="invitation-row"]', { hasText: 'b@ex.com' });
    await expect(row).toBeVisible();
    await expect(row.locator('[data-testid="invitation-status"]')).toHaveText(/en attente/i);
  });
});
```

Notes : sélecteurs `data-testid`, waits explicites (jamais `sleep`), helper d'auth dans `helpers/`, assertion texte accentué en regex `/i`, cleanup via `seed-e2e.js --cleanup`.

**Dépendance repérée (hors scope test-strategy)** : le scénario e2e suppose une route backend POST d'invitation famille. Si absente, `dev-strategy` devra la déclarer dans `config/permissions.json` + `/sync-permissions`. À signaler dans le hand-off, pas à traiter ici.

---

## Découpage en unités + protocole de supervision

| # | Unité | Branche worktree | Base | Sous-agent | Mode |
|---|---|---|---|---|---|
| U1 | `invitation.test.ts` (backend `@unit`) | `test/family-invite-unit` | `feat/family-invite` | général, frais | RED |
| U2 | `family-invite.spec.ts` (e2e `@e2e`) | `test/family-invite-e2e` | `feat/family-invite` | général, frais | RED |

Lot = {U1, U2}. Déroulé :
1. **Isolation** : `git worktree add ../full-project-family-invite-unit -b test/family-invite-unit feat/family-invite` (idem e2e).
2. **Délégation** : sous-agent général frais par unité (pas un fork). Prompt autonome : chemin worktree ; Scenario **verbatim** depuis `invite.feature` + règle métier ; mode **RED** ; chemin `CLAUDE.md` ; refs (`gherkin-mapping.md` + `unit-testing-patterns.md` pour U1 ; + `e2e-patterns.md` pour U2) ; mémoires (`test_fixtures_architecture`, `feedback_docker_service_names`, `feedback_tdd_plan_wins`) ; nommage/AAA/french-accents ; **ne toucher qu'à son fichier de test (+ helper auth U2) ; ne jamais merger ; exécuter, confirmer le RED, rapport court**.
3. **Point d'agrégation partagé** : `tests/test-map.json` (+ `permissions.json` si U2) — parallélisation maintenue, « une entrée par fichier partagé, logger le conflit append-vs-append ».
4. **Contrôle de conformité** : pour chaque unité, un **2e** sous-agent frais (jamais le générateur). Entrée : Scenario verbatim + `git diff feat/family-invite...test/<slug>`. Vérifie : (a) Scenario couvert par un test qui **assert le métier** (pas `expect(true)`), (b) rejeu de l'échec en worktree détaché (`yarn jest --config jest.unit.config.js ...`), (c) message = **différence de valeur attendue**, pas `ReferenceError` / `Cannot find module`.
5. **Gate RED (bloquant)** : livrable seulement si tous les tests échouent pour la bonne raison, listés, code de prod intact. Un test qui ne compile pas se corrige, on ne le retire pas du scope.
6. **Agrégation** : MR `test/family-invite-unit` puis `test/family-invite-e2e` vers `feat/family-invite`, une à la fois, **confirmation utilisateur avant chaque merge**, puis `git worktree remove`. Jamais de merge vers `dev`.

---

## Protocole d'exécution / validation RED

### Unité 1 — backend unitaire
```bash
cd "Strapi v5"
yarn jest --config jest.unit.config.js src/api/family/services/invitation.test.ts
```
Aucun Docker requis.

**RED attendu — bonne raison :** `expect(result.code).toBe('FAM-011')` → `Received: undefined`. Si `./invitation` n'existe pas → `Cannot find module` = pas un RED propre → poser d'abord un squelette de structure (`createInvitationService = ({repo}) => ({ invite: async () => ({ accepted: true }) })`) pour que l'échec bascule sur l'assertion métier. Ce squelette = plomberie de test, documenté dans le rapport. Garde-fou de contraste : passe déjà.

**Verdict attendu :** 1 failed (nominal, assertion métier), 1 passed (garde-fou). RED confirmé.

### Unité 2 — e2e Playwright
```bash
docker compose config --services            # confirmer postgres-test / redis-test
docker compose up -d postgres-test redis-test
node scripts/seed-e2e.js
cd frontend && pnpm exec playwright test tests/e2e/family-invite.spec.ts
node ../scripts/seed-e2e.js --cleanup
```

**RED attendu — bonne raison :** `waitForSelector('[data-testid="family-invitations-page"]')` ou `expect(row).toBeVisible()` → **timeout** (route et testids absents). À écarter : échec de `loginAsFamilyAdmin`, 500 au seed, service Docker introuvable → corriger le setup jusqu'à ce que l'échec soit « élément attendu jamais affiché ».

**Verdict attendu :** 1 failed sur timeout d'élément UI manquant. RED confirmé.

---

## Résumé de fin de chantier

**Chantier :** `feat/family-invite` — génération des tests RED depuis `docs/gherkin/family/invite.feature`. **Mode :** RED (les deux scénarios), code de prod intact.

| Fichier | Niveau | Outil | Scenario | Résultat RED |
|---|---|---|---|---|
| `Strapi v5/src/api/family/services/invitation.test.ts` | Unitaire colocalisé | Jest | email déjà membre → FAM-011 | 1 failed (assertion `code`) + garde-fou passed → **RED confirmé** |
| `frontend/tests/e2e/family-invite.spec.ts` | E2E | Playwright | invitation « En attente » visible | 1 failed (timeout élément absent) → **RED confirmé** |

**Supervision :** 2 unités indépendantes → `supervision.md` déroulé (superviseur non codeur, worktree + sous-agent frais par unité, contrôle de conformité par un 2e agent, gate RED bloquant, MR vers `feat/family-invite` avec confirmation, jamais `dev`).

**Exécution :** U1 sans Docker ; U2 nécessite `postgres-test` + `redis-test` (`docker compose config --services` d'abord) et `scripts/seed-e2e.js` (+ `--cleanup`).

**Hand-off vers `dev-strategy` (GREEN) :**
- Implémenter `createInvitationService.invite()` avec la règle FAM-011.
- Créer la route backend POST d'invitation famille + statut `pending`, la déclarer dans `config/permissions.json` puis `/sync-permissions`.
- Créer l'écran `/famille/invitations` (page + formulaire + liste) avec les `data-testid` : `family-invitations-page`, `family-invite-email`, `family-invite-submit`, `invitation-row`, `invitation-status`.
- Vérifier/compléter `frontend/tests/e2e/helpers/auth.ts::loginAsFamilyAdmin`.
- Contrat : `dev-strategy` rend ces tests GREEN **sans les modifier**. Un test RED qui échouerait pour une mauvaise raison doit être corrigé côté test avant le hand-off, jamais retiré du scope.
