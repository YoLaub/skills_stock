# Livrable dev-strategy — chantier `feat/withdrawal-limits` (GREEN)

> Exécution en sandbox : pas d'accès au repo ActivCreew. Ce livrable est le plan complet + protocole d'exécution + résumé-type que le skill produirait. Le code de prod ci-dessous est une proposition à confronter aux assertions exactes des 2 fichiers RED au moment de l'exécution (le test gagne sur le code).

---

## Étape 0 — Détection du terrain, puis du périmètre

### Terrain
Commandes que je lancerais :
```bash
git branch --show-current      # attendu : feat/withdrawal-limits
git status --porcelain         # attendu : vide (arbre propre)
```
- Sous-branche de chantier `feat/withdrawal-limits`, arbre propre → **OK, on peut travailler**.
- Pas sur `main`/`dev` → pas d'arrêt.
- Vérif "code de prod existant" pour les domaines visés :
  ```bash
  ls "Strapi v5/src/api/withdrawal/services/" "Strapi v5/src/api/banner/services/"
  git log --oneline -- "Strapi v5/src/api/withdrawal" "Strapi v5/src/api/banner"
  ```
  - Si `withdrawal-validation.ts` ou `banner-schedule.ts` existent déjà partiellement → **reprendre l'existant, ne pas écraser**. L'échec `is not a function` suggère soit fichier absent, soit fonction non exportée — je regarde lequel avant de créer.
  - Si les modules `withdrawal` / `banner` existent déjà (schema, controller) → je ne touche qu'à la couche service pur.

### Périmètre
Source de vérité = les 2 fichiers de tests RED cités, confirmés RED et indépendants :

| # | Fichier de test RED | Fonction attendue | Règles métier | Échec actuel |
|---|---|---|---|---|
| 1 | `Strapi v5/src/api/withdrawal/services/withdrawal-validation.test.ts` | `validateWithdrawalAmount(amount, balance)` | WD-004 (montant > solde refusé), WD-005 (montant ≤ 0 refusé) | `validateWithdrawalAmount is not a function` |
| 2 | `Strapi v5/src/api/banner/services/banner-schedule.test.ts` | `nextActiveBanner(banners, now)` | BN-002 (fenêtre couvrant `now`, la plus prioritaire) | `nextActiveBanner is not a function` |

- Recherche Gherkin / specs pour le _pourquoi_ (best-effort, non bloquant) via grep sur WD-004/WD-005/BN-002 dans `docs/gherkin` et `docs/specs`. Si trouvées : lecture pour caler les cas limites (montant = solde exactement ? bannière dont la fenêtre commence pile à `now` ? plusieurs bannières à priorité égale ?). Si absentes → **le test tranche**, je lis les assertions au caractère près.

---

## Étape 1 — Lecture des conventions projet

1. **`CLAUDE.md`** — accents (`french-accents`), logging `console.log('[Module] msg')`, `documentId` jamais `id`, `strapi.documents()` en écriture, Knex lecture seule, services Docker (`postgres-test`/`redis-test`), imports monorepo. Mémoire `feedback_tdd_plan_wins`.
2. **Un controller voisin** — style gestion d'erreurs / réponse / logging. Utile seulement si on descend au controller (a priori non).
3. **`config/permissions.json`** — pertinent uniquement si nouvelles routes. Périmètre = fonctions pures → **aucune route, aucune permission**. Noté explicitement.
4. **Un `schema.json` existant** — pertinent seulement si un schema `withdrawal`/`banner` doit être créé. Échec = `is not a function` (pas erreur DB) → **pas de schema requis**. À confirmer en lisant les tests (import direct du `.ts` vs `startStrapi()`).
5. **DRY check** — grep `validateWithdrawal*` / `WithdrawalAmount` / `nextActiveBanner` / `*-validation.ts` / notion de fenêtre temporelle active. Étendre/composer si existant, sinon créer.

---

## Étape 2 — Questions OBLIGATOIRES (posées, réponses persona)

| Question | Réponse persona |
|---|---|
| 1. Périmètre confirmé (les 2 fichiers RED) ? | Oui, exactement ces 2 fichiers. |
| 2. Stack ? | Backend seul. |
| 3. Services tiers (Stripe, email, WS) ? | Non, aucun. |

Complément déduit : tests unitaires de **fonctions pures** (import direct `.ts`), donc pas de fixtures, pas de `draftAndPublish`, pas de base de test.

---

## Étape 3 — Plan d'implémentation

### 3.1 DRY check
grep sur `validateWithdrawal*`, `nextActiveBanner`, `*-validation.ts` → si aucun hit hors test : fonctions neuves. Pattern de référence réutilisable : `patterns-activcreew.md` → `validateMinimumAmount` qui `throw new Error(...)`. S'aligner **si et seulement si** les assertions du test l'attendent.

### 3.2 Cartographie par couche

