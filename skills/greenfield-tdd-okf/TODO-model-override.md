# À trancher — override de modèle dans greenfield-tdd-okf

Note de travail, pas une référence active du skill (rien ici n'est lu pendant
l'exécution). Sert à reprendre la réflexion si on décide d'ajouter des
`model:` overrides comme ça a été fait ailleurs dans le dépôt
(`candidate-screener`, `rh-needs-analyst`, `gap-analyser` → `opus` en
frontmatter ; porte de contrôle de `presentation-builder` et juge de
`skill-bench` → `opus` sur le dispatch). Pas encore fait ici, volontairement —
la situation est différente, détaillée ci-dessous.

## Pourquoi ce n'est pas un ajout direct comme les autres

Les overrides déjà posés visaient tous un **rôle de juge/classification fixe**
porté par un fichier agent dédié ou un point de dispatch unique et toujours
identique. `greenfield-tdd-okf` n'a ni l'un ni l'autre :

- **Mode viber** (phases 1-4) : tout tourne dans la session principale, pas de
  sous-agent dispatché. Aucun point d'ancrage pour un `model:` — le modèle de
  la session est le choix de l'utilisateur, pas un réglage du skill.
- **Mode coder, Phase 3** (`references/mode-coder-execution.md`) : dispatche
  un sous-agent par issue, mais ce sont des **exécutants** (TDD, build, E2E),
  pas des juges contre un rubric fixe. Le bon modèle dépend de la nature de
  l'issue traitée, pas du rôle — ça ne se fige pas une fois pour toutes en
  frontmatter comme pour un agent dédié.

## Deux pistes si on y revient

### 1. Tiering par complexité d'issue (Phase 3 du mode coder)

Dans `mode-coder-execution.md`, section "3. Déléguer un sous-agent par
issue" : le superviseur pourrait choisir `model: opus` pour les issues
fondatrices/architecturales (celles dont dépendent beaucoup d'autres, ou qui
posent un choix structurant non trivial) et laisser le modèle par défaut pour
les issues routinières (CRUD, ajustements UI). Ça suppose d'ajouter un
critère de classification en Phase 1 du protocole d'exécution (à côté du
calcul du lot non bloqué) — pas juste une ligne de frontmatter, un vrai choix
à documenter : qui décide qu'une issue est "fondatrice", sur quel signal
(nombre d'issues qui en dépendent via `Depends on`, mention explicite dans le
backlog `docs/05_github_backlog.md`, ou jugement du superviseur au cas par
cas).

### 2. Ajouter une porte de contrôle avant merge (si elle voit le jour)

`greenfield-tdd-okf` n'a aujourd'hui **aucun équivalent** de la porte de
contrôle de `presentation-builder` ou du juge de `skill-bench` — la Phase 3
(séquentielle ou superviseur/sous-agents) enchaîne suite verte → build → E2E
→ merge, sans relecture dédiée par un sous-agent frais distinct de celui qui
a écrit le code. Si une telle porte était ajoutée un jour (relecture avant
`--no-ff` ou avant merge de PR), elle serait la candidate naturelle pour
`model: opus`, par le même raisonnement que les autres juges du dépôt : un
relecteur plus faible que l'auteur du code a des angles morts. Mais c'est un
ajout de phase, pas juste un override — à traiter comme une évolution de
méthodologie (donc dans `SKILL.md`/`mode-coder.md`, pas seulement ce fichier)
si l'idée est retenue.

## Ce qui ne bouge pas sans décision explicite

Ne pas ajouter de `model:` à la légère dans `mode-coder-execution.md` sans
trancher la piste 1 ci-dessus — un override uniforme sur tous les sous-agents
d'issue coûterait cher sans bénéfice net sur les issues routinières, qui sont
la majorité dans un backlog typique.
