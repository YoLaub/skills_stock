# Livrable `ux-ui-strategy` — `feat/withdrawal-limits` / `docs/maquettes/withdrawal.html`

> Mode A — en suite de `dev-strategy`. Comportement GREEN, écrans bruts. Sandbox : livrable = plan + protocole que le skill produirait.

## Étape 0 — Terrain, puis périmètre

**Terrain** : `git branch --show-current` → `feat/withdrawal-limits` (sous-branche OK) ; `git status --porcelain` vide (OK) ; pas d'intégration visuelle partielle connue → on part du GREEN brut. Si arbre sale ou branche `dev`/`main` → stop, réclamer la branche.

**Périmètre (ordre imposé)** :
1. Maquette `docs/maquettes/withdrawal.html` — 2 vues : `#form` (formulaire de retrait), `#history` (table des retraits). Ne montre que l'état nominal.
2. Code de prod : `apps/helm/app/withdrawal/page.tsx` (formulaire brut, `onSubmit → useWithdraw()`) ; `packages/ui/src/components/WithdrawalHistory` (table brute).
3. Tests : E2E `apps/helm` + RTL `packages/ui`. Contrat connu : texte **« Montant à retirer »** asserté.
4. Specs / Gherkin : chercher un identifiant `WDR-00x` annoté dans le HTML. Absent → ne rien inventer sur les plafonds.

**Triage par vue** :
| Vue | Code de prod | Tests | Verdict |
|---|---|---|---|
| `#form` | présent | E2E « Montant à retirer », testids `withdrawal-amount-input`/`withdrawal-submit` | Habillable maintenant |
| `#history` | présent | testid `withdrawal-row`, rôle `table` | Habillable maintenant |

Aucune vue ne relève de `dev-strategy`.

**Indépendance** : `#form` dans `apps/helm`, `#history` dans `packages/ui`, aucun composant partagé à modifier → **2 unités indépendantes ⇒ étape 4 = protocole `supervision.md`**.

## Étape 1 — Lecture du design system

À relever (`design-system-mapping.md`) : tokens HSL de `globals.css` (`--primary`, `--card`, `--background`, `--foreground`, `--muted-foreground`, `--border`, `--radius`, bloc `.dark`) ; `tailwind.config.ts` (couleurs sémantiques, breakpoints) ; inventaire `packages/ui/src/components/` (button, card, input, label, form, table, skeleton, alert) ; écran voisin déjà intégré dans `apps/helm` ; `CLAUDE.md` (imports `@workspace/...`, `french-accents`, Client Component pour le form avec `useWithdraw()`).

**Mapping maquette → design system** (figé avant de coder) :
| Maquette (en dur) | Cible sémantique |
|---|---|
| `#2563eb` (boutons) | `bg-primary` / `text-primary-foreground` — **token `primary` réutilisé** (variant `default` de `<Button>`) |
| `gray-100` (fonds de carte) | `bg-card` via `<Card>` |
| `bg-white` conteneur | `bg-card` / `<Card>` |
| `text-gray-900` / `text-gray-500` | `text-foreground` / `text-muted-foreground` |
| `border-gray-200` | `border-border` |
| `<button>` / `<input>` / `<table>` ad hoc | `<Button size="lg">` / `<Input>`+`<Label>` / `<Table>` Shadcn |
| rayons/ombres ad hoc | conventions `<Card>` (`--radius`) |
| police inline | déjà configurée globalement — **ne pas réimporter** |

Dark mode gratuit si tout passe par les tokens.

## Étape 2 — Questions obligatoires (réponses persona)

| # | Question | Réponse |
|---|---|---|
| 1 | Périmètre confirmé (2 vues, 2 fichiers cibles) ? | Oui, ces deux fichiers, rien d'autre. |
| 2 | `#2563eb` → token `primary` existant ou nouveau token ? | **Réutiliser `primary`.** |
| 3 | Composants manquants → Shadcn ou composer ? | **Shadcn si un composant manque**, sinon composer. |
| 4 | Décliner loading/vide/erreur/disabled/focus de moi-même ? | **Oui**, états non-nominaux obligatoires. |
| 5 | Garder `useWithdraw()` et `onSubmit` tels quels ? | **Oui**, on ne restyle que la forme. |

## Étape 3 — Plan d'intégration visuelle

### 3.1 Inventaire des écrans

**`#form` → `apps/helm/app/withdrawal/page.tsx`** (Client Component). Composants réutilisés : `Card`, `Input`, `Label`, `Button`, `Skeleton`, `Alert`. Structure : `<main>` centré (`max-w-md mx-auto px-4 py-8`, mobile-first) → `<Card>` → titre **« Montant à retirer »** → champ montant labellé → bouton submit pleine largeur. À créer : `Alert`/`Skeleton` via Shadcn si absents, `WithdrawalFormSkeleton`, message d'erreur inline. États déclinés : loading initial (`Skeleton`), erreur (`Alert role="alert"` + « Réessayer »), `isPending` (`<Button disabled>` + spinner), plafond atteint (si règle `WDR-xxx`), focus clavier visible.

