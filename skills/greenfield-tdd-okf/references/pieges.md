# Pièges connus

Fichier append-only : ajouter chaque nouveau piège sous la section de la stack concernée
(créer la section si besoin, la dater). Ne consulter que les sections correspondant à la
stack du projet en cours — inutile de charger le reste en contexte.

## Génériques (toute stack)
- Webhooks inter-services : HMAC-SHA256 hex + comparaison timing-safe, contrat de payload
  partagé (schéma validé des deux côtés).
- Numérotation légale : transaction + contrainte unique (memberId, year, seq).
- Feature qui a besoin d'un secret/SMTP externe : prévoir un mode simulé (jsonTransport)
  pour que l'app tourne sans config ; le vrai transport s'active si la variable d'env est présente.
- Rendre en headless une page protégée : jeton court (JWT) lié au chemin, autorisé dans le proxy.
- Intl fr-FR : séparateurs = espaces insécables ; comparer via le formateur, pas une chaîne écrite.
- IP client pour rate-limit : `x-forwarded-for` est une liste pré-remplissable par le
  client (le 1er élément est forgé). Ne faire confiance qu'aux proxies qu'on opère, qui
  ajoutent à DROITE → vraie IP = Nième depuis la fin, N = `TRUSTED_PROXY_COUNT` d'env.
  Défaut sûr = 0 (header ignoré). Lire l'env dans la fonction, pas au chargement du module.
- CI qui lance `vitest` + un build d'app ne type-check PAS les packages sans étape de
  build (ex. `packages/services`) : les fakes de repo dans les tests dérivent en silence
  dès qu'une interface gagne une méthode. Prévoir un `typecheck: tsc --noEmit` par package
  testable + un step CI dédié, dès le bootstrap.

## Next 16 / TypeScript (2026-07, projet CRM_TEAM)
- npm workspaces + `exports` + `turbopack.root` pour un package TS partagé.
- jose/crypto sous vitest jsdom → `// @vitest-environment node` sur les tests de services.
- tsx/seeds : `import "dotenv/config"` obligatoire.
- Next : `new Response(new Uint8Array(buffer))` — BodyInit n'accepte pas Buffer directement.
- Drag & drop : HTML5 dataTransfer + useOptimistic + server action typée, zéro dépendance.
- `next start` force `NODE_ENV=production` → masque tout `console.log` gardé par
  `NODE_ENV !== "production"` (ex. lien magic-link en transport simulé). Un e2e qui lit
  les logs serveur doit tourner sous `next dev`.
- `apps/web` sans `vitest.config.ts` : l'alias `@/*` n'est pas résolu sous Vitest. En
  ajouter un (mappe `@/*` → `./`) dès qu'un test importe un module applicatif.
- `process.env` (type `ProcessEnv`) n'a « aucune propriété commune » avec un type objet
  fermé : une fonction qui prend `env` en paramètre injectable (défaut `process.env`) doit
  le typer `Record<string, string | undefined>`, pas `{ MA_VAR?: string }` (TS2322 au
  `next build`, invisible sous `vitest`).

## Prisma 7 (2026-07)
- Generator `prisma-client`, prisma.config.ts + dotenv, driver adapter requis.

## MCP / serveur de tools (2026-08, projet carte_fidelite)
- `mcp-handler` (route handlers Next) v2 dépend de `@modelcontextprotocol/server` ^2, PAS
  de `@modelcontextprotocol/sdk` 1.x. API v2 : `server.registerTool(name, { title,
  description, inputSchema: z.object({...}) }, cb)` (plus de `server.tool()`) ; l'auth de
  la requête est sous `ctx.http?.authInfo`. Fichier `app/[transport]/route.ts`, l'URL
  client réelle est `/mcp` (le segment est cosmétique). `export const runtime = "nodejs"`
  obligatoire (le SDK utilise des built-ins Node).
- `withMcpAuth` ne fait que 401/403 (RFC 9728). Pour un rate-limit par identité ou une
  résolution de token maison : wrapper manuel `authenticateMcpRequest(req) -> 401 | 429 |
  { context }`, puis un handler MCP construit par requête avec le `context` capturé en
  closure (les handlers de tools le lisent sans re-parser le token). Rate-limiter par
  identité d'agent (`mcp:<agentClientId>`), pas par IP.
- Erreur métier d'un tool : `throw new Error(<message générique>)` dans le handler
  `tools/call` → le SDK le convertit en `{ content, isError: true }`. Le message doit être
  la valeur d'une constante partagée (anti-fuite + test par égalité stricte).
- Tester un tool : extraire `run<Tool>({ repo, context }, args)` pur/testable ;
  `registerTool` reste un wrapper mince non testé unitairement (couvert par l'e2e).
- e2e d'un tool sans SDK client : JSON-RPC brut en POST sur `/mcp` avec
  `Accept: application/json, text/event-stream`, séquence `initialize` →
  `notifications/initialized` → `tools/list` → `tools/call`. Plus lisible dans un transcript.

## Python & interop Python ↔ TS (2026-07)
- pydantic→zod : `by_alias=True, exclude_none=True` (zod `.optional()` refuse null).
- Scrapling : navigateurs via l'exe `scrapling install`, pas `python -m scrapling` ; le
  Playwright ainsi installé est réutilisable pour du rendu PDF (ne pas réembarquer Chromium).
