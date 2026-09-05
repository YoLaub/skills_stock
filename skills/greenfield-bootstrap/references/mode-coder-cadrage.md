# Mode coder — cadrage documenté → backlog GitHub

Variante du greenfield pour un produit à part entière (pas un module isolé) : le temps
investi en Phase 1 se rembourse en épargnant des allers-retours de cadrage pendant le
développement. Éprouvé sur Survival AI (2026-08) : les 5 documents ci-dessous en sont
issus, généralisés en templates.

Ce fichier couvre le **cadrage + le backlog** (Phases 1-2). L'exécution des issues
(Phase 3) et la clôture (Phase 4) sont dans le skill `tdd-backlog-run`.

Références dédiées :
- `references/templates-coder/` — un fichier par document de `docs/`, à lire un par un
  au moment de rédiger le document correspondant, pas tous d'un coup.

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

Prérequis : le bootstrap du dépôt (Phase 2 du `SKILL.md` — `git init -b main` avec
premier commit avant toute autre branche, `CLAUDE.md`, `docs/index/` OKF, `retro.md`,
dépôt GitHub distant créé). Sans ce bootstrap, les commandes `gh` ci-dessous n'ont pas de
dépôt sur lequel créer labels/milestones/issues, et `tdd-backlog-run` n'a pas de
`CLAUDE.md` de projet à donner aux sous-agents.

Sur un projet repris (le code existe mais pas de plan), le bootstrap est déjà fait : ne
pas le rejouer. Vérifier seulement que `CLAUDE.md`, `docs/index/` et le dépôt distant
existent, et créer uniquement ce qui manque.

1. Depuis `docs/05_github_backlog.md` : créer un label par tag d'Epic s'il n'existe pas
   (`gh label create`), puis un milestone GitHub par Epic
   (`gh api repos/:owner/:repo/milestones -f title=...`).
2. Créer une issue de suivi (tracking issue) par Epic sur son milestone, avec la liste
   des User Stories en checklist. Créer une issue par User Story rattachée au même
   milestone, description = le format « En tant que / je veux / afin de » + critères
   d'acceptation copiés tels quels du document. Le champ **Dépend de** devient une ligne
   `Depends on #<numéro>` dans le corps de l'issue.
3. **Confirmer avec l'utilisateur avant de pousser quoi que ce soit sur GitHub** (labels,
   milestones, issues sont visibles par toute l'équipe) : présenter le plan de création,
   attendre validation, puis exécuter.

## Fin — Hand-off

Backlog créé → l'exécution des issues (GitHub Flow, TDD, superviseur/sous-agents) et la
clôture des milestones se font dans **`tdd-backlog-run`**.

## Évolution

- Les 5 templates de documents → `references/templates-coder/*.md` (append-only par
  variante ; ne pas réécrire l'existant).
- Ce fichier ne bouge que si le déroulé du cadrage change (nouvelle phase, nouvel
  ordre) — pas pour un ajustement de formulation de question.
