---
name: init-projet
description: >
  Initialise un nouveau projet en rédigeant d'abord son CLAUDE.md via une série de
  questions fermées (QCM), afin de capturer le contexte une bonne fois pour toutes et
  d'optimiser les sessions suivantes. Amorce ensuite le BRAIN du projet
  (`~/brain/<projet>/`) et le bloc de journalisation des erreurs.
  Intentions déclenchantes : "init projet", "initialise le projet", "nouveau projet",
  "démarre le projet", "crée le CLAUDE.md", "bootstrap le projet".
  Ne pas confondre avec compile-rules, qui compile ce journal en règles une fois rempli.
---

# Init Projet — Cadrage par questions fermées → CLAUDE.md

## Principe
Le CLAUDE.md est le contrat de session : tout ce qui y est écrit n'aura plus jamais à
être demandé à l'utilisateur. Ce skill commence donc **toujours** par la rédaction (ou
la mise à jour) du CLAUDE.md, et ne génère **aucun code** tant que le CLAUDE.md n'est
pas validé par l'utilisateur.

Ce fichier a deux couches d'autorité, à ne jamais confondre :
le **Contrat** est contraignant et stable, la **Méthode** est indicative et adaptable.

---

## Contrat (v1) — contraignant

Ces clauses tiennent quel que soit le modèle qui exécute ce skill, et quel que soit le
projet. Chacune est vérifiable par observation de l'exécution.

- **C1 — Aucun code avant validation.** Aucun fichier de code, de configuration ou de
  dépendances n'est créé ni modifié avant que l'utilisateur ait validé explicitement le
  CLAUDE.md. Seul le CLAUDE.md lui-même échappe à cette clause.
- **C2 — Jamais inventer.** Tout fait non tranché est écrit `_à décider_`, jamais rempli
  d'une valeur plausible. Cela inclut le `PROJECT_KEY`, qui est confirmé en question
  fermée et jamais déduit silencieusement.
- **C3 — Questions fermées uniquement.** Toute question passe par `AskUserQuestion`, en
  oui/non ou 2 à 4 options. Exception unique : un fait brut impossible à deviner (nom,
  adresse, téléphone).
- **C4 — Option recommandée en premier.** Chaque question fermée ouvre sur une option
  marquée « (Recommandé) », avec sa raison en description, pour que tout soit validable
  en un clic.
- **C5 — Rien de déductible n'est demandé.** La reconnaissance de l'existant (racine du
  repo, CLAUDE.md ou exemple fourni, `docs/index/`, `.claude/`, git, conversation en
  cours) précède la première question, et tout ce qu'elle établit ne fait pas l'objet
  d'une question.
- **C6 — Mode de collaboration intouchable.** Le bloc est recopié mot pour mot depuis
  [references/bonnes-pratiques-claude-md.md](references/bonnes-pratiques-claude-md.md) :
  aucun résumé, aucune reformulation, aucune question sur son contenu. S'il figure déjà
  dans `~/.claude/CLAUDE.md`, il n'est pas dupliqué dans le projet.
- **C7 — Écriture en APPEND.** Aucun contenu préexistant d'un CLAUDE.md n'est modifié ni
  supprimé, aucun bloc déjà présent n'est dupliqué. Un bloc existant est signalé et passé.
- **C8 — Le BRAIN vient après.** L'amorçage `~/brain/` et le bloc de journalisation ne
  démarrent qu'après validation du CLAUDE.md par l'utilisateur.
- **C9 — Le bloc de routage reste dormant.** « Règles projet » est écrit dans
  `PENDING-rules-block.md` et jamais appendé au CLAUDE.md par ce skill : c'est
  `compile-rules` qui le bascule, après sa première passe réussie.
