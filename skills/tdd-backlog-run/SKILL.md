---
name: tdd-backlog-run
description: >
  Dérouler un lot d'issues / un milestone GitHub en TDD via un superviseur qui délègue
  chaque issue à un sous-agent frais (worktree dédié, TDD red-green, PR), avec une porte
  de conformité par un 2e sous-agent avant chaque merge. Invocable à froid. Utiliser pour
  « déroule le backlog », « implémente le milestone », « continue les issues de l'epic »,
  « exécute la Phase 3 du mode coder ». Troisième maillon du trio greenfield :
  greenfield-bootstrap (backlog) → tdd-backlog-run (exécution + clôture). Pour une seule
  feature isolée, utiliser plutôt tdd-feature-okf.
---

# TDD Backlog Run

Exécution supervisée d'un backlog d'issues. Le thread principal ne code jamais une issue
dès qu'il y en a plus d'une non bloquée : il devient superviseur et délègue.

Références (à lire au moment indiqué, pas avant) :
- `references/execution.md` — protocole complet (calcul du lot, worktrees, prompts des
  sous-agents, porte de conformité, merges, relance). À lire entièrement avant la
  première issue.
- `references/pieges.md` — pièges connus par stack (**copie partagée dans les 3 skills du
  trio** ; enrichir en clôture).
- `references/orientation.md` — se réorienter dans un projet en cours (**copie partagée
  avec tdd-feature-okf**). À lire seulement si la Phase 0 en a besoin.

## Phase 0 — Terrain

```bash
git log --oneline -1
gh issue list --limit 5
```

- **Pas de dépôt, ou pas de `docs/05_github_backlog.md` ni de milestone GitHub** → il n'y
  a rien à dérouler : `greenfield-bootstrap` mode coder d'abord (cadrage + création du
  backlog).
- **Contexte redémarré, état du projet flou** → dérouler `references/orientation.md`
  (archi-scanner, lire `docs/index/*` + `retro.md`, faire tourner la suite de tests),
  PUIS Phase 1.
- **Backlog en place, tu sais quel milestone dérouler** → Phase 1.

## Phase 1 — Exécution supervisée

Dérouler `references/execution.md` :
1. Calculer le lot d'issues **non bloquées** (`Depends on #<n>` toutes fermées).
2. Lot d'une seule issue → la traiter directement en TDD (pas de délégation).
3. Lot ≥ 2 → un worktree + un sous-agent frais (général, pas un fork) par issue, prompt
   autonome avec critères d'acceptation copiés verbatim.
4. Chaque PR : CI verte, puis **porte de conformité** — un 2e sous-agent frais (jamais le
   codeur) vérifie chaque critère = code + test et rejoue la suite dans un worktree
   détaché.
5. **Confirmation de l'utilisateur avant chaque merge**, un merge à la fois.
6. Lot mergé → recalculer les issues nouvellement non bloquées, répéter.

## Phase 2 — Clôture

1. Rétro finale dans `retro.md`.
2. Fermer chaque milestone GitHub une fois toutes ses issues closes.
3. Tag de version éventuel sur `main`.
4. Reporter les nouveaux pièges génériques dans `references/pieges.md` (**répliquer dans
   les 3 skills du trio**).

## Évolution

- Le protocole d'exécution (calcul des lots, prompts des sous-agents, worktrees, porte de
  conformité) → `references/execution.md` : c'est ce fichier qui évolue si le mode de
  délégation change.
- Nouveau piège → `references/pieges.md` (répliquer dans les 3 skills du trio).
- Ne modifier ce SKILL.md que si les phases elles-mêmes changent.
- Note de travail non tranchée sur un éventuel `model:` override : `TODO-model-override.md`.