**`#history` → `packages/ui/src/components/WithdrawalHistory`** (présentational, ne pas ajouter `"use client"` sans raison). Composants : `Table` & sous-composants, `Skeleton`, `Card`, `Badge` (statut si en maquette). Structure : `<Table>` sémantique, `<TableRow data-testid="withdrawal-row">` par ligne, `<TableHead>`. À créer : `Table` via Shadcn si absent, `WithdrawalHistorySkeleton`, état vide (`<TableCaption>` ou bloc « Aucun retrait pour le moment »). États : liste vide (message centré, pas table vide), loading (skeleton de lignes), erreur (`Alert`), responsive (`overflow-x-auto` sur mobile ou cartes empilées).

### 3.2 Mapping tokens (exhaustif, zéro `#hex`/`gray-XXX` dans le diff final) — cf. table étape 1, + hover bouton géré par le variant (`hover:bg-primary/90`), fond de page `bg-background`.

### 3.3 Garde-fous comportement (contrat de non-régression)

**`#form`** : `data-testid="withdrawal-amount-input"` (sur le `<Input>` montant, à l'identique), `data-testid="withdrawal-submit"` (sur le `<Button type="submit">`, à l'identique), texte **« Montant à retirer » mot pour mot** sur un élément visible (ne pas reformuler ; accents natifs en TSX, pas d'entité HTML en string JS), `onSubmit → useWithdraw()` **inchangé**, états de `useWithdraw()` (`isPending`, `error`) consommés jamais modifiés.

**`#history`** : `data-testid="withdrawal-row"` sur chaque `<TableRow>` de donnée (pas l'en-tête), à l'identique ; `role="table"` préservé (le `<Table>` Shadcn rend un `<table>` natif ; vérifier qu'un `overflow-x-auto` ne casse pas l'arbre ARIA) ; signature de props (`withdrawals`, `isLoading`, `error`) **inchangée**.

**Transverse** : aucun test modifié ; si une spec casse → le markup est en tort.

## Étape 4 — Intégration (protocole de supervision, 2 vues indépendantes)

**4.0** Le superviseur ne code pas : il découpe, délègue, contrôle la non-régression, agrège.

**4.1 Unités** :
| Unité | Vue | Worktree | Branche | Base | Fichiers autorisés |
|---|---|---|---|---|---|
| U1 | `#form` | `../full-project-withdrawal-form` | `feat/withdrawal-form-ui` | `feat/withdrawal-limits` | `apps/helm/app/withdrawal/page.tsx` + sous-composants locaux ; `globals.css` 1 ligne max si strictement nécessaire (a priori non) |
| U2 | `#history` | `../full-project-withdrawal-history` | `feat/withdrawal-history-ui` | `feat/withdrawal-limits` | `packages/ui/src/components/WithdrawalHistory/**` + ajout Shadcn `table`/`skeleton` si absent |

Si les deux unités doivent ajouter le même composant Shadcn (`skeleton`) : U2 l'ajoute en premier, U1 le consomme → sérialiser U1 après U2. Sinon parallèle.
```bash
git worktree add ../full-project-withdrawal-history -b feat/withdrawal-history-ui feat/withdrawal-limits
git worktree add ../full-project-withdrawal-form    -b feat/withdrawal-form-ui    feat/withdrawal-limits
```

**4.2 Prompt du sous-agent intégrateur** (général, frais — pas un fork), par unité : répertoire = worktree ; vue de maquette + annotations `WDR-xxx` verbatim ; fichiers autorisés (ne toucher à rien d'autre) ; chemin `CLAUDE.md` ; refs (`design-system-mapping.md`, `contrat-non-regression.md`, `patterns-integration.md`) ; **contrat à préserver explicite** (U1 : les 2 testids + texte exact + `onSubmit→useWithdraw()` + états ; U2 : testid row + `role="table"` + signature props) ; consignes (zéro couleur en dur, mobile-first, tous les états, `french-accents`, imports `@workspace/...`, `<button>` action / `<a>` navigation, labels liés) ; **ne jamais merger soi-même** — quand `pnpm build` + `pnpm lint` 0 erreur + specs de la vue vertes → rapport court.

**4.3 Contrôle de conformité — 2e sous-agent frais par unité** (jamais l'intégrateur). Entrée seulement : contrat verbatim + maquette + `git diff feat/withdrawal-limits...feat/withdrawal-<vue>-ui`. Checklist : (1) chaque testid/texte/ARIA du contrat toujours présent sur l'élément au même rôle ? (2) aucun handler/appel API/état/signature de props modifié ? (3) rejeu suite en worktree détaché :
```bash
git worktree add ../full-project-verify-<vue> --detach feat/withdrawal-<vue>-ui
cd frontend
pnpm --filter @workspace/ui test            # U2 (RTL WithdrawalHistory)
pnpm exec playwright test <spec withdrawal> # U1
pnpm build && pnpm lint
```
(4) conformité visuelle : couleurs **via tokens** (aucun `#2563eb`/`gray-XXX` dans le diff), états déclinés, responsive. Régression / test cassé / couleur en dur → **blocage** → relance ciblée une fois (si un test casse c'est le markup), sinon escalade.

**4.4 Gate bloquant** : vue livrable seulement si toutes les specs E2E/RTL qui passaient passent encore + `pnpm build` + `pnpm lint` 0 erreur.

**4.5 Agrégation — sans merger vers `dev`** : contrôle conformité par vue → MR de chaque branche vers **`feat/withdrawal-limits`** (`glab mr create --target-branch feat/withdrawal-limits --source-branch ...`), une à la fois, **confirmation utilisateur avant chaque merge** → `git worktree remove` (form, history, verify-*). **Jamais de merge vers `dev`** (builds Coolify).

## Étape 5 — Vérification visuelle & non-régression (globale, sur `feat/withdrawal-limits`)

1. `cd frontend && pnpm build && pnpm lint` → 0 erreur.
2. `pnpm exec playwright test` (spec withdrawal) + `pnpm --filter @workspace/ui test` → GREEN identique à avant. Si l'une casse → corriger le **markup** (testid remis sur le bon élément, texte remis mot pour mot), jamais le test.
3. Vérif visuelle vs maquette (via `/run` ou `/verify`, `dev-worktree.sh`) : `#form` (hiérarchie titre→champ→bouton, bouton pleine largeur `primary`, carte `bg-card`), `#history` (table lisible), responsive 360→1280px, dark mode (`.dark`), états non-nominaux ajoutés.
4. Checklist d'écart :
| Écart | Statut | Raison |
|---|---|---|
| Teinte `#2563eb` → `bg-primary` | Assumé | consigne : réutiliser `primary` |
| `gray-100` → `bg-card` | Assumé | traduction sémantique, suit le dark mode |
| Rayons/ombres légèrement différents | Assumé | conventions `<Card>` / `--radius` priment |
| États loading/vide/erreur ajoutés | Assumé (ajout) | non négociables |
| Table mobile scroll vs cartes | À valider visuellement | selon la maquette |
| Tout `#hex`/`gray-XXX` résiduel dans le diff | **À corriger — bloquant** | zéro couleur en dur |

## Étape 6 — Résumé de fin de chantier

- **Maquette intégrée** : `docs/maquettes/withdrawal.html` — 2 vues (`#form`, `#history`).
- **Branche** : `feat/withdrawal-limits` (MR depuis `feat/withdrawal-form-ui` et `feat/withdrawal-history-ui`, worktrees supprimés). **Aucun merge vers `dev`.**
- **Design system respecté** : `#2563eb` → token `primary` existant (aucun nouveau token) ; `gray-100` → `bg-card` ; composants `Card`/`Input`/`Label`/`Button`/`Table`/`Skeleton`/`Alert` de `packages/ui`, manquants ajoutés via Shadcn ; **zéro couleur en dur** ; police non réimportée.
- **Fichiers modifiés (forme uniquement)** : `apps/helm/app/withdrawal/page.tsx` (+ sous-composants skeleton/erreur) ; `packages/ui/src/components/WithdrawalHistory/**` (+ composants Shadcn ajoutés).
- **Non-régression** : testids `withdrawal-amount-input`, `withdrawal-submit`, `withdrawal-row` préservés ; texte « Montant à retirer » mot pour mot ; `role="table"` conservé ; `onSubmit → useWithdraw()` et états inchangés ; signature props `WithdrawalHistory` inchangée ; specs X/X E2E + Y/Y RTL GREEN ; build+lint 0 erreur.
- **Couverture états & responsive** : loading/skeleton, vide, erreur (`role="alert"` + retry), disabled (`isPending`), focus visible ; mobile-first 360→1280 ; dark mode via tokens.
- **Écarts assumés** : teinte bouton alignée sur `--primary`, fonds/rayons alignés sur `<Card>`, états non-nominaux ajoutés.
- **À suivre** : confirmer rendu table mobile (scroll vs cartes) ; si règle de plafond `WDR-xxx` annotée dans le HTML, câbler le message « plafond atteint » avec la vraie valeur de `useWithdraw()`.
