# Pièges connus

> **Fichier partagé** — copie identique dans `greenfield-bootstrap`, `tdd-feature-okf`
> et `tdd-backlog-run`. Toute addition doit être répliquée dans les 3.

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
- Durcir l'auth d'une page servie AUSSI à un service machine (rendu headless, webhook…) :
  rejouer l'E2E de TOUS les consommateurs existants, pas seulement le navigateur (2026-07-10 :
  requireMember ajouté aux pages print a cassé le PDF headless sans que la CI le voie).
- E2E d'un formulaire web : réutiliser le Playwright déjà présent dans le projet (script de
  quelques lignes) plutôt que simuler le POST du framework à la main.
- Identité dans une API machine (MCP, webhook…) : jamais en paramètre déclaratif du schéma —
  toujours dérivée du credential (bearer → lookup), sinon usurpation triviale entre tenants.
- Changer la source de vérité d'un état (champ statut → dérivé d'écritures) : migrer AUSSI
  les données historiques (backfill), pas seulement le schéma — les nouveaux consommateurs
  voient sinon un trou silencieux.
- Gros module multi-modèles : UNE migration au départ, puis features = services/UI/tools
  seulement. (2026-07, CRM_TEAM)
- Un service (uvicorn, worker…) lancé sans --reload AVANT une modif sert l'ancien code
  pendant l'E2E « réel » sans aucun signal : redémarrer les services touchés avant l'E2E.
- Windows : tuer le shell `npm run start` ne tue pas node → port occupé par un orphelin qui
  sert l'ANCIEN build (E2E faussement rouge). netstat -ano | grep <port> puis taskkill //F.
- E2E avec process de fond (2026-08-26) : un serveur lancé en tâche de fond peut mourir
  silencieusement entre deux commandes shell — avant de déboguer une erreur réseau côté
  client comme un bug de code, revérifier que le process tourne encore (`ps`/`curl`) et que
  le contenu servi est à jour (`curl` direct sur le fichier statique).
- E2E avec plusieurs agents/issues en parallèle sur le même dépôt (2026-08) : le port par
  défaut du serveur de dev est souvent occupé par l'instance d'un autre agent — vérifier
  (`lsof -i :PORT`), prendre un port libre plutôt que tuer un process qu'on n'a pas lancé.
- API avec CORS sur une liste d'origines fixe (2026-08-27, projet avel-finances) : lancer
  le frontend sur un port hors allowlist (ex. pour éviter l'instance d'un autre agent)
  casse tout `fetch` navigateur avec un « Failed to fetch » générique, alors qu'un `curl`
  direct répond — faux diagnostic côté code. Vérifier d'abord que le port réel du frontend
  est dans l'allowlist.
- FastAPI/Starlette `CORSMiddleware(allow_methods=[...])` (2026-08-28) : un `TestClient`
  ne fait pas de vraie préflight (OPTIONS) — oublier PUT/DELETE dans `allow_methods` en
  ajoutant un endpoint ne fait échouer AUCUN test ; seul un vrai navigateur le voit.
- E2E d'idempotence : tester le rejeu sur une ressource DISPONIBLE. Sur une ressource saturée
  (créneau plein…), aucune écriture n'a lieu et les deux appels renvoient la même erreur —
  faux positif. Toujours vérifier aussi le négatif (sans clé → deux entités distinctes).
- E2E d'une feature basée sur des DONNÉES PASSÉES quand l'API interdit le passé : seeder
  l'historique directement dans la base réelle (`docker exec <conteneur> psql`, CTE
  `INSERT ... RETURNING`), puis interroger l'API. C'est un vrai E2E, pas un contournement.
- Tester l'expiration d'un jeton sans attendre ni mocker l'horloge (2026-08-27) : si le
  store expose une durée de validité, ouvrir une 2e connexion au même fichier de données
  que le serveur testé et créer directement un jeton à durée négative.
- Rendu HTML par concaténation de chaînes (pas de template engine) : tout champ venant d'une
  API/tiers doit être échappé avant insertion — sinon XSS ; couvrir d'un test dédié.
