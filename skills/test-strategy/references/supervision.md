# Supervision — délégation par unité isolée (ActivCreew)

À dérouler à l'étape 2 (router et générer) **quand le périmètre contient au moins 2
unités indépendantes**. Une seule unité → la générer directement, le coût de délégation
ne se justifie pas.

**Unité, pour `test-strategy`** : un fichier de test (RED ou GREEN) par domaine ou par
groupe de Scenarios d'un même `.feature`. Deux unités sont indépendantes si elles ne
ciblent pas le même fichier de test ni les mêmes fixtures.

Adapté de `tdd-backlog-run` (`references/execution.md`), au modèle de branches imposé
`git-workflow-chantier` et à la stack ActivCreew.

## 1. Le superviseur ne code pas

Dès qu'il y a plus d'une unité non bloquée, le thread principal devient superviseur :
il découpe (par Scenario / domaine), délègue, contrôle, agrège — il n'écrit lui-même
aucun fichier de test d'unité. Raison : sinon il accumule dans son contexte les logs
d'exécution de toutes les unités à la suite, et sature.

Le lot = toutes les unités non bloquées à cet instant (les unités de test sont presque
toujours toutes non bloquées entre elles).

## 2. Isoler chaque unité (worktree dédié)

```bash
git worktree add ../full-project-<slug> -b test/<slug> <base>
```

- `<base>` = **la branche principale du chantier** (`feat/<chantier>`), jamais `main`,
  jamais `dev` (`git-workflow-chantier` §1).
- Un worktree par unité parallèle : deux sous-agents dans le même arbre = checkout
  conflictuel + fichiers de build partagés.

**Point d'agrégation partagé** (`tests/test-map.json`, `config/permissions.json` pour une
nouvelle route à couvrir, un helper d'auth E2E) : pas un motif de sérialisation.
Paralléliser — le conflit au merge est un append-vs-append trivial. Consigne à chaque
sous-agent : n'ajouter qu'UNE entrée par fichier partagé, logger le conflit attendu.

## 3. Déléguer un sous-agent frais par unité

Un sous-agent **général** (pas un fork). Prompt autonome :

- Chemin du worktree = répertoire de travail.
- Les Scenarios / Examples de l'unité **copiés verbatim** depuis le `.feature`, + les
  règles métier numérotées concernées. Ne pas résumer : les critères doivent rester
  vérifiables mécaniquement.
- **Mode RED ou GREEN** de l'unité (cf. étape 1 du SKILL.md) et ce que ça impose.
- Chemin de `CLAUDE.md` du repo.
- Chemins des `references/` à lire : `gherkin-mapping.md` (niveau + emplacement),
  `unit-testing-patterns.md` (génération unitaire) ou `e2e-patterns.md` (génération E2E)
  selon le niveau de l'unité.
- Mémoires qui mordent ici : `test_fixtures_architecture` (⚠️ `draftAndPublish` → créer
  via API HTTP, pas SQL), `feedback_docker_service_names` (`postgres-test`,
  `redis-test`), `feedback_tdd_plan_wins`.
- Consigne : nommage `should_<résultat>_when_<condition>`, structure AAA, entités HTML
  d'accents en TSX / accents natifs en strings JS (`french-accents`). Écrire le fichier
  au bon endroit (table de l'étape 2). Ne toucher qu'à son fichier de test + fixtures.
- **Ne jamais merger soi-même** : exécuter le test, confirmer le résultat attendu selon
  le mode, rendre la main avec un rapport court (fichier créé, niveau, RED confirmé /
  GREEN, ou blocage).

## 4. Contrôle de conformité avant de déclarer l'unité "faite"

Lancer un **2e** sous-agent frais (général — **jamais** celui qui a généré le test).
Entrée seulement : les Scenarios / Examples verbatim + le diff de l'unité
(`git diff <base>...<branche>`).

Consigne : pour chaque Scenario et chaque ligne d'Examples, dire s'il existe un test qui
le couvre et qui **assert le bon comportement métier** (pas juste un `expect(true)`), et
si l'exécution donne bien le résultat attendu par le mode :

- **RED** : le test échoue sur une **assertion métier**, pas sur une erreur d'import / de
  setup / de fixture. Rejouer :
  ```bash
  git worktree add ../full-project-verify-<slug> --detach <branche>
  cd "Strapi v5" && yarn test <chemin>        # ou pnpm exec playwright test <spec>
  ```
  Vérifier que le message d'échec est bien une différence de valeur attendue, pas un
  `ReferenceError` / `Cannot find module`.
- **GREEN** : le test passe.

Scenario non couvert, ou RED qui échoue pour une mauvaise raison → **blocage** (§6). Une
relance ciblée du générateur, sinon escalade.

## 5. Gate RED/GREEN — bloquant, non négociable

- **RED** : une unité n'est livrable que si tous ses tests échouent **pour la bonne
  raison** (assertion métier), listés explicitement, code de prod **intact**. On ne
  "retire jamais du scope" un test qui ne compile pas — on corrige le test jusqu'à ce
  qu'il échoue proprement sur le comportement.
- **GREEN** : tous les tests de l'unité passent ; si l'un échoue, c'est le CODE qui est
  faux (on le corrige, on ne touche pas au test).
- Pas de hand-off vers `dev-strategy` tant qu'une unité RED n'a pas son échec confirmé
  et documenté.

## 6. Agréger — sans merger vers dev

1. Attendre la fin de chaque sous-agent (résultat confirmé) ou son blocage.
2. Contrôle de conformité par unité (§4).
3. Ramener chaque branche `test/<slug>` sur la branche principale du chantier par MR
   (`glab mr create --target-branch feat/<chantier>`), une à la fois, **confirmation de
   l'utilisateur avant chaque merge**.
4. `git worktree remove ../full-project-<slug>`.
5. **Ne jamais merger vers `dev` de sa propre initiative** (builds Coolify —
   `git-workflow-chantier` §3). Le skill s'arrête après avoir tout ramené sur la branche
   principale + rapport de fin de chantier.
6. Blocage : le superviseur décide — corriger le prompt et relancer **une** fois, ou
   escalader. Les autres unités continuent.

## 7. Relancer

Lot mergé → s'il reste des Scenarios non traités, recalculer le lot et répéter, sinon
→ résumé de fin de chantier du SKILL.md.
