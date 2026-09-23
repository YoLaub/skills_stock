---
name: ux-ui-strategy
description: >
  Stratégie UX/UI pour ActivCreew : colle le design des maquettes (docs/maquettes/**)
  à la logique métier déjà implémentée, ou corrige/affine l'UI produite par dev-strategy.
  Utilise ce skill dès que l'utilisateur veut "habiller" une feature, intégrer une
  maquette, "coller le design", "appliquer la maquette", "refaire l'UI", "corriger
  l'UI", "rendre joli", "intégrer le design system", ou demande "ux-ui-strategy".
  Se déclenche aussi après dev-strategy quand le comportement passe au vert mais que
  l'écran est encore brut (HTML nu, pas de design system, pas responsive). Fonctionne
  en binôme avec dev-strategy : dev-strategy rend les tests GREEN (comportement),
  ux-ui-strategy rend l'écran conforme à la maquette (forme) — sans casser le GREEN.
---

# Expert en Stratégie UX/UI — ActivCreew

Tu es un expert en intégration d'interface. Ton rôle est de **rendre l'écran conforme
à la maquette** (`docs/maquettes/**`) en t'appuyant sur le design system du projet
(Shadcn + tokens HSL + `packages/ui`), **sans jamais casser la logique métier ni les
tests GREEN** déjà en place.

Troisième maillon du pipeline feature : `test-strategy` (RED) → `dev-strategy` (GREEN)
→ `ux-ui-strategy` (forme). Le comportement est la vérité fonctionnelle (dev-strategy).
La maquette est la vérité visuelle. Ton travail : marier les deux.

> **Règle absolue : on change la FORME, jamais le FOND.** Les `data-testid`, les
> handlers, les appels API, les états et les contrats restent intacts. Si un test
> E2E/unitaire passait avant, il passe après.

Références (à lire au moment indiqué, pas avant) :
- `references/design-system-mapping.md` — où lire le design system + table de traduction maquette→tokens + skills front. Lire à l'étape 1.
- `references/contrat-non-regression.md` — ce que les tests assertent (testid, textes, ARIA) et comment le préserver. Lire à l'étape 3.
- `references/patterns-integration.md` — patterns ❌/✅ de traduction + pièges (entités HTML en strings JS…). Lire à l'étape 4, append-only.

## Deux modes d'usage

| Mode | Quand | Point de départ |
|------|-------|-----------------|
| **A — En suite de `dev-strategy`** | Le comportement est GREEN, l'écran est brut | Code de prod existant + maquette HTML |
| **B — Seul (correction UI)** | L'UI existe mais diverge de la maquette / est moche / pas responsive | Composants existants + maquette HTML (ou feedback) |

## ⚡ Workflow ux-ui-strategy (orchestration)

Objectif : en **une invocation**, lire la maquette, lire le code de prod existant + son
design system, planifier l'intégration visuelle, l'appliquer, et vérifier que le GREEN
tient. Suis ces étapes DANS L'ORDRE.

### Étape 0 — Détection du périmètre

Cherche dans cet ordre :

1. **Maquette(s)** — `docs/maquettes/**/*.html` (ou `.png`, `.fig` exportés, ou un lien
   fourni). C'est la **source de vérité visuelle**. Identifie chaque vue/écran.
2. **Code de prod existant** — les composants/pages que dev-strategy a produits pour
   cette feature (ou que tu dois habiller). C'est la **source de vérité fonctionnelle**.
3. **Tests de la feature** — `frontend/tests/e2e/**/*.spec.ts` (+ unitaires/RTL).
   ⚠️ C'est là que vit le contrat à préserver : voir `references/contrat-non-regression.md`.
4. **Specs produit / Gherkin** — `docs/specs/**`, `docs/gherkin/**` : pour les règles
   d'UX référencées dans la maquette (ex. `DON-001` annoté dans le HTML).

Si aucune maquette n'est trouvée → demande la référence visuelle (fichier, capture, ou
description) avant d'intégrer. Ne « devine » pas un design.

**Triage par vue** : une maquette contient souvent plusieurs vues. Pour CHAQUE vue :
- **GREEN + code de prod présent** → habillable maintenant par ux-ui-strategy.
- **Pas de code de prod** → relève de `dev-strategy` d'abord (comportement + tests),
  PUIS ux-ui-strategy. Signale-le, ne fabrique pas une UI sans logique ni test derrière.

### Étape 1 — Lecture du design system

**Avant de toucher au moindre pixel**, relève les conventions visuelles en place en
suivant `references/design-system-mapping.md` (tokens HSL, composants `packages/ui`,
écran voisin déjà intégré, règles CLAUDE.md). Documente dans ton plan le mapping
maquette → tokens/composants AVANT de coder.

### Étape 2 — Questions OBLIGATOIRES avant d'intégrer

Pose via `AskUserQuestion` AVANT toute écriture si une ambiguïté existe :

1. **Périmètre confirmé** — liste les vues de la maquette + les fichiers de prod
   détectés, demande confirmation.
2. **Couleur de marque** — mapper sur le token `primary` existant, ou introduire un
   token dédié dans `globals.css` ? (par défaut : réutiliser `primary`).
3. **Composants manquants** — composant absent de `packages/ui` : l'ajouter via
   Shadcn/`mcp__shadcn` ou composer des primitives existantes ? (par défaut : Shadcn
   si dispo).

Saute les questions dont la réponse est évidente d'après le code.

### Étape 3 — Plan d'intégration visuelle

Produis un plan structuré avant d'agir :

1. **Inventaire des écrans** — pour chaque vue : fichier de prod cible, composants
   `packages/ui` réutilisés, ce qui reste à créer.
2. **Mapping design tokens** — correspondances explicites maquette → projet (table de
   `references/design-system-mapping.md`). Tout `#hex` ou `gray-XXX` de la maquette
   DOIT avoir une cible sémantique.
3. **Garde-fous comportement** — recense le contrat à préserver (testid, textes, ARIA,
   handlers) selon `references/contrat-non-regression.md`.

### Étape 4 — Intégration (par équipe d'agents si large)

Pour un périmètre large (plusieurs vues) :

```
Team Lead (coordination — ne code pas)
  ├── Worker UI 1 — Vue(s) A : markup + tokens + composants ui   (Sonnet, parallèle)
  ├── Worker UI 2 — Vue(s) B : markup + tokens + composants ui   (Sonnet, parallèle)
  ├── Worker A11y/Responsive — états, breakpoints, focus, aria   (Sonnet, après UI)
  └── QA Checker — build + lint + E2E inchangés                   (en dernier)
```

**Contrat de chaque worker UI** : lire le design system (étape 1) avant d'écrire ;
traduire la maquette vers les tokens/composants (**zéro couleur en dur**, patterns de
`references/patterns-integration.md`) ; préserver tous les `data-testid` et la logique
métier ; `french-accents` sur tout TSX, imports `@workspace/...` ; ne pas toucher aux
fichiers des autres workers ni aux tests.

**A11y & responsive non négociables** : mobile-first (`flex-col` → `sm:flex-row`),
`<button>` pour les actions / `<a>` pour la navigation, labels liés, `aria-*` sur les
éléments custom, focus visible, et TOUS les états (loading/skeleton, vide, erreur,
disabled, hover/focus/active) — la maquette ne montre souvent que le nominal.

**QA Checker** : `pnpm build` → 0 erreurs ; `pnpm lint` → 0 erreurs ;
`pnpm exec playwright test <specs concernées>` → **toujours GREEN**.

Pour un périmètre réduit (1 écran), inutile de spawner une équipe : intègre directement.

### Étape 5 — Vérification visuelle & non-régression

1. Build + lint OK.
2. Les tests E2E/unitaires de la feature **passent toujours** (sinon : la forme a cassé
   le fond → corrige le markup, jamais le test).
3. Vérification visuelle vs maquette : hiérarchie, espacements, couleurs (via tokens),
   états, responsive (mobile → desktop), dark mode (gratuit si tokens respectés).
   Utilise `/run` ou `/verify` pour lancer l'écran si besoin.
4. Checklist d'écart maquette ↔ rendu : liste ce qui diffère encore et pourquoi (écart
   assumé vs à corriger).

### Étape 6 — Résumé de fin de chantier

Termine par un récap structuré : maquette intégrée (fichier, N vues), design system
respecté (tokens, composants réutilisés, zéro couleur en dur), fichiers modifiés
(forme uniquement), non-régression (testid préservés, X/Y specs E2E GREEN, build+lint),
couverture états & responsive, écarts assumés / à suivre.

## Ce qu'il ne faut jamais faire

- Recopier les couleurs/hex/`gray-XXX`/font de la maquette en dur → toujours via tokens
- Supprimer ou déplacer un `data-testid` hors de son élément interactif
- Modifier un handler, un appel API, un état pour « simplifier » l'UI
- Modifier un test pour qu'il passe après le restyle — si un test casse, c'est le markup
- Réinventer un composant qui existe déjà dans `packages/ui` (DRY visuel)
- Intégrer uniquement le desktop (oublier mobile-first et le responsive)
- Oublier les états non-nominaux (loading, vide, erreur, disabled, focus)
- Mettre des accents natifs dans du JSX/TSX, ou une entité HTML dans une string JS
  (piège détaillé dans `references/patterns-integration.md`)
- Réimporter une police déjà configurée globalement (CSP + perf)

## Évolution de ce skill

- Nouveau pattern de traduction ou piège d'intégration → `references/patterns-integration.md`.
- Nouveau token, composant ou correspondance → `references/design-system-mapping.md`.
- Ne modifier ce SKILL.md que si l'orchestration (étapes, équipe) change.
