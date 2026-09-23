# Cartographies & règles non négociables — ActivCreew

À lire à l'étape 3 (plan d'implémentation) pour dresser la liste des fichiers à créer
par couche et vérifier les conventions. Fichier évolutif : toute nouvelle règle projet
ou nouvelle couche s'ajoute ICI, pas dans SKILL.md.

## Cartographie Backend (Strapi v5)

Pour chaque domaine couvert par les tests, identifie les fichiers à créer :

| Couche | Fichier | Skill |
|--------|---------|-------|
| Schema | `src/api/<m>/content-types/<m>/schema.json` | (cf. Pattern Schema dans `patterns-activcreew.md`) |
| Routes | `src/api/<m>/routes/<m>-custom.ts` | `strapi-routes` |
| Controller | `src/api/<m>/controllers/<m>.ts` | `strapi-controllers` |
| Service pur | `src/api/<m>/services/<m>-validation.ts` | — |
| Service Strapi | `src/api/<m>/services/<m>.ts` | `strapi-queries` |
| Lifecycle | `src/api/<m>/content-types/<m>/lifecycles.ts` | `strapi-lifecycles` |
| Permissions | `config/permissions.json` | `/sync-permissions` |

**Règles Strapi v5 non négociables** :
- `strapi.documents()` pour toutes les **écritures** (create/update/delete)
- Knex (`strapi.db.connection`) uniquement pour les **lectures** complexes (agrégation, COUNT) — jamais pour les écritures (pas de lifecycles déclenchés)
- `documentId` (UUID) jamais `id` dans les CRUD
- `console.log('[NomModule] message')` pour le logging, jamais `strapi.log`
- `draftAndPublish: false` par défaut sauf exception justifiée

**SOLID check Backend** :
- Le controller ne contient que du routage (validation input → appel service → réponse)
- La logique métier est dans les services
- Les fonctions pures (sans Strapi) sont dans un fichier séparé `*-validation.ts`

## Cartographie Frontend (Next.js)

Pour chaque spec E2E, identifie :

| Couche | Fichier | Skill |
|--------|---------|-------|
| Composant UI | `packages/ui/src/components/<C>/` | `nextjs-component` |
| Page | `apps/<app>/app/<route>/page.tsx` | `nextjs-routing` |
| Store | `packages/kernel/src/stores/<s>.ts` | `nextjs-state` |
| Hook SWR | `packages/kernel/src/hooks/use<H>.ts` | `nextjs-swr` |
| Accents TSX | Tout fichier `.tsx` | `french-accents` |

**Règles Next.js non négociables** :
- Cookies SSR → `const cookieStore = await cookies(); headers: { Cookie: cookieStore.toString() }`
- Imports monorepo → `@workspace/package-name/path` (pas de `src/` explicite)
- `data-testid` sur tout élément interactif couvert par un test E2E
- Pas de `useEffect + fetch` → SWR (`useSWR`) systématiquement

**SOLID check Frontend** :
- Un composant = une responsabilité (affichage ≠ logique métier ≠ appel API)
- La logique d'appel API est dans les hooks SWR, pas dans les composants
- Les stores Zustand n'ont pas de logique d'effets de bord
