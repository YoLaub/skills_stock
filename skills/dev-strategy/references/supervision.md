# Supervision — délégation par unité isolée (ActivCreew)

À dérouler à l'étape 4 **quand le périmètre contient au moins 2 unités indépendantes**.
Une seule unité → l'implémenter directement, le coût de délégation ne se justifie pas.

**Unité, pour `dev-strategy`** : une tranche couche × domaine telle que listée dans
`cartographie-conventions.md` (schema + service pur / routes + controller / lifecycles +
permissions / frontend d'un domaine). Deux unités sont indépendantes si elles ne
partagent pas de fichier de logique.

Adapté de `greenfield-tdd-okf` (`mode-coder-execution.md`), au modèle de branches imposé
`git-workflow-chantier` et à la stack ActivCreew.

## 1. Le superviseur ne code pas

Dès qu'il y a plus d'une unité non bloquée, le thread principal devient superviseur :
il découpe, délègue, contrôle, agrège — il n'écrit lui-même aucune ligne de code d'unité.
Raison : sinon il accumule dans son contexte les logs de test, diffs et allers-retours
de build de toutes les unités à la suite, et sature.

Une unité est **non bloquée** si aucune autre unité du lot ne doit être finie avant elle
(pas de dépendance de logique). Le lot = toutes les unités non bloquées à cet instant.

## 2. Isoler chaque unité (worktree dédié)

Pour chaque unité du lot, avant de lancer le sous-agent :

```bash
git worktree add ../full-project-<slug> -b <type>/<slug> <base>
```

- `<base>` = **la branche principale du chantier** (`feat/<chantier>`), jamais `main`,
  jamais `dev` (`git-workflow-chantier` §1). Les sous-branches y reviendront par MR.
- `<type>` ∈ `feat|fix|chore|perf`. Pas de numéro de ticket en préfixe.
- Un worktree par unité parallèle : deux sous-agents dans le même arbre = checkout
  conflictuel + fichiers de build partagés.
- Ports dev : `dev-worktree.sh` à la racine gère l'attribution (Strapi 1437, apps
  3100-3107) si un worktree doit lancer l'app.

**Point d'agrégation partagé** (`config/permissions.json`, un barrel `index.ts`,
`retro.md`) : pas un motif de sérialisation. Paralléliser quand même — le conflit au
merge est un append-vs-append trivial (garder les deux côtés). Consigne à chaque
sous-agent : n'ajouter qu'UNE entrée par fichier partagé, et logger le conflit attendu
dans son rapport.

Si deux unités touchent en réalité la même logique dans les mêmes fichiers (le découpage
s'est trompé) : ne pas les paralléliser, les repasser en séquentiel.

## 3. Déléguer un sous-agent frais par unité

Un sous-agent **général** (pas un fork — chaque unité est un contexte propre, rien à
hériter). Prompt autonome, il démarre sans mémoire de cette conversation :

- Chemin du worktree = répertoire de travail.
- Énoncé de l'unité + **critères copiés verbatim** : les tests RED ciblés (chemins +
  contenu), les règles métier numérotées concernées (CA-XXX…). Ne pas résumer.
- Chemin de `CLAUDE.md` du repo (conventions, commandes, règles Strapi v5 / Next.js).
- Chemins des `references/` du skill à lire et lesquelles :
  `cartographie-conventions.md` (couches + règles non négociables),
  `patterns-activcreew.md` (patterns de code), `principes-solid-dry.md`.
- Rappel des mémoires qui mordent ici : `feedback_tdd_plan_wins` (le test gagne sur le
  code), `test_fixtures_architecture` (⚠️ `draftAndPublish` → créer via API HTTP, pas
  SQL), `feedback_docker_service_names` (`postgres-test`, `redis-test`).
- Consigne : appliquer les skills de domaine (`strapi-routes`, `nextjs-component`,
  `french-accents`…), SOLID + DRY (chercher avant de créer), ne toucher qu'aux fichiers
  de son unité, déclarer les nouvelles routes dans `permissions.json`.
- **Ne jamais merger soi-même** : s'arrêter quand la suite de l'unité est verte + build,
  rendre la main au superviseur avec un rapport court (unité traitée, tests verts,
  blocage éventuel).

## 4. Contrôle de conformité avant de déclarer l'unité "faite"

Ne pas sauter, même si la suite du sous-agent est verte : des tests verts prouvent que le
code écrit tourne, pas qu'il couvre tout ce que l'unité demandait.

Lancer un **2e** sous-agent frais (général, contexte propre — **jamais** le codeur ni un
fork de lui : il faut un regard sans biais de confirmation). Entrée seulement :

- les critères de l'unité copiés verbatim (tests RED ciblés, règles métier),
- le diff de l'unité (`git diff <base>...<branche>`).

Consigne : pour chaque critère, dire s'il est couvert par **du code ET un test** /
partiel / absent — verdict par critère, sans reformuler ni commenter le style. Lui donner
un worktree détaché et lui demander de **rejouer la suite** en plus de lire le diff :

```bash
git worktree add ../full-project-verify-<slug> --detach <branche>
cd "Strapi v5" && ./scripts/run-affected-tests.sh      # backend
cd frontend && pnpm --filter <package> test            # front (jest/vitest selon package)
pnpm exec playwright test <spec>                        # E2E
```

Un e2e ou un test de non-régression ne se voit pas dans un diff.

- Critère absent ou partiel → **blocage** (voir §6). Une relance ciblée du codeur (liste
  des critères manquants), sinon escalade à l'utilisateur.
- Si le sous-agent de conformité meurt pour une raison d'environnement (veille, watchdog) :
  le relancer une fois, puis faire le contrôle inline soi-même.

## 5. Gate RED/GREEN — bloquant, non négociable

- `dev-strategy` : une unité n'est livrable que si **tous ses tests sont GREEN**,
  `yarn tsc --noEmit` (Strapi) et `pnpm build` (frontend) passent à 0 erreur, et l'E2E
  réel a été fait (curl API / Playwright). Un test qui échoue = le CODE est faux, jamais
  le test, jamais "retirer du scope".
- Pas de hand-off vers `ux-ui-strategy` tant qu'une seule unité du périmètre n'a pas
  passé ce gate.

## 6. Agréger — sans merger vers dev

1. Attendre que chaque sous-agent du lot ait fini (suite verte) ou remonté un blocage.
2. Contrôle de conformité par unité (§4).
3. Ramener chaque branche d'unité sur la branche principale du chantier par MR
   (`glab mr create --target-branch feat/<chantier>`), une à la fois, **avec
   confirmation de l'utilisateur avant chaque merge** (action visible par l'équipe).
4. Supprimer le worktree traité : `git worktree remove ../full-project-<slug>`.
5. **Ne jamais merger vers `dev` de sa propre initiative** — chaque merge dev déclenche
   des builds Coolify. La bascule `feat/<chantier> → dev` est décidée par Clément
   (`git-workflow-chantier` §3). Le skill s'arrête après avoir tout ramené sur la
   branche principale + hand-off.
6. Blocage (tests rouges persistants, critères ambigus, conformité invalidée) : le
   superviseur décide — corriger le prompt et relancer **une** fois, ou escalader. Les
   autres unités du lot continuent, non affectées.

## 7. Relancer

Lot mergé sur la branche principale → recalculer les unités nouvellement non bloquées
(§1) et répéter jusqu'à ce que le périmètre soit épuisé → étape 5 du SKILL.md
(validation GREEN globale).