- Onglets qui partagent un seul conteneur DOM rempli par des vues async (2026-08-26) :
  changer d'onglet avant la fin d'un fetch laisse la réponse tardive écraser l'onglet
  affiché, sans erreur console. Un conteneur privé et permanent par vue (masqué via
  `display`, jamais détruit/recréé).
- Un handler qui capture une exception générique (ex. `except ValueError`) pour deux cas
  différents (conflit vs requête invalide) fige un seul code de statut : une nouvelle
  validation levant la même exception en hérite en silence (409 sur une valeur invalide).
  Vérifier ce que le handler fait de CHAQUE exception ; distinguer sur le type.
- Heuristique de filtrage de contenu : cibler le vocabulaire de la catégorie à exclure,
  jamais celui du domaine métier (partagé avec les faux positifs) ; seuil ≥ 2 signaux.
- Autocomplétion/recherche : `includes` + troncature sans TRI de pertinence = résultats
  perçus comme aléatoires. L'ordre est la feature : trier (préfixe > mot interne >
  inclusion) AVANT de couper, et tester le CLASSEMENT, pas la présence.
- Extraction d'un nom propre par regex après avoir retiré les balises : convertir les
  balises en `\n` (pas en espace) et interdire au motif de franchir un saut de ligne,
  sinon le nom avale le libellé du bloc suivant.
- Un DSL de sécurité (sandbox, firewall, policy…) dont un exemple public utilise une syntaxe
  ne prouve pas que cette syntaxe couvre le cas voulu — vérifier contre le vrai moteur
  avant d'écrire une doc ou un plan (2026-07-31, kern-exec : `(remote ip "1.2.3.4:443")` de
  Seatbelt *parse*, mais `host` n'accepte que `*`/`localhost` en vrai).
- `.gitignore` d'un template Python (`lib/`, `build/`, `dist/` non ancrés) dans un dépôt
  mixte Python + front : il avale `frontend/src/lib/` sans bruit. Tout marche sur la
  machine d'origine, un clone frais ne compile pas (2026-09-23, MALA). Ancrer (`/lib/`)
  ou ajouter une négation, et vérifier le build depuis un `git clone` frais au bootstrap.
- Sous-agents en parallèle : jamais de `pkill -f <motif>` ni de `kill` par port qu'on n'a
  pas ouvert soi-même — on tue le démon d'un autre agent. Arrêter ses processus par PID,
  et donner à chaque agent son port dédié dans le prompt (2026-09-23, MALA).
- Dans chaque prompt de sous-agent en parallèle, nommer la zone de fichier qu'il a le droit
  de toucher (« seule la ligne X de `process()` ») et réserver d'avance les numéros de
  fiche OKF : les merges n'ont plus buté que sur l'append de `retro.md` (2026-09-23, MALA).

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
- `redirect()` de Next lance une exception : jamais DANS un try/catch qui l'avalerait.
- `cookies().set()` dans une server action force un refresh RSC : si la page re-rendue
  change de branche, le composant client est démonté (état perdu — fatal pour un secret
  affiché une seule fois). Séparer action-données (retourne la session) et
  action-cookie+redirect (au clic suivant).
- Server actions de pages publiques : erreurs en valeurs de retour ({ ok, error }), jamais
  throw (messages masqués en prod).
- Composant réutilisable à travers la frontière RSC : passer DONNÉES + server actions, jamais
  de fonction de rendu en prop.
- Pages serveur : annoter les params `.map`/`.filter` (`Awaited<ReturnType<typeof fn>>[number]`)
  pour éviter « implicit any » sur les types Prisma profonds.
- `create-next-app` refuse un dossier non vide : bootstrapper dans un dossier scratch puis
  copier les fichiers utiles (pas `node_modules`, réinstaller à la racine).
- `npx tsc --noEmit` seul échoue sur les types générés par Next (ex. `LayoutProps`) :
  `npm run build` (ou `next build`) pour un typecheck fiable. (2026-08, domain_finder)
- `next dev` (Next 16) append un bloc `<!-- BEGIN:nextjs-agent-rules -->` à `CLAUDE.md`
  à chaque démarrage — ne pas le retirer, le committer. (2026-08, domain_finder)
- `tsx -e "…"` transpile en CJS : top-level await interdit → IIFE async. Les alias `@/`
  (tsconfig paths) sont, eux, résolus par tsx.
