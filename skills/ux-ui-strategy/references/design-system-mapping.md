# Design system ActivCreew — lecture & table de traduction

À lire à l'étape 1 (avant de planifier). Fichier évolutif : tout nouveau token,
composant ou correspondance maquette→projet s'ajoute ICI, pas dans SKILL.md.

## Où lire le design system

1. `frontend/packages/ui/src/styles/globals.css` → les tokens HSL (`--primary`,
   `--muted-foreground`, `--card`, `--sidebar-*`, `--radius`…) et le dark mode.
2. `frontend/packages/tailwind-config/tailwind.config.ts` → les couleurs sémantiques
   mappées sur les tokens, le `container`, les `screens`.
3. `frontend/packages/ui/src/components/` → l'inventaire des composants disponibles
   (`shadcn/button`, `shadcn/card`, `shadcn/input`, `shadcn/dialog`…), rangés par
   origine : `shadcn/`, `originui/`, `magicui/`, `aceternity/`, `other/`.
4. Un écran voisin déjà intégré (même app, même famille) → relève le style réel
   (espacements, tailles de titres, structure de page, usage des variants).
5. `CLAUDE.md` → règles critiques transverses (imports monorepo `@workspace/...`,
   `french-accents` en TSX, Server vs Client component).

## Table de traduction maquette → projet

La maquette (`docs/maquettes/**`) est souvent du HTML brut avec Tailwind CDN et des
couleurs en dur. **Ne recopie jamais ces valeurs en dur.** Traduis-les :

| Maquette (à traduire) | Projet (cible) |
|-----------------------|----------------|
| `bg-brand-600`, `#16a34a` | token sémantique → `bg-primary` (ou la couleur de marque mappée) |
| `text-gray-900`, `text-gray-500` | `text-foreground`, `text-muted-foreground` |
| `border-gray-200` | `border-border` / `border` |
| `bg-white` carte | `bg-card` / composant `<Card>` |
| `bg-gray-100` fond | `bg-background` / `bg-muted` |
| `<button class="...">` | `<Button variant=… size=…>` de `packages/ui` |
| `<input class="...">` | `<Input>` / `<Form>` Shadcn |
| `rounded-2xl shadow-sm` ad hoc | conventions de la `<Card>` existante |
| Font Inter inline | la police déjà configurée globalement (ne pas réimporter) |

> La maquette donne l'**intention** (hiérarchie, espacements, états, parcours). Le design
> system donne l'**implémentation**. Le dark mode et la cohérence inter-app viennent
> gratuitement quand tu passes par les tokens HSL plutôt que par des couleurs en dur.

## Skills front à appliquer selon le sujet

| Sujet | Skill |
|-------|-------|
| Server vs Client, structure composant | `nextjs-component` |
| Accents en TSX | `french-accents` (AUTOMATIQUE) |
| Formulaires (don, profil) | `nextjs-forms` |
| Loading / skeleton / error | `nextjs-loading` |
| Tableaux | `nextjs-datatable` |
| Re-renders (composants lourds, stores) | `nextjs-rerender` |
| Imports `@workspace/...` | `monorepo-imports` |
| Classes Tailwind v4 | `tailwind-v4-migration` |
| Nouveau service externe (font, CDN) | `csp-management` |
