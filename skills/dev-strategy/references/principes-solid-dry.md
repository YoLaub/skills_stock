# Principes SOLID / DRY appliqués à ActivCreew

À lire avant de planifier (étape 3) : chaque worker les applique pendant l'implémentation.

## SOLID

| Principe | Application concrète |
|----------|----------------------|
| **S** — Single Responsibility | Un fichier = une responsabilité. Controller ≠ Service ≠ Validation. Sépare les services purs (logique métier) des services Strapi (accès DB). |
| **O** — Open/Closed | Étends par composition, pas par modification. Nouveau comportement → nouveau service ou middleware, pas un `if` dans le controller existant. |
| **L** — Liskov | Tes fonctions respectent le contrat attendu par les tests. Si un test attend `{ status: 'cancelled' }`, retourne exactement ça. |
| **I** — Interface Segregation | Ne fais pas dépendre un module de fonctions qu'il n'utilise pas. Services purs importés individuellement (named exports), pas un objet monolithique. |
| **D** — Dependency Inversion | Les controllers dépendent d'abstractions (fonctions de service injectées), pas d'implémentations concrètes. Facilite les tests unitaires sans `startStrapi()`. |

## DRY

- Avant d'écrire une fonction, cherche si elle existe déjà dans `src/api/*/services/`
- Les helpers partagés entre modules vont dans `src/api/custom/services/` ou un package kernel
- Les règles de validation dupliquées → factoriser en service pur réutilisable
- Patterns répétés dans les controllers → extraire en middleware ou policy

## Code simple et reviewable

- Pas d'abstraction prématurée : 3 lignes similaires ne justifient pas un helper
- Nommage explicite : `validateDonationAmount` > `validate` > `check`
- Pas de commentaire sur le QUOI (le code le dit). Commentaire uniquement sur le POURQUOI si non-obvieux
- Aucune logique cachée dans un middleware non documenté