- Script de vérif ad hoc en TS : un vrai fichier DANS le package (imports relatifs
  `../src/*`), pas `tsx -e` (interop ESM/CJS → exports nommés undefined) ni hors du repo.
- Scripts tsx d'E2E : les exécuter depuis le dossier de l'app (imports relatifs), pas la racine.

## Prisma 7 (2026-07)
- Generator `prisma-client`, prisma.config.ts + dotenv, driver adapter requis.
- Après `prisma migrate dev`, relancer `npx prisma generate` si le build ne voit pas les enums.
- Après `migrate dev` + `generate`, REDÉMARRER le serveur dev : l'ancien client reste en
  mémoire (« Unknown argument » au runtime alors que le build passe).
- `where: { x: { in: [...] as const } }` refusé (readonly) : typer la liste avec l'enum généré.
- Agent/CI (shell non-interactif) : `prisma migrate dev` refuse de tourner → `prisma migrate
  diff --from-config-datasource --to-schema <schema> --script` écrit dans
  `prisma/migrations/<timestamp>_<nom>/migration.sql`, puis `prisma migrate deploy`.

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

## MCP Rust / rmcp 3.x (2026-09, projet screen_forge)
- Un `todo!()`/panic dans un handler `#[tool]` ne renvoie JAMAIS de réponse : le client
  attend indéfiniment (suite de tests bloquée, pas rouge). Tests via client in-process
  (`tokio::io::duplex` + `().serve(client_io)`) : envelopper `call_tool` dans
  `tokio::time::timeout`.
- `#[tool_handler]` sans `router = self.tool_router` reconstruit le routeur à chaque
  appel et laisse le champ `tool_router` inutilisé (warning « never read »).
- Serveur stdio : stdout = protocole. Tout diagnostic sur stderr (`eprintln!`), jamais
  `println!`.
- Image renvoyée au modèle : `ContentBlock::image(base64, "image/png")` en bloc séparé,
  pas du base64 dans le JSON texte — vérifié en E2E via `claude -p --mcp-config <json>
  --strict-mcp-config` (ne touche pas la config MCP globale).

## Tauri v2 (2026-09, projet screen_forge)
- Déposer un fichier sur la fenêtre : Tauri l'intercepte par défaut (`dragDropEnabled`
  = true) → la WebView ne reçoit JAMAIS l'événement HTML `drop`, sans erreur. Mettre
  `"dragDropEnabled": false` sur la fenêtre dans `tauri.conf.json`, ou écouter
  `onDragDropEvent` côté Tauri (chemins de fichiers).
- E2E du front sans l'app : Playwright sur le serveur Vite + `page.addInitScript` qui
  définit `window.__TAURI_INTERNALS__ = { transformCallback, invoke }` (stub des
  commandes). Ne couvre PAS les réglages de fenêtre Tauri : les valider dans la vraie app.
- Arguments de commande : `fn cmd(canvas_json: String)` côté Rust ↔ `invoke("cmd",
  { canvasJson })` côté JS (camelCase par défaut).
- `[profile.release]` d'un crate membre est ignoré : le mettre dans le `Cargo.toml`
  racine du workspace.
- `tauri dev` : la fenêtre de l'app peut garder l'ANCIEN front alors que Vite sert les
  nouveaux fichiers (rechargement à chaud non appliqué, sans erreur). Avant de faire
  tester un changement de front à un humain, relancer l'app de dev.

## Fabric.js 7 (2026-09, projet screen_forge)
- `originX/originY` valent `center` par défaut (≠ v5/v6) : `left/top` = centre de
  l'objet. Placer au centre de la vue avec `canvas.getVpCenter()` directement.
- Propriétés métier sérialisées : `FabricObject.customProperties = [...]` (statique),
  puis `canvas.toObject()` / `loadFromJSON` les conservent.
- pnpm 11 : `canvas` (node-canvas, dépendance optionnelle de fabric) bloque
  `install --frozen-lockfile` → `allowBuilds: { canvas: false }` dans
  `pnpm-workspace.yaml` quand le rendu se fait dans un navigateur/WebView.
