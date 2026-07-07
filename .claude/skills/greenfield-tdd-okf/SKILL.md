---
name: greenfield-tdd-okf
description: Workflow répétable pour construire un produit greenfield en TDD avec index OKF — recherche de l'existant, cadrage par questions, plan validé, bootstrap monorepo git-flow, features en branches avec tests verts + E2E avant merge, index OKF par feature, rétro continue. Utiliser au démarrage d'un nouveau projet applicatif ou d'un gros module.
---

# Greenfield TDD + OKF

Workflow éprouvé sur CRM_TEAM (2026-07). Objectif : livrer vite sans dette, avec un
contexte relisible en quelques fichiers.

## Phase 1 — Recherche & cadrage (avant TOUTE ligne de code)
1. Chercher l'existant open source à imiter (web) : 2-3 références, noter stack et périmètre.
2. **Ne jamais scraper/recoder ce qui a une API officielle ou une lib réutilisable** (licence permissive → l'utiliser telle quelle).
3. Poser 3-4 questions de cadrage fermées (AskUserQuestion) : modèle à imiter, stack,
   contraintes structurantes du domaine (ex. multi-entité), options payantes.
4. Écrire le plan (contexte, décisions validées, architecture, modèle de données, étapes
   parallélisables, vérification E2E) et le faire valider.

## Phase 2 — Bootstrap (une branche `feature/bootstrap`)
- `git init -b main` → branche `dev` → une branche par feature. Merge `--no-ff` vers dev
  UNIQUEMENT si tests verts + E2E fait. Jamais de commit direct sur main/dev.
- Monorepo : workspaces dès le départ si un package est partagé (sinon la résolution
  bundler casse) ; docker-compose pour la base ; `.env.example` complet.
- **Lire les docs embarquées des frameworks récents** (ex. `node_modules/next/dist/docs`)
  au lieu de supposer : les conventions changent (proxy.ts vs middleware.ts…).
- CLAUDE.md : conventions, commandes, règles métier clés.
- Créer `docs/index/` (OKF) + `retro.md` immédiatement.

## Phase 3 — Chaque feature (branche dédiée, TDD)
1. Tests d'abord sur la **logique pure** (calculs, machines d'états, dédoublonnage,
   signatures) placée dans `services/` ; UI/routes = orchestration mince.
2. Toute logique est un service unique consommé par l'UI ET par les interfaces machine
   (tools MCP, API) — jamais de duplication.
3. Suite verte → build → **E2E réel** (curl sur l'API/MCP, vrai appel externe si gratuit).
4. Fiche OKF `docs/index/<feature>.md` : entête YAML (id, feature, branch, status, files,
   tests, decisions) + corps ≤ 15 lignes (quoi, pièges). Dater les décisions.
5. Ajouter les pièges rencontrés à `retro.md` AU MOMENT où ils mordent.
6. Commit conventionnel, merge --no-ff vers dev.

## Phase 4 — Clôture
- Rétro finale dans `retro.md`, merge dev → main (jalon stable), tag éventuel.
- Mettre à jour ce skill avec les nouveaux pièges.

## Pièges connus (2026-07, stack Next 16 / Prisma 7 / Python)
- npm workspaces + `exports` + `turbopack.root` pour un package TS partagé.
- Prisma 7 : generator `prisma-client`, prisma.config.ts + dotenv, driver adapter requis.
- jose/crypto sous vitest jsdom → `// @vitest-environment node` sur les tests de services.
- pydantic→zod : `by_alias=True, exclude_none=True` (zod `.optional()` refuse null).
- tsx/seeds : `import "dotenv/config"` obligatoire.
- Webhooks inter-services : HMAC-SHA256 hex + comparaison timing-safe, contrat zod partagé.
- Numérotation légale : transaction + contrainte unique (memberId, year, seq).
- Scrapling : navigateurs via l'exe `scrapling install`, pas `python -m scrapling` ; le
  Playwright ainsi installé est réutilisable pour du rendu PDF (ne pas réembarquer Chromium).
- Rendre en headless une page protégée : jeton court (JWT) lié au chemin, autorisé dans le proxy.
- Next : `new Response(new Uint8Array(buffer))` — BodyInit n'accepte pas Buffer directement.
- Intl fr-FR : séparateurs = espaces insécables ; comparer via le formateur, pas une chaîne écrite.
- Feature qui a besoin d'un secret/SMTP externe : prévoir un mode simulé (jsonTransport) pour
  que l'app tourne sans config ; le vrai transport s'active si la variable d'env est présente.
- Drag & drop : HTML5 dataTransfer + useOptimistic + server action typée, zéro dépendance.
