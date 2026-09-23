# Patterns d'implémentation ActivCreew

Fichier append-only : chaque nouveau pattern éprouvé sur une feature s'ajoute ici,
jamais dans SKILL.md. À lire à l'étape 4 (implémentation), par les workers concernés.

## Pattern Schema Strapi v5

```json
{
  "kind": "collectionType",
  "collectionName": "<module>s",
  "info": { "singularName": "<module>", "pluralName": "<module>s", "displayName": "<Module>" },
  "options": { "draftAndPublish": false },
  "attributes": {
    "user": { "type": "relation", "relation": "manyToOne", "target": "plugin::users-permissions.user" },
    "status": {
      "type": "enumeration",
      "enum": ["active", "cancelled", "suspended"],
      "default": "active"
    }
  }
}
```

## Pattern Service pur (S + D de SOLID)

```typescript
// src/api/<module>/services/<module>-validation.ts
// Fonctions pures : zéro dépendance Strapi → testables sans startStrapi()

export function validateMinimumAmount(amountInEuros: number, minimum = 2): void {
  if (amountInEuros < minimum) {
    throw new Error(`Le montant minimum est de ${minimum} €`);
  }
}

export function shouldDisplayCount(count: number, threshold = 10): boolean {
  return count >= threshold;
}
```

> Séparer systématiquement les fonctions pures des services Strapi.
> Les tests unitaires importent le fichier directement sans `startStrapi()`.

## Pattern Idempotence (protection double-appel)

```typescript
// En mémoire pour les tests ; en production → table DB ou Redis
const _processed = new Map<string, unknown>();

export async function runOnce<T>(
  key: string,
  fn: () => Promise<T> | T
): Promise<T | { alreadyProcessed: true }> {
  if (_processed.has(key)) return { alreadyProcessed: true } as any;
  const result = await fn();
  _processed.set(key, result);
  return result;
}
```

## Pattern Controller (S de SOLID : routage uniquement)

```typescript
import { factories } from '@strapi/strapi';
import { validateMinimumAmount } from '../services/<module>-validation';

export default factories.createCoreController('api::<module>.<module>', ({ strapi }) => ({
  async create(ctx) {
    const user = ctx.state.user;
    if (!user) return ctx.unauthorized();

    const { amount } = ctx.request.body;
    try {
      validateMinimumAmount(amount / 100);
    } catch (e: any) {
      return ctx.badRequest(e.message);
    }

    console.log(`[<Module>] create user=${user.id} amount=${amount}`);
    const result = await strapi.service('api::<module>.<module>').create({ user, amount });
    return ctx.send(result);
  },
}));
```

## Pattern Route custom Strapi v5

```typescript
// src/api/<module>/routes/<module>-custom.ts
export default {
  routes: [
    {
      method: 'POST',
      path: '/<module>/action',
      handler: '<module>.action',
      config: { policies: [], middlewares: [] },
    },
    {
      method: 'GET',
      path: '/<module>/public-data',
      handler: '<module>.publicData',
      config: { auth: false, policies: [] },
    },
  ],
};
```

## Pattern Webhook tiers (Stripe, etc.)

```typescript
// Route sans auth — vérification de signature dans le controller
{
  method: 'POST',
  path: '/<module>/webhook',
  handler: '<module>.handleWebhook',
  config: { auth: false, policies: [] },
}

// Controller : skip signature en mode test
async handleWebhook(ctx) {
  const sig = ctx.request.headers['stripe-signature'];
  const secret = process.env.STRIPE_WEBHOOK_SECRET;
  let event = ctx.request.body;

  if (process.env.NODE_ENV !== 'test' && sig && secret) {
    try {
      event = stripe.webhooks.constructEvent(ctx.request.rawBody, sig, secret);
    } catch {
      return ctx.badRequest('Signature invalide');
    }
  }

  // Idempotence : ignorer si déjà traité
  const existing = await strapi.documents('api::<module>.<module>').findFirst({
    filters: { stripeEventId: event.id },
  });
  if (existing) return ctx.send({ received: true });

  // Traitement...
  return ctx.send({ received: true });
}
```