- Fabric 7 `Line` a un `fill` noir par défaut (jamais dessiné) : tout export de style
  (couleurs pour un agent, CSS) doit ignorer le remplissage des lignes.
- Dégradés Fabric : `gradientUnits: "percentage"` + coordonnées 0..1 = indépendant de la
  taille de l'objet ; `toObject`/`loadFromJSON` conservent l'objet `Gradient`.
- Fabric 7 `Path` déplacé/redimensionné : ses données de chemin ne changent pas. Pour
  retrouver les points en coordonnées scène : `new Point(p.x - obj.pathOffset.x,
  p.y - obj.pathOffset.y).transform(obj.calcTransformMatrix())`.
- Paper.js crée un canvas dès son CHARGEMENT : sous jsdom (Vitest), « unable to provide a
  2D context » avant même le test. `vi.hoisted` qui remplace
  `HTMLCanvasElement.prototype.getContext` par un contexte factice (Proxy no-op) AVANT
  l'import ; les booléens (unite/subtract/intersect/exclude) sont de la géométrie pure.
- Résultat booléen composé (exclude) : les aires signées des morceaux s'annulent
  (`area` = 0) — tester le vide avec `isEmpty()` et les dimensions de `bounds`.

## Vitest + Testing Library (2026-09)
- Sans `globals: true`, Testing Library ne nettoie pas le DOM entre les tests (rendus
  empilés, « Found multiple elements ») : `afterEach(cleanup)` dans le setup.

## CSS / mise en page (2026-09, projet screen_forge)
- Élément de taille fixe (`<canvas>`, image) dans un enfant `flex-1` : l'enfant ne
  rétrécit jamais sous son contenu (`min-width: auto`) → le panneau voisin est poussé
  hors écran. Pire : focaliser un champ de ce panneau fait DÉFILER le conteneur même en
  `overflow-hidden` → tout se décale, les clics tombent à côté, sans erreur. `min-w-0`
  sur l'enfant flex. Diagnostic : `scrollLeft` des ancêtres + `getBoundingClientRect()`.

## macOS capture d'écran / TCC (2026-09, projet screen_forge)
- Sans l'autorisation « Enregistrement de l'écran », `CGWindowListCopyWindowInfo` ne
  donne pas `kCGWindowName` → xcap (qui le lit) ne liste que la barre de menus. Liste vide
  ≠ bug de filtre : vérifier `CGPreflightScreenCaptureAccess()` d'abord.
- En `tauri dev`, l'autorisation appartient au TERMINAL parent (processus responsable),
  et l'accorder oblige à quitter ce terminal → tester la capture dans l'app packagée.
- App signée ad hoc : chaque rebuild change l'identité ; les Réglages montrent l'ancienne
  autorisation cochée mais la nouvelle build est refusée (redemande en boucle).
  `tccutil reset ScreenCapture <bundle-id>` puis réaccorder, à chaque rebuild.
- `kCGWindowListOptionOnScreenOnly` = bureau (Space) courant seulement : ramener l'app au
  premier plan fait changer de bureau et la fenêtre cible disparaît de la liste.
- Filtrer les fenêtres par `kCGWindowLayer == 0`, jamais par nom d'app (noms localisés :
  « Centre de notifications »). L'outil Capture d'écran laisse une fenêtre plein écran
  100 % transparente devant tout.
- « Fenêtre au premier plan » = plus grande fenêtre de l'app de tête, pas la 1re de la
  liste : Chrome plein écran empile des calques de barre d'onglets transparents devant.
- Identifiant de bundle se terminant par `.app` : avertissement Tauri, conflit avec les
  bundles macOS — le choisir dès le scaffold (changer plus tard reset les autorisations).
- Diagnostic sans autorisation : un binaire Swift de 15 lignes qui dump
  `CGWindowListCopyWindowInfo` (owner, layer, alpha, bounds) — propriétaire, niveau et
  taille restent lisibles, seuls les titres sont masqués.

## Rust / E2E de binaire (2026-09, projet screen_forge)
- `cargo test` ne reconstruit PAS le binaire `[[bin]]` de `target/debug/` (il compile
  un harnais de test) : un E2E qui lance ce binaire après un changement de modèle teste
  l'ANCIEN code, avec une erreur trompeuse. `cargo build -p <crate>` avant chaque E2E,
  et vérifier la date du binaire en cas de doute.
