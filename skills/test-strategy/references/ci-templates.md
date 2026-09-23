# Templates CI/CD avec Quality Gates

## Table des matières
1. GitHub Actions
2. GitLab CI
3. Quality Gates — Configuration
4. Smoke Tests post-déploiement

---

## 1. GitHub Actions

### Pipeline complet avec pyramide des tests

```yaml
# .github/workflows/test.yml
name: Test Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check

  unit-tests:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - name: Coverage Gate
        run: |
          COVERAGE=$(npx istanbul-cobertura-coverage < coverage/cobertura-coverage.xml)
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80% threshold"
            exit 1
          fi
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run test:integration
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/test

  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run build
      - run: npm run test:e2e
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/

  deploy-staging:
    runs-on: ubuntu-latest
    needs: e2e-tests
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - run: echo "Deploy to staging..."
      # Adapter selon l'hébergeur (Vercel, AWS, etc.)

  smoke-tests:
    runs-on: ubuntu-latest
    needs: deploy-staging
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:smoke
        env:
          BASE_URL: https://staging.example.com
```

### Protection de branche (settings GitHub)

```
Branch protection rules pour 'main' :
✅ Require status checks to pass before merging
  - lint
  - unit-tests
  - integration-tests
  - e2e-tests
✅ Require branches to be up to date
✅ Do not allow bypassing the above settings
```

---

## 2. GitLab CI

### Pipeline équivalent

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test-unit
  - test-integration
  - test-e2e
  - deploy
  - smoke

variables:
  NODE_VERSION: "20"

lint:
  stage: lint
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run lint
    - npm run format:check

unit-tests:
  stage: test-unit
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm run test:unit -- --coverage
  coverage: '/All files.*?\s+(\d+\.\d+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

integration-tests:
  stage: test-integration
  image: node:${NODE_VERSION}
  services:
    - postgres:16
  variables:
    POSTGRES_DB: test
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgres://test:test@postgres:5432/test
  script:
    - npm ci
    - npm run test:integration

e2e-tests:
  stage: test-e2e
  image: mcr.microsoft.com/playwright:v1.40.0-jammy
  script:
    - npm ci
    - npm run build
    - npm run test:e2e
  artifacts:
    when: on_failure
    paths:
      - playwright-report/

deploy-staging:
  stage: deploy
  script:
    - echo "Deploy to staging..."
  only:
    - main

smoke-tests:
  stage: smoke
  script:
    - npm ci
    - npm run test:smoke
  variables:
    BASE_URL: https://staging.example.com
  only:
    - main
```

---

## 3. Quality Gates — Configuration

### Jest / Vitest — Seuils de couverture

```json
// dans package.json ou jest.config.ts
{
  "coverageThreshold": {
    "global": {
      "branches": 80,
      "functions": 80,
      "lines": 80,
      "statements": 80
    }
  }
}
```

### Pytest — Seuil de couverture

```ini
# pytest.ini ou pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term --cov-fail-under=80"
```

### SonarQube Quality Gate (si utilisé)

```
Conditions recommandées :
- Coverage on new code ≥ 80%
- Duplicated lines on new code < 3%
- Maintainability rating = A
- Reliability rating = A
- Security rating = A
```

---

## 4. Smoke Tests post-déploiement

### Script de smoke test type

```typescript
// tests/smoke/smoke.spec.ts
import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';

test.describe('Smoke Tests', () => {
  test('health endpoint responds 200', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/health`);
    expect(response.status()).toBe(200);
  });

  test('homepage loads', async ({ page }) => {
    await page.goto(BASE_URL);
    await expect(page).toHaveTitle(/.+/);
    await expect(page.locator('body')).not.toBeEmpty();
  });

  test('login page is accessible', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await expect(page.locator('[data-testid="login-form"]')).toBeVisible();
  });

  test('API returns data', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/status`);
    expect(response.status()).toBe(200);
    const body = await response.json();
    expect(body).toHaveProperty('status', 'ok');
  });
});
```
