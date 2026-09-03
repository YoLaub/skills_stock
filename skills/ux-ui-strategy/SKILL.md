---
name: ux-ui-strategy
description: >
  Stratégie UX/UI pour ActivCreew : rendre un écran conforme à sa maquette
  (docs/maquettes/**) via le design system (Shadcn + tokens HSL + packages/ui),
  sans casser la logique métier ni les tests GREEN. Utilise ce skill quand
  l'utilisateur veut "habiller" une feature, "intégrer / appliquer la maquette",
  "corriger l'UI", "rendre joli", ou dit "ux-ui-strategy" ; aussi après dev-strategy
  quand le comportement est vert mais l'écran brut. Troisième maillon du pipeline :
  test-strategy (RED) → dev-strategy (GREEN) → ux-ui-strategy (forme).
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
- `references/supervision.md` — délégation par vue isolée (worktree + sous-agent frais + contrôle de non-régression). Lire à l'étape 4 si ≥ 2 vues indépendantes.

Règles transverses (accents `french-accents`, DRY visuel) : voir `CLAUDE.md` du repo.
Ne pas les recopier ici.

## Deux modes d'usage

| Mode | Quand | Point de départ |
|------|-------|-----------------|
| **A — En suite de `dev-strategy`** | Le comportement est GREEN, l'écran est brut | Code de prod existant + maquette HTML |
| **B — Seul (correction UI)** | L'UI existe mais diverge de la maquette / est moche / pas responsive | Composants existants + maquette HTML (ou feedback) |

## ⚡ Workflow ux-ui-strategy (orchestration)

Objectif : en **une invocation**, lire la maquette, lire le code de prod existant + son
design system, planifier l'intégration visuelle, l'appliquer, et vérifier que le GREEN
tient. Suis ces étapes DANS L'ORDRE.

### Étape 0 — Terrain, puis périmètre

**Terrain d'abord** — `git branch --show-current` + `git status --porcelain` :
- Sur une sous-branche de chantier (`feat/…`) avec un arbre propre → OK.
- Sur `main`/`dev` ou arbre sale → s'arrêter, demander la branche de travail
  (`git-workflow-chantier`).
- Une intégration visuelle partielle existe déjà sur cette vue → **la reprendre**, ne
  pas repartir de zéro. En cas de doute, demander.

**Périmètre** — cherche dans cet ordre :

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

### Étape 4 — Intégration

Une **unité** = une vue de maquette + les fichiers de prod qui la portent. Deux vues
sont indépendantes si elles ne partagent pas de composant à modifier (un composant
`packages/ui` partagé retouché = une unité "composant" traitée en premier).

- **1 vue** → intègre-la directement : design system lu (étape 1), traduction vers
  tokens/composants (**zéro couleur en dur**, `references/patterns-integration.md`),
  tous les `data-testid` et la logique préservés.
- **≥ 2 vues indépendantes** → **déroule `references/supervision.md`** : superviseur qui
  ne code pas, worktree + sous-agent frais par vue, contrôle de non-régression par un 2e
  agent (contrat testid/texte/ARIA intact + specs vertes) avant chaque merge, MR vers
  `feat/<chantier>` seulement, jamais vers `dev`.

**A11y & responsive non négociables** (tout worker, toute vue) : mobile-first
(`flex-col` → `sm:flex-row`), `<button>` pour les actions / `<a>` pour la navigation,
labels liés, `aria-*` sur les éléments custom, focus visible, et TOUS les états
(loading/skeleton, vide, erreur, disabled, hover/focus/active) — la maquette ne montre
souvent que le nominal.

QA final (toutes vues livrées) : `pnpm build` + `pnpm lint` → 0 erreur ;
`pnpm exec playwright test <specs concernées>` → **toujours GREEN**.

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

## Ce qu'il ne faut jamais faire (propre à ce maillon)

- Recopier les couleurs/hex/`gray-XXX`/font de la maquette en dur → toujours via tokens
- Supprimer ou déplacer un `data-testid` hors de son élément interactif
- Modifier un handler, un appel API, un état pour « simplifier » l'UI
- Modifier un test pour qu'il passe après le restyle — si un test casse, c'est le markup
- Intégrer uniquement le desktop, ou oublier les états non-nominaux (loading, vide,
  erreur, disabled, focus)
- Réimporter une police déjà configurée globalement (CSP + perf)
- Merger une vue vers `dev` (builds Coolify) — MR vers `feat/<chantier>` uniquement

(DRY visuel — réutiliser `packages/ui` — et accents TSX / entités HTML en strings :
dans `CLAUDE.md` + `references/patterns-integration.md`.)

## Évolution de ce skill

- Nouveau pattern de traduction ou piège d'intégration → `references/patterns-integration.md`.
- Nouveau token, composant ou correspondance → `references/design-system-mapping.md`.
- Nouveau point de protocole de délégation → `references/supervision.md`.
- Ne modifier ce SKILL.md que si l'orchestration (étapes) change.
