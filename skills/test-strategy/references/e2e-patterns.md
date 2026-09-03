# Patterns de Tests End-to-End

## Table des matières
1. Playwright
2. Cypress
3. Stratégies anti-flakiness
4. Organisation des tests E2E

---

## 1. Playwright

### Setup recommandé

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  retries: 1,                    // 1 retry avant échec définitif
  workers: process.env.CI ? 1 : undefined,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',     // Trace uniquement sur retry (debug)
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { browserName: 'chromium' } },
    { name: 'firefox', use: { browserName: 'firefox' } },
  ],
});
```

### Pattern Page Object Model

```typescript
// pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  // Sélecteurs via data-testid (robustes)
  private emailInput = '[data-testid="login-email"]';
  private passwordInput = '[data-testid="login-password"]';
  private submitButton = '[data-testid="login-submit"]';
  private errorMessage = '[data-testid="login-error"]';

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill(this.emailInput, email);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.submitButton);
  }

  async getError(): Promise<string | null> {
    const el = this.page.locator(this.errorMessage);
    if (await el.isVisible()) return el.textContent();
    return null;
  }
}
```

### Test E2E avec AAA

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/login.page';

test.describe('Authentication Flow', () => {
  test('should_redirect_to_dashboard_when_credentials_valid', async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    // Act
    await loginPage.login('user@test.com', 'ValidPass123!');

    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
  });

  test('should_show_error_when_password_is_wrong', async ({ page }) => {
    // Arrange
    const loginPage = new LoginPage(page);
    await loginPage.goto();

    // Act
    await loginPage.login('user@test.com', 'wrong');

    // Assert
    await expect(page).toHaveURL('/login');
    await expect(page.locator('[data-testid="login-error"]'))
      .toContainText('Invalid credentials');
  });
});
```

### Attentes explicites (pas de sleep)

```typescript
// BON — Attendre un élément spécifique
await page.waitForSelector('[data-testid="results-loaded"]');
await expect(page.locator('.item')).toHaveCount(10);

// BON — Attendre une réponse réseau
await Promise.all([
  page.waitForResponse(resp => resp.url().includes('/api/users') && resp.status() === 200),
  page.click('[data-testid="load-users"]'),
]);

// MAUVAIS — Délai arbitraire
await page.waitForTimeout(3000); // ❌ Ne jamais faire ça
```

---

## 2. Cypress

### Setup recommandé

```typescript
// cypress.config.ts
export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    retries: { runMode: 1, openMode: 0 },
    viewportWidth: 1280,
    viewportHeight: 720,
  },
});
```

### Commands personnalisées (équivalent Page Object)

```typescript
// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.get('[data-testid="login-email"]').type(email);
  cy.get('[data-testid="login-password"]').type(password);
  cy.get('[data-testid="login-submit"]').click();
});

// Raccourci API pour bypass UI dans les tests non-login
Cypress.Commands.add('loginViaApi', (email: string, password: string) => {
  cy.request('POST', '/api/auth/login', { email, password })
    .its('body.token')
    .then(token => {
      cy.setCookie('auth_token', token);
    });
});
```

### Test Cypress avec AAA

```typescript
describe('Checkout Flow', () => {
  beforeEach(() => {
    cy.loginViaApi('user@test.com', 'pass');
    cy.visit('/products');
  });

  it('should_complete_purchase_when_cart_has_items', () => {
    // Arrange — Ajouter un produit au panier
    cy.get('[data-testid="product-card"]').first()
      .find('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="cart-badge"]').should('contain', '1');

    // Act — Procéder au checkout
    cy.get('[data-testid="go-to-checkout"]').click();
    cy.get('[data-testid="confirm-order"]').click();

    // Assert
    cy.url().should('include', '/order/confirmation');
    cy.get('[data-testid="order-status"]').should('contain', 'Confirmed');
  });
});
```

---

## 3. Stratégies anti-flakiness

### Les causes principales et leurs solutions

| Cause | Symptôme | Solution |
|-------|----------|----------|
| Timing | Test parfois OK, parfois KO | Attentes explicites sur les éléments |
| Données partagées | Échec selon l'ordre d'exécution | Données isolées par test, cleanup systématique |
| Animations | Click sur un élément en mouvement | Désactiver les animations en test |
| Réseau lent | Timeout sur les appels API | Intercepter les appels, mocker si nécessaire |
| État global | Test dépend d'un test précédent | Chaque test repart d'un état propre |

### Checklist anti-flakiness

```typescript
// 1. Désactiver les animations
// Dans le CSS de test :
// *, *::before, *::after { animation-duration: 0s !important; transition-duration: 0s !important; }

// 2. Isoler les données
beforeEach(async () => {
  await resetTestDatabase();
  await seedTestData();
});

// 3. Intercepter le réseau quand nécessaire
await page.route('**/api/slow-service', route =>
  route.fulfill({ status: 200, body: JSON.stringify({ data: 'mocked' }) })
);

// 4. Retry automatique (1 seul retry)
// Configuré au niveau du framework, pas dans le test
```

---

## 4. Organisation des tests E2E

### Structure de dossiers recommandée

```
e2e/
├── fixtures/            # Données de test
│   ├── users.json
│   └── products.json
├── pages/               # Page Objects
│   ├── login.page.ts
│   ├── dashboard.page.ts
│   └── checkout.page.ts
├── specs/               # Tests par feature
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── registration.spec.ts
│   └── checkout/
│       ├── cart.spec.ts
│       └── payment.spec.ts
└── support/
    ├── commands.ts      # Helpers réutilisables
    └── setup.ts         # Setup global
```

### Quels parcours tester en E2E

Réserver les tests E2E aux **chemins critiques** uniquement :
- Authentification (login, logout, refresh token)
- Inscription et onboarding
- Parcours d'achat / paiement
- Actions destructives (suppression de compte, etc.)
- Flux multi-étapes critiques pour le business

Tout le reste devrait être couvert par des tests unitaires et d'intégration.
