# Garde-fous comportement — ne pas casser le GREEN

À lire à l'étape 3 (plan d'intégration). Le contrat à préserver = **tout ce que les
tests savent localiser/asserter**. Extrais-le des specs (étape 0.3) ET du code de prod.

## Ce qui fait partie du contrat

- les `data-testid` présents (à **préserver à l'identique**, sur l'élément qui garde le
  même rôle d'interaction)
- les **textes assertés** par `getByText(...)` / `getByRole(..., { name })` — le wording
  fait partie du contrat. Si un test cherche « Où va votre don ? » ou « … € collectés »,
  tu ne peux PAS reformuler ce texte en restylant. Garde-le mot pour mot (les entités
  d'accents `&eacute;` ne changent pas le texte rendu, jsdom les décode).
- les **attributs ARIA** assertés : `aria-pressed`, `aria-selected`, `role="alert"`,
  `aria-label`. Le composant Shadcn `Tabs` gère `aria-selected` ; mais un bouton de montant
  custom doit garder son `aria-pressed`.
- les handlers / Server Actions / appels API / états (forme uniquement : on enveloppe et
  restyle, on ne touche ni la logique ni les props)

> Astuce non-régression : si un test utilise un `.or(getByRole('heading', { name }))`
> comme fallback d'un `data-testid`, tu peux changer le titre visuel (pour coller à la
> maquette) À CONDITION d'ajouter/garder le `data-testid` que le sélecteur vise en premier.

## Où lire le contrat

Les specs E2E de la feature (`frontend/tests/e2e/**/*.spec.ts`) et les tests
unitaires/RTL. ⚠️ C'est dans les TESTS que vit le contrat, pas seulement dans le code de
prod : lis-les AVANT de restyler.