- **C10 — Sortie fermée et rapportée.** Les seuls artefacts produits sont ceux listés en
  [Sortie](#sortie), et l'exécution se termine par un rapport des fichiers créés,
  modifiés et ignorés (avec la raison).

**Statut du contrat.** Il n'est pas auto-modifiable. Aucune exécution de ce skill ne
réécrit ces clauses, et aucune adaptation au modèle courant ne les assouplit. Elles ne
changent que par `skill-optimizer`, avec validation humaine et incrément de version —
même règle que l'interdiction d'écriture de `compile-rules`.

C'est aussi la source unique du rubric de `skill-bench` : voir
[references/fixture-conformite.md](references/fixture-conformite.md).

---

## Méthode — indicative

Ce qui suit est un déroulé qui marche, pas une procédure à respecter à la lettre. Le
modèle arbitre selon le contexte du projet ; s'en écarter n'est pas une violation tant
que le Contrat tient.

### 1. Reconnaissance (sans question)
Lire ce qui existe déjà et en tirer le maximum de contexte avant toute question (C5).

### 2. Salves de questions fermées
Regrouper par thème, viser 4 questions maximum par salve, et s'arrêter dès que le
CLAUDE.md peut être rédigé sans inventer. Thèmes à couvrir, dans l'ordre qui a du sens
pour ce projet, en sautant tout thème déjà établi par la reconnaissance :
1. **Contexte métier** — type de projet, client, problème n°1 à résoudre, public cible.
2. **Périmètre** — fonctionnalités incluses / exclues du premier livrable.
3. **Stack & hébergement** — framework, base de données éventuelle, cible de déploiement.
4. **Méthode** — TDD ou non, stratégie git, niveau d'autonomie accordé à Claude
   (demander validation à chaque étape vs avancer seul et rendre compte).

Le nombre de salves, leur regroupement et leur ordre sont laissés au jugement : un projet
dont la stack est déjà visible dans `package.json` n'a pas besoin du thème 3.

### 3. Rédaction du CLAUDE.md
À la racine du projet, en suivant le gabarit et les règles de rédaction de
[references/bonnes-pratiques-claude-md.md](references/bonnes-pratiques-claude-md.md).

Avant de rédiger, vérifier la présence du bloc **Mode de collaboration** dans
`~/.claude/CLAUDE.md` (chercher la ligne « Le désaccord est attendu »).
- **Présent** → ne pas le recopier dans le projet ; il s'applique déjà à toutes les
  sessions de la machine.
- **Absent** (nouvelle machine, `~/.claude/CLAUDE.md` inexistant) → proposer en question
  fermée : l'ajouter à `~/.claude/CLAUDE.md` (recommandé, une seule source pour tous les
  projets) ou l'inscrire dans le CLAUDE.md du projet seul.

### 4. Validation
Présenter le CLAUDE.md et demander une validation en question fermée (valider / ajuster).

### 5. Amorçage du BRAIN et du journal d'erreurs
Dérouler [references/journal-erreurs.md](references/journal-erreurs.md) : arborescence
`~/brain/<PROJECT_KEY>/`, bloc de journalisation appendé au CLAUDE.md, bloc de routage
laissé dormant.

### 6. Suite
Proposer l'étape suivante (bootstrap du repo, première feature) — par exemple via le
skill `greenfield-tdd-okf` s'il est disponible.

---

## Sortie
- `CLAUDE.md` à la racine du projet, validé par l'utilisateur.
- `~/brain/<PROJECT_KEY>/` : `rules/`, `bag.ndjson` vide, `PENDING-rules-block.md`.
- `~/brain/global/rules/`.
- Zéro autre fichier généré par ce skill.

## Évolution de ce skill
- Gabarit du CLAUDE.md et règles de rédaction → `references/bonnes-pratiques-claude-md.md`.
- Mécanique BRAIN / journal d'erreurs → `references/journal-erreurs.md`.
- Scénario de non-régression → `references/fixture-conformite.md`.
- **Méthode** : modifiable librement, y compris pour s'adapter à un modèle plus capable.
- **Contrat** : modifiable seulement via `skill-optimizer` + validation humaine, en
  incrémentant `v1` et en rejouant la fixture. Un contrat qui change sans que la fixture
  soit rejouée est une dérive, pas une amélioration.