**Domaine `withdrawal`** : seul `Strapi v5/src/api/withdrawal/services/withdrawal-validation.ts` créé (service pur). Schema/Routes/Controller/Lifecycle/Permissions : NON (échec = `is not a function`, import direct, aucun besoin DB/HTTP).

**Domaine `banner`** : seul `Strapi v5/src/api/banner/services/banner-schedule.ts` créé (service pur). Autres couches : NON.

**Règles non négociables applicables** : fichier séparé `*-validation.ts` / `*-schedule.ts`, named exports, zéro import `@strapi/strapi`, pas de `console.log` dans une fonction pure. `documentId`/Knex/`strapi.documents()`/`draftAndPublish` : non concernés.

**SOLID check** : S (une fonction = une responsabilité), O (nouvelles règles = nouvelles clauses), L (retourne exactement la forme attendue par les assertions), I (named exports), D (aucune dépendance concrète).

### 3.3 Note contrat (incertitude assumée, non résolue sans lire les assertions)
- `validateWithdrawalAmount` : (A) `throw Error` message FR — si `expect(() => …).toThrow(...)` ; (B) `{ valid, reason }` — si `toEqual`.
- `nextActiveBanner` : `Banner | null` vs `undefined` ; champs `startDate`/`endDate` vs `startAt`/`endAt` ; `priority` vs `weight` ; bornes inclusives ? → pris du test/fixtures.

---

## Étape 4 — Découpage en unités + protocole de supervision

### Unités
| Unité | Couche × domaine | Fichier de logique | Test RED |
|---|---|---|---|
| U1 | service pur × withdrawal | `src/api/withdrawal/services/withdrawal-validation.ts` | `withdrawal-validation.test.ts` |
| U2 | service pur × banner | `src/api/banner/services/banner-schedule.ts` | `banner-schedule.test.ts` |

U1 et U2 ne partagent aucun fichier de logique ni point d'agrégation (`permissions.json` intouché) → **2 unités indépendantes non bloquées** → `references/supervision.md` s'applique : **je deviens superviseur, je ne code pas moi-même.**

> Arbitrage honnête : périmètre minuscule (2 fonctions pures, ~15-25 lignes). La règle du skill est claire (supervision dès ≥ 2 unités indépendantes), je la déroule ; une implémentation inline séquentielle reste défendable si l'utilisateur préfère.

### Protocole de supervision (déroulé)

**1. Isolation** — worktrees basés sur `feat/withdrawal-limits` (jamais `main`/`dev`) :
```bash
git worktree add ../full-project-withdrawal-validation -b feat/withdrawal-validation feat/withdrawal-limits
git worktree add ../full-project-banner-schedule       -b feat/banner-schedule       feat/withdrawal-limits
```
Pas de lancement d'app → pas besoin de `dev-worktree.sh`.

