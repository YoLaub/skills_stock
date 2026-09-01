# Reprise d'un projet existant (brownfield)

Chemin à suivre quand la Phase 0 du `SKILL.md` a détecté du code préexistant. Objectif :
retrouver l'état réel du projet et repartir du bon endroit du workflow, sans réécrire ce
qui existe ni supposer une architecture.

## Étape 1 — Cartographier avant de décider

Lancer le skill `archi-scanner` sur le dépôt (Skill tool, `archi-scanner`). Il produit
`archi-output/INDEX.md` (référence complète) et `archi-output/PROJECT_MEMORY.md` (résumé).

Si `archi-output/INDEX.md` existe déjà, ne pas rescanner à l'aveugle : le lire, vérifier
sa date face à `git log -1 --format=%cd`, et ne relancer le scanner que si le code a
bougé depuis.

**Ne rien écrire d'autre tant que le scan n'est pas terminé.** Ni bootstrap, ni fiche
OKF, ni test — tout choix pris avant le scan est un choix pris à l'aveugle.

## Étape 2 — Inventaire des acquis du workflow

Le scanner dit ce que le code contient ; cette étape dit ce qui manque au workflow.
Vérifier la présence de chacun de ces artefacts et noter son état :

| Artefact | Vérification |
|---|---|
| Historique git | `git log --oneline -5` (dépôt initialisé ? commits réels ?) |
| Branche `dev` | `git branch -a` (modèle de branche en place ?) |
| Suite de tests | framework détecté par le scanner + `<runner> --version`, puis exécution |
| `CLAUDE.md` | présent, et à jour du stack détecté ? |
| `docs/index/` (OKF) | présent ? combien de fiches vs combien de modules à l'index ? |
| `retro.md` | présent ? |
| `docs/01_concept.md` … `05_github_backlog.md` | cadrage mode coder déjà fait ? |
| Backlog GitHub | `gh issue list`, `gh api repos/:owner/:repo/milestones` |

**Faire tourner la suite de tests avant toute chose.** Une suite rouge à l'arrivée est
l'état de départ, pas une régression à imputer au travail à venir : le noter
explicitement à l'utilisateur avant d'écrire une ligne.

## Étape 3 — Restituer et choisir la suite avec l'utilisateur

Présenter en une dizaine de lignes maximum : stack, périmètre couvert, état des tests,
artefacts du workflow manquants. Puis poser une question fermée (AskUserQuestion) sur la
suite :

- **Continuer une feature en cours** → aller directement à la Phase 3 du `SKILL.md`
  (TDD sur branche dédiée), en s'appuyant sur `archi-output/INDEX.md` au lieu de
  redécouvrir le code.
- **Ajouter une nouvelle feature** → Phase 1 réduite : pas de recherche de modèle open
  source (le modèle, c'est le code existant), seulement les questions de cadrage propres
  à la feature, puis Phase 3.
- **Reprendre le cadrage produit du mode coder** (le projet a du code mais pas de plan)
  → `references/mode-coder.md`, Phase 1, en rédigeant les documents **à partir de
  l'existant scanné** et non d'une vision inventée.

Le choix du mode viber/coder de la Phase 0 reste valable et s'applique à la suite.

## Étape 4 — Combler les manques, sans big bang

Les artefacts manquants repérés à l'étape 2 se rattrapent au fil de l'eau, pas dans un
commit de reprise géant :

- `CLAUDE.md`, `retro.md`, `docs/index/` absents → les créer maintenant, en un commit
  dédié, à partir de `archi-output/PROJECT_MEMORY.md`.
- Fiches OKF manquantes → **ne pas documenter rétroactivement tout le code**. Une fiche
  s'écrit quand on touche au module correspondant, pas avant.
- Pas de branche `dev` ni de modèle de branche → proposer de l'aligner sur la Phase 2 du
  `SKILL.md`, mais laisser l'utilisateur trancher : sur un dépôt partagé, changer le
  modèle de branche impacte d'autres personnes.
- Pas de tests → écrire les tests de la feature en cours (TDD normal), et seulement des
  tests de caractérisation sur le code existant que cette feature modifie.

## Règles propres au brownfield

- **Les conventions du dépôt priment sur celles du skill.** Nommage, structure de
  dossiers, style de commit : suivre ce que le scan a relevé, même si le skill
  recommande autre chose. Signaler l'écart à l'utilisateur, ne pas le corriger d'office.
- Ne jamais reformater, renommer ou déplacer du code existant hors du périmètre demandé.
- Les pièges du code existant vont dans `retro.md` avec la mention « préexistant », pour
  ne pas les confondre avec ceux introduits pendant la reprise.
