# Mode coder — cadrage documenté → backlog GitHub → GitHub Flow

Variante du greenfield pour un produit à part entière (pas un module isolé) : le temps
investi en phase 1 se rembourse en épargnant des allers-retours de cadrage pendant le
développement. Éprouvé sur Survival AI (2026-08) : les 5 documents ci-dessous en sont
issus, généralisés en templates.

Références dédiées :
- `references/templates-coder/` — un fichier par document de `docs/`, à lire un par un
  au moment de rédiger le document correspondant, pas tous d'un coup.
- `references/mode-coder-execution.md` — protocole d'exécution de la Phase 3
  (superviseur/sous-agents), à lire entièrement dès que la Phase 2 est terminée.

## Phase 1 — Recherche & cadrage documenté

1. Recherche de l'existant (identique au mode viber) : 2-3 références open source ou
   produits à imiter, noter stack et périmètre. Ne jamais recoder ce qui a une API
   officielle ou une lib réutilisable.
2. Cadrage par salves de questions fermées (AskUserQuestion, 3-4 questions par salve,
   une salve par thème, s'arrêter dès qu'un document peut être rédigé sans inventer) :
   - Vision produit & positionnement (à qui, quel problème, quelle direction
     artistique/UX s'il y en a une).
   - Piliers fonctionnels & modules principaux.
   - Stack technique & contraintes de plateforme (cible, hors-ligne/connecté, budget).
   - Découpage du MVP (qu'est-ce qui rentre dans la v1, qu'est-ce qui attend).
3. Rédiger les 5 documents dans `docs/`, un par un, dans l'ordre, en faisant valider
   chaque document avant de passer au suivant (question fermée : valider / ajuster) :
   - `docs/01_concept.md` ← `references/templates-coder/01-concept.md`
   - `docs/02_architecture_ui.md` ← `references/templates-coder/02-architecture-ui.md`
   - `docs/03_implementation_plan.md` ← `references/templates-coder/03-implementation-plan.md`
   - `docs/04_catalogue_items.md` ← `references/templates-coder/04-catalogue-items.md`
   - `docs/05_github_backlog.md` ← `references/templates-coder/05-github-backlog.md`
4. Créer `docs/README.md` qui indexe les 5 documents (résumé d'une ligne chacun).

## Phase 2 — Backlog GitHub (Epics + Issues)

1. Depuis `docs/05_github_backlog.md` : créer un label par tag d'Epic s'il n'existe pas
   (`gh label create`), puis un milestone GitHub par Epic (`gh api repos/:owner/:repo/milestones -f title=...`).
2. Créer une issue de suivi (tracking issue) par Epic sur son milestone, avec la liste
   des User Stories en checklist. Créer une issue par User Story rattachée au même
   milestone, description = le format « En tant que / je veux / afin de » + critères
   d'acceptation copiés tels quels du document.
3. **Confirmer avec l'utilisateur avant de pousser quoi que ce soit sur GitHub** (labels,
   milestones, issues sont visibles par toute l'équipe) : présenter le plan de création,
   attendre validation, puis exécuter.

## Phase 3 — Exécution des issues (GitHub Flow, TDD, superviseur/sous-agents)

Le TDD est identique au mode viber (phase 3) ; ce qui change est le modèle de branche
(GitHub Flow, PR par issue) **et** le mode d'exécution : dès que plusieurs issues sont
non bloquées en même temps, le thread principal devient un superviseur qui délègue
chaque issue à un sous-agent dédié plutôt que de les dérouler une par une.

Déroulé complet (calcul du lot, délégation, worktrees, critères de fusion) :
`references/mode-coder-execution.md` — à lire entièrement avant la première issue de
la Phase 3.

## Phase 4 — Clôture

1. Rétro finale dans `retro.md`.
2. Fermer chaque milestone GitHub une fois toutes ses issues closes.
3. Tag de version éventuel sur `main`.
4. Reporter les nouveaux pièges génériques dans `references/pieges.md` du skill parent.

## Évolution

- Les 5 templates de documents → `references/templates-coder/*.md` (append-only par
  variante si un domaine a besoin d'une section en plus ; ne pas réécrire l'existant).
- Le protocole d'exécution (calcul des lots, prompts des sous-agents, worktrees) →
  `references/mode-coder-execution.md` ; c'est ce fichier qui évolue si le mode de
  délégation change, pas celui-ci.
- Ce fichier ne bouge que si le déroulé du mode coder change (nouvelle phase, nouvel
  ordre) — pas pour un ajustement de formulation de question.