**2. Un sous-agent général frais par unité** (pas un fork). Prompt autonome : répertoire = worktree ; chemin + contenu intégral du fichier de test RED ; règles métier verbatim (WD-004/WD-005 ; BN-002) ; chemin `CLAUDE.md` ; refs à lire (`cartographie-conventions.md`, `patterns-activcreew.md` Pattern Service pur, `principes-solid-dry.md`) ; mémoires (`feedback_tdd_plan_wins`, `feedback_docker_service_names`, `test_fixtures_architecture`) ; consignes (fonction pure, named exports, zéro import Strapi, messages FR corrects, SOLID+DRY grep avant créer, ne toucher qu'aux fichiers de son unité, ne pas toucher `permissions.json`) ; **ne jamais merger soi-même**, s'arrêter quand suite verte + `yarn tsc --noEmit` OK, rapport court (fichier, tests verts, contrat de retour choisi + pourquoi, blocage).

**3. Contrôle de conformité — 2e sous-agent frais par unité** (général, jamais le codeur ni un fork). Entrée seulement : critères verbatim (test RED + règles métier) + diff `git diff feat/withdrawal-limits...feat/withdrawal-validation`. Worktree détaché pour rejouer :
```bash
git worktree add ../full-project-verify-withdrawal-validation --detach feat/withdrawal-validation
cd "Strapi v5" && yarn test src/api/withdrawal/services/withdrawal-validation.test.ts
cd "Strapi v5" && yarn tsc --noEmit
```
Verdict **par critère** : couvert par code ET test / partiel / absent. U1 : WD-004 ? WD-005 ? cas `amount === balance` ? U2 : fenêtre couvrant `now` ? plus prioritaire ? cas "aucune active" ? Critère absent/partiel → blocage → relance ciblée une fois, sinon (pas d'humain) je tranche en superviseur et livre en `⏳ / bloqué`.

**4. Gate RED/GREEN (bloquant)** par unité : tous tests GREEN + `yarn tsc --noEmit` 0 erreur. Pas de `pnpm build` (backend seul). E2E réel : pas d'endpoint → l'"E2E" se réduit à la suite unitaire, signalé.

**5. Agrégation — sans merger vers `dev`** :
```bash
glab mr create --source-branch feat/withdrawal-validation --target-branch feat/withdrawal-limits
glab mr create --source-branch feat/banner-schedule       --target-branch feat/withdrawal-limits
```
**avec confirmation utilisateur avant chaque merge.** `git worktree remove` de tous les worktrees (y compris `verify-*`). **Jamais de merge vers `dev`** (builds Coolify — Clément).

**6. Relance** : périmètre épuisé après le 1er lot → étape 5.

---

## Étape 5 — Exécution et validation GREEN (protocole)

```bash
cd "Strapi v5"
yarn test src/api/withdrawal/services/withdrawal-validation.test.ts
yarn test src/api/banner/services/banner-schedule.test.ts
# ou ../scripts/run-affected-tests.sh
yarn tsc --noEmit
```
Boucle : test rouge → corriger le **code de prod**, jamais le test ; échec d'import/setup → corriger le setup sans toucher au comportement ; répéter jusqu'au vert + `tsc` 0 erreur. Le test gagne sur le code. Aucun test "retiré du scope".

### Proposition d'implémentation (à confronter aux assertions exactes)

**U1 — `withdrawal-validation.ts`** (variante contrat A : `throw`)
```typescript
export function validateWithdrawalAmount(amount: number, balance: number): void {
  if (!(amount > 0)) {
    throw new Error('Le montant du retrait doit être supérieur à 0'); // WD-005
  }
  if (amount > balance) {
    throw new Error('Le montant du retrait dépasse le solde disponible'); // WD-004
  }
}
```
> Si le test attend un objet : `{ valid: false, reason: 'NON_POSITIVE_AMOUNT' | 'INSUFFICIENT_BALANCE' }` / `{ valid: true }`.

**U2 — `banner-schedule.ts`**
```typescript
export interface ScheduledBanner {
  startDate: string | Date; endDate: string | Date; priority: number; [key: string]: unknown;
}
export function nextActiveBanner<T extends ScheduledBanner>(banners: T[], now: Date): T | null {
  const t = now.getTime();
  const active = banners.filter((b) => {
    const start = new Date(b.startDate).getTime();
    const end = new Date(b.endDate).getTime();
    return start <= t && t <= end; // bornes inclusives — à confirmer sur le test
  });
  if (active.length === 0) return null;
  return active.reduce((best, b) => (b.priority > best.priority ? b : best)); // BN-002
}
```
> Noms de champs, sens de priorité, inclusivité des bornes, valeur "aucune active", tie-break → pris du test.

---

## Étape 6 — Résumé de fin de chantier

### Conventions respectées
Lecture `CLAUDE.md` (seule la règle accents mord — messages FR) ; DRY check effectué avant création ; SOLID : fonctions pures isolées, named exports, zéro dépendance Strapi.

### Fichiers créés / modifiés
| Fichier | Statut | Rôle SOLID |
|---|---|---|
| `Strapi v5/src/api/withdrawal/services/withdrawal-validation.ts` | créé | Service pur — validation métier du retrait (S), consommable par futur controller (D) |
| `Strapi v5/src/api/banner/services/banner-schedule.ts` | créé | Service pur — sélection bannière active prioritaire (S) |
| Tests RED (`*.test.ts` ×2) | **non modifiés** | source de vérité |
| `config/permissions.json` | **non modifié** | aucune nouvelle route |

### Résultat des tests
- `withdrawal-validation.test.ts` : GREEN attendu (WD-004 + WD-005) — ⏳ non exécuté en sandbox.
- `banner-schedule.test.ts` : GREEN attendu (BN-002) — ⏳.
- `yarn tsc --noEmit` : 0 erreur — ⏳.
- Intégration / E2E : **N/A** (aucun endpoint créé). `pnpm build` frontend : **N/A** (backend seul).

### Permissions ajoutées
Aucune. `permissions.json` inchangé.

### Prochaines étapes
1. Confirmer les 2 MR vers `feat/withdrawal-limits`, puis `git worktree remove`.
2. **Ne pas** merger `feat/withdrawal-limits → dev` (Clément).
3. Hors périmètre : controller/route `withdrawal` consommant `validateWithdrawalAmount` (+ `permissions.json`), endpoint/job exposant `nextActiveBanner`, tests d'intégration + E2E.
4. Pas de hand-off vers `ux-ui-strategy` : rien à habiller (backend pur).

### Points en suspens (à lever à la lecture des assertions, non devinés)
- Contrat de retour de `validateWithdrawalAmount` (`throw` vs objet) et cas `amount === balance`.
- `nextActiveBanner` : noms des champs fenêtre/priorité, inclusivité des bornes, valeur si aucune active, tie-break à priorité égale.