- Capture d'écran relue via un visualiseur d'images : elle peut être affichée réduite.
  Ne jamais mesurer des tailles/positions sur l'image affichée — mesurer dans la page
  (getBoundingClientRect, pixels d'une ligne capturée).

## Tauri v2 sidecar / intégration clients MCP (2026-09, projet screen_forge)
- `bundle.externalBin` est vérifié par tauri-build à la COMPILATION : le déclarer dans
  `tauri.conf.json` casse `cargo test`/CI tant que le binaire n'est pas construit. Le
  mettre dans une config de packaging séparée (`tauri build --config <fichier>`) dont le
  `beforeBuildCommand` construit et copie `binaries/<nom>-<triple>`. Dans le bundle, le
  binaire atterrit à côté de l'exécutable (`current_exe().with_file_name(nom)`), comme en
  dev dans `target/debug/` — un seul chemin de résolution.
- App lancée depuis le Dock : pas le PATH du terminal → trouver une CLI (`claude`, `node`…)
  via un shell de connexion `$SHELL -lc 'command -v <cli>'`.
- Enregistrer un serveur MCP dans Claude Code : `claude mcp add --scope user <nom> -- <bin>`
  (supprimer l'entrée avant : `add` refuse un nom existant). Ne pas éditer `~/.claude.json`.
- Claude Desktop : fusionner `claude_desktop_config.json` (garder les autres clés, refuser
  un fichier illisible, sauvegarder l'original), et le client lance le serveur SANS dossier
  de projet → prévoir un repli (ex. projet ouvert dans l'app). Il réécrit lui-même ses
  `preferences` au redémarrage : comparer par chemin de clé.

## Évolution d'un format de fichier partagé (2026-09, projet screen_forge)
- serde (comme la plupart des parseurs JSON) IGNORE les champs inconnus par défaut : un
  lecteur compilé avant l'ajout d'un champ lit les nouveaux fichiers sans erreur et perd
  le champ en silence. Quand un binaire installé ailleurs (bundle, serveur enregistré dans
  un client) lit le format, le reconstruire/redéployer fait partie de la feature.

## Python & interop Python ↔ TS (2026-07)
- pydantic→zod : `by_alias=True, exclude_none=True` (zod `.optional()` refuse null).
- Scrapling : navigateurs via l'exe `scrapling install`, pas `python -m scrapling` ; le
  Playwright ainsi installé est réutilisable pour du rendu PDF (ne pas réembarquer Chromium).
- Presidio en langue non-anglaise (2026-08) : les moteurs par défaut chargent un modèle
  spaCy ANGLAIS, sans erreur — juste zéro entité détectée. Câbler
  `NlpEngineProvider(nlp_configuration={"nlp_engine_name": "spacy", "models": [{"lang_code":
  "fr", "model_name": "fr_core_news_lg"}]}).create_engine()` → `AnalyzerEngine(nlp_engine=...,
  supported_languages=["fr"])` → `ImageAnalyzerEngine(analyzer_engine=...)` →
  `ImageRedactorEngine(image_analyzer_engine=...)`. Langue OCR (Tesseract `lang: "fra"`,
  ISO 3 lettres) et langue Presidio (`language="fr"`, ISO 2) sont deux réglages distincts.

## API tierces (2026-07)
- API paginée par token de continuation (Google Places nextPageToken, etc.) : le token doit
  être DEMANDÉ dans la projection/FieldMask, sinon l'API ne le renvoie jamais — pagination
  silencieusement bornée à la 1re page. Tester `limit > pageSize` avec un mock multi-pages.
- E2E sur une API à identité personnelle (token par utilisateur) : compte de test dédié
  (email réservé), jamais le credential d'un vrai utilisateur.

## Contrats inter-services (toute stack, 2026-07, projet Kern)
- **Fixture de contrat exécutable** : le même fichier JSON dans `contracts/` des deux repos,
  chaque côté assertant contre lui (producteur : « j'émets exactement ça » ; consommateur :
  « j'accepte exactement ça »). La dérive devient un test rouge. Si deux fichiers de test du
  même paquet assertent la même fixture, les patcher ensemble.
- **Un identifiant qui ressemble à un autre n'est pas le même** : avant de joindre deux
  domaines sur un nom, vérifier que le lien est déclaré et non deviné.
- **Une spec écrite depuis une maquette est plus large que le contrat réel** : que vaut
  chaque champ aujourd'hui chez le producteur ? Un champ constant sur toutes les lignes ne
  transporte aucune information.
- **Ne jamais faire traverser un chemin de fichier** : c'est un interne, pas un contrat.
- **404 vs 200 vide** : « aucun producteur n'a parlé » et « le producteur n'a rien » sont deux
  faits distincts. Les confondre fait afficher un écran qui affirme ce qu'on ignore.
- Un état ressource publié en ENTIER à chaque fois évite d'inventer un protocole de
  suppression, tant que la charge tient dans un paquet.
- Vérifier un état « en cours » en E2E demande un vrai travail lent : un stub instantané
  montre l'état final et laisse croire que la dérivation marche.

## Go (2026-07, projet Kern-Orch)
- Typed-nil : un pointeur nil typé (ex. `(*bytes.Buffer)(nil)`) rangé dans un champ
  interface produit une interface NON nil → `if w == nil` échoue → panic. N'assigner un
  pointeur à un champ interface que s'il est non-nil.
- Subprocess streaming : tester le vrai chemin avec un process externe réel (script sh dans
  `t.TempDir()`) en plus du pattern `TestHelperProcess` (`GO_WANT_HELPER_PROCESS=1`).
- Fan-out concurrent : un `Clone()` du state par branche, merge sur une seule goroutine dans
  un ordre stable ; valider avec `go test -race`.

## Go / JSON (2026-08, projets Kern et kern-billing)
- Struct sans tags `json:"..."` : sérialise en PascalCase sur le fil, et à la lecture ne
  convertit jamais `snake_case` → tout reste en zéro-value, sans erreur. Le bug apparaît
  ailleurs (validation au message trompeur, ex. « cost must be positive »), et `go test` ne
  le voit pas s'il asserte la struct décodée. Tags dès qu'un type devient un contrat + un
  test de round-trip JSON par type exposé.
- `var list []T` reste `nil` sans élément → `json.Marshal` produit `null`, pas `[]`, et un
  client JS qui fait `.map()` plante. `make([]T, 0)` pour toute slice destinée au JSON.

## Go / PostgreSQL (2026-08, projet kern-billing)
- `golang-migrate/.../database/pgx/v5` : dépendance transitive (`jackc/pgerrcode`) absente
  de `go.sum` tant qu'on n'a pas fait `go get .../database/pgx/v5@<version>` explicitement.
- Tester une couche Postgres réelle (pas de mock SQL) : `docker compose up -d postgres` +
  variable d'env de test, `t.Skip()` propre si absente. Un skip n'est pas un vert : lire
  le couple (passés, skippés).
- `DROP CONSTRAINT` sur une PK échoue (`SQLSTATE 2BP01`) si une FK en dépend : DROP la FK
  d'abord, la reconstruire après la nouvelle PK ; la down-migration fait l'ordre inverse.
- Un échec de migration golang-migrate laisse `schema_migrations` à `dirty=true` même si
  Postgres a tout annulé (schéma intact) — nettoyer à la main
  (`UPDATE schema_migrations SET dirty=false, version=<dernière bonne> WHERE version=<échouée>`).

## Go / kern-link (2026-08, projet kern-billing)
- `providers.Models(nil)` tire tout le catalogue (Bedrock, Codex, Vertex…) et ses
  dépendances (AWS SDK v2, websocket, zstd…) — `go mod tidy` avant la première build.
- `Authorization: Bearer` via `StreamOptions.Headers` (avec `APIKey` vide) REMPLACE l'en-tête
  natif du provider (`x-api-key`/`x-goog-api-key`) — utile derrière un reverse proxy à auth
  propre (ex. kern-firewall), sans transmettre de vraie clé provider.
- `Models.Complete` ne retourne jamais d'erreur Go pour un refus provider (401, 500…) :
  l'échec est dans `AssistantMessage.ErrorMessage` avec `StopReason: "error"`.

## Stripe API / webhooks (2026-08, projet kern-billing)
- `Invoice` (API récente) : plus de `subscription` racine ni de `period_end` fiable — le lien
  est sous `parent.subscription_details`, la vraie fin de période est
  `lines.data[0].period.end` (le `period_end` racine = date de création : expiration quasi
  immédiate, en silence). Vérifier la forme réelle via `stripe <resource> list` /
  `stripe trigger` avant d'écrire le parsing, jamais depuis la mémoire d'une doc.
- Compte sur un train d'API plus récent que tout SDK publié : `webhook.ConstructEvent`
  refuse tout (« expects API version X »). `ConstructEventWithOptions` +
  `IgnoreAPIVersionMismatch: true`, sûr seulement si l'événement est lu via des structs
  maison (forme JSON vérifiée), jamais les structs typés du SDK.
- Managed Payments (actif par défaut sur les comptes récents) fait échouer une Checkout
  Session sans `tax_code` produit — `params.AddExtra("managed_payments[enabled]", "false")`
  (pas encore typé dans stripe-go v82.5.1).
- `stripe trigger checkout.session.completed` échoue aussi sur ces comptes : ajouter
  `--override "checkout_session:managed_payments[enabled]=false"` et
  `--remove "checkout_session:payment_intent_data.shipping"`.
- `stripe listen` en arrière-plan meurt silencieusement si un `pkill`/`lsof -ti :port | kill`
  voisin le cible — vérifier `pgrep -fl "stripe listen"` au lieu de le supposer vivant.

## Astro 5 / site statique (2026-07, projet refonte sagefemmevannes)
- npm `allow-scripts` bloque les postinstall (esbuild, sharp) → build KO tant qu'on n'a pas
  `npm approve-scripts esbuild sharp` puis `npm rebuild`. Vérifier après tout install.
- Tailwind v4 : plus de `tailwind.config.js` ; config CSS-first via `@theme` + plugin
  `@tailwindcss/vite` dans `astro.config`. Ne pas générer de config JS.
- E2E d'un site statique = `astro build` + un script Node qui grep le HTML de `dist/`
  (CTA, coordonnées, JSON-LD, slugs attendus) ; testable sans navigateur.
- Scraper un WordPress OVH : le HTTPS peut servir un cert mutualisé (`*.hosting.ovh.net`)
  qui casse WebFetch → `curl http://`.
- Content Collections : schéma Zod dans un fichier à part importé depuis `zod` (PAS
  `astro:content`, non résolvable en Vitest) → testable en unitaire ET réutilisé par
  `content.config.ts`.
- Frontmatter YAML : une valeur contenant « : » doit être quotée (« incomplete explicit
  mapping pair » sinon).

## Vue 3 / Vue Router 4 (2026-08, projet LPB_1.0_Vue)
- i18n par préfixe d'URL : le `<link rel="canonical">` pointe vers SA PROPRE URL localisée,
  jamais vers la langue par défaut — sinon les autres langues sont désindexées comme
  doublons. Invisible en unitaire ; seul un E2E navigateur (DOM après navigation) l'a vu.
- Détection de langue navigateur servant un contenu différent à la MÊME URL : incompatible
  avec hreflang (une URL par langue) — trancher avant d'implémenter l'un des deux.
- Paramètre de route optionnel à regex restreinte (`/:lang(en|fr|pg)?`) : pas de routes
  dupliquées par langue quand la langue par défaut reste non préfixée.

## React 19 / Vite 8 (2026-07, projet PainPinGo)
- `npm create vite@latest <dir> -- --template react-ts` sous npm 11/Windows : `--template`
  ignoré (scaffolde vanilla). Fiable : `npx create-vite@<version> <dir> --template react-ts`,
  puis vérifier le package.json avant `npm install`.
- Template Vite react-ts (2026) active `erasableSyntaxOnly` : interdit paramètres-propriétés
  de constructeur, `enum` non-const, namespaces. Champs déclarés puis assignés ; unions.
- Windows : un outil installé via winget (ex. Go) peut manquer au PATH de la session
  PowerShell de l'agent → préfixer `$env:Path += ";<dossier bin>"`.
