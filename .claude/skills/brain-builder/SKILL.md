---
name: brain-builder
description: >
  Crée et maintient des "cerveaux projets" sous forme de vaults Obsidian structurés en Markdown,
  inspirés de l'approche LLM Wiki d'Andrej Karpathy. Chaque projet obtient son propre vault isolé
  avec l'architecture 3 couches (raw/wiki/reports), prêt à être connecté à un cerveau central.
  Utilise ce skill dès que l'utilisateur mentionne : "cerveau projet", "mémoire persistante",
  "vault Obsidian", "mini cerveau", "LLM wiki", "mémoire IA structurée", "bootstrap projet",
  "initialiser un nouveau projet avec mémoire", ou toute demande de structure de connaissance
  durable pour un projet. Se déclenche aussi pour les phases suivantes : compiler le raw en wiki,
  linter le vault (détection d'orphelins, liens cassés, incohérences), ou connecter un cerveau
  projet au cerveau central.
---

# Brain-Builder

Skill de construction et maintenance de cerveaux projets basés sur l'approche **LLM Wiki** de Karpathy, déployés comme vaults Obsidian autonomes.

## Philosophie

Chaque projet a son propre cerveau. Un cerveau = un vault Obsidian = un dossier isolé contenant trois couches :

1. **`raw/`** — Sources immuables (PDF, transcripts, dumps de code, notes brutes). L'IA lit, ne modifie jamais.
2. **`wiki/`** — Mémoire active compilée par l'IA. Notes d'entités interconnectées, MOC (Maps of Content), synthèses.
3. **`reports/`** — Conclusions, analyses, rapports de haut niveau. Peuvent nourrir le wiki en retour.

Le format Markdown + YAML garantit la souveraineté des données, la pérennité, et permet à l'humain comme à l'IA de collaborer sur les mêmes fichiers.

## Phases du skill

Ce skill couvre quatre phases qui peuvent s'exécuter indépendamment :

| Phase | Commande déclencheur (user) | Ce que fait le skill |
|-------|-----------------------------|----------------------|
| **1. Bootstrap** | "crée un cerveau pour X" / "initialise un vault pour X" | Crée la structure 3 couches + fichiers d'amorce |
| **2. Compilation** | "compile le raw en wiki" / "synthétise ce que j'ai ajouté" | Lit raw/, génère/met à jour wiki/ |
| **3. Linting** | "linte le cerveau" / "audit du vault" | Détecte orphelins, liens cassés, incohérences |
| **4. Connexion centrale** | "connecte ce cerveau au central" | Crée les liens inter-vaults vers le cerveau central |

**Phase 1 (Bootstrap) est la phase actuellement complètement implémentée. Les phases 2-4 ont leurs conventions définies mais sont à enrichir au fur et à mesure des besoins.**

---

## Phase 1 : Bootstrap (détaillée)

### Étape 1.1 — Capture d'intention

Avant de créer quoi que ce soit, collecter les informations essentielles. Si elles ne sont pas déjà dans la conversation, demander (idéalement en une seule passe avec `ask_user_input_v0`) :

1. **Nom du projet** (identifiant court, kebab-case de préférence : `activcreew`, `loar`, `mon-app`)
2. **Chemin du vault** (ex: `~/ObsidianVaults/activcreew-brain/` — par défaut suggérer ce pattern)
3. **Description courte** (1-2 phrases, sera la racine de l'identité du cerveau)
4. **Stack / domaine** (pour calibrer les premières entités : "Strapi + Next.js", "SwiftUI + FastAPI", "recherche bio", etc.)
5. **Sources initiales disponibles** (optionnel : l'utilisateur a-t-il déjà des docs à poser dans `raw/` dès le bootstrap ?)

### Étape 1.2 — Exécution du bootstrap

Deux voies possibles selon l'environnement :

**Voie A — Script Python (préférée, déterministe, rejouable)**

```bash
python /chemin/vers/brain-builder/scripts/bootstrap_brain.py \
  --name "activcreew" \
  --path "~/ObsidianVaults/activcreew-brain" \
  --description "Backend Strapi v5 + Turborepo frontend" \
  --stack "strapi,nextjs,postgres"
```

Le script crée l'arborescence complète et copie les templates. Il est **idempotent** : si le vault existe déjà, il ne détruit rien, il complète uniquement ce qui manque.

**Voie B — Création manuelle via tools de fichiers (fallback si pas d'accès shell ou MCP Obsidian uniquement)**

Suivre l'arborescence décrite dans `references/vault-structure.md` et copier les templates un par un.

### Étape 1.3 — Personnalisation post-bootstrap

Une fois la structure créée, personnaliser les fichiers d'amorce :

1. **`wiki/INDEX.md`** — Map of Content racine. Renseigner les premières entités prévisibles selon la stack (ex: pour Strapi → `Auth`, `User`, `Content-Types`, `Plugins`).
2. **`wiki/_meta/IDENTITY.md`** — Carte d'identité du cerveau. Nom, objectif, périmètre, hors-périmètre.
3. **`wiki/_meta/CENTRAL_LINKS.md`** — Déjà créé vide, prêt à accueillir les liens vers le cerveau central quand il existera (voir `references/central-brain-protocol.md`).
4. **`.obsidian/`** — Si possible, poser une config Obsidian minimale (voir `assets/templates/obsidian-config/`).

### Étape 1.4 — Vérification

Après bootstrap, toujours produire un récapitulatif à l'utilisateur :

```
✅ Cerveau "activcreew" créé à ~/ObsidianVaults/activcreew-brain/

Structure :
  raw/          (0 fichiers — à remplir)
  wiki/         (4 fichiers d'amorce)
  reports/      (vide)
  .obsidian/    (config minimale)

Prochaines étapes suggérées :
  1. Ouvrir le vault dans Obsidian
  2. Déposer tes premières sources dans raw/
  3. Me demander "compile le raw en wiki" quand tu as du contenu
```

---

## Phase 2 : Compilation (à détailler au premier usage)

**Objectif** : lire le contenu de `raw/`, en extraire les entités et concepts, et mettre à jour les notes dans `wiki/`.

**Principes directeurs** (à respecter même dans les itérations futures) :

- **Jamais de modification de `raw/`.** C'est la source de vérité immuable.
- **Incrémental, pas régénératif.** Si une note `wiki/Auth.md` existe déjà, l'enrichir, pas la réécrire.
- **Toujours citer la source.** Chaque fait ajouté dans le wiki doit référencer le fichier raw d'origine via un lien Markdown ou un champ YAML `source:`.
- **Signaler les contradictions.** Si une nouvelle source contredit une note existante, créer une section `## Contradictions` plutôt que d'écraser.
- **Mettre à jour `wiki/INDEX.md`** à chaque compilation (ajout de nouvelles entités).

Workflow minimal à implémenter quand l'utilisateur demande une compilation :
1. Lister les fichiers de `raw/` avec leur date de modif
2. Comparer avec le `_meta/COMPILATION_LOG.md` pour identifier ce qui est nouveau
3. Pour chaque nouvelle source, extraire les entités et les injecter dans `wiki/`
4. Logger l'opération dans `_meta/COMPILATION_LOG.md`

Détails complets à construire lors du premier usage réel — le squelette est dans `references/note-templates.md`.

---

## Phase 3 : Linting (à détailler au premier usage)

**Objectif** : garantir la cohérence et l'intégrité du cerveau.

**Vérifications minimales** :
- Liens Markdown cassés (`[[NoteInexistante]]`)
- Notes orphelines (aucun lien entrant ni sortant)
- Champs YAML obligatoires manquants (`created`, `tags`, `source`)
- Duplications sémantiques (deux notes sur le même sujet avec noms proches)
- Notes dans `wiki/` sans aucune référence à une source de `raw/`

Le linting produit un rapport dans `reports/linting/YYYY-MM-DD-lint-report.md` avec une section "action items" priorisée.

---

## Phase 4 : Connexion au cerveau central (à détailler quand le central existe)

**Objectif** : permettre à chaque cerveau projet de référencer et être référencé par un cerveau central commun (concepts transverses, méthodes, préférences personnelles, leçons apprises).

Le protocole est spécifié en amont dans `references/central-brain-protocol.md` — il définit :
- La convention de chemin du central (`~/ObsidianVaults/central-brain/`)
- Le format des liens inter-vaults (symlinks ou liens Markdown avec chemin relatif)
- La règle de non-duplication (un concept vit dans le central **OU** dans le projet, jamais les deux)
- Le fichier `_meta/CENTRAL_LINKS.md` qui sert d'interface

Cette phase sera activée quand l'utilisateur créera son cerveau central — le skill est déjà câblé pour l'accueillir.

---

## Fichiers de référence

Lire ces fichiers selon la phase :

- `references/vault-structure.md` — Arborescence complète, obligatoire pour toutes les phases
- `references/note-templates.md` — Templates YAML + squelettes de notes par type
- `references/central-brain-protocol.md` — Convention de liaison inter-vaults

## Scripts

- `scripts/bootstrap_brain.py` — Création déterministe de la structure (phase 1)

## Assets

- `assets/templates/` — Fichiers Markdown d'amorce copiés tels quels au bootstrap

---

## Principes de qualité

- **Un cerveau = un vault isolé.** Jamais de fusion forcée, la propreté d'isolation est un feature.
- **Markdown pur + YAML.** Pas de format propriétaire, pas de base de données. Le vault doit rester lisible dans `cat`.
- **L'utilisateur est copilote.** Tous les fichiers créés par l'IA peuvent être édités à la main sans casser le système.
- **Préparer l'avenir.** Même en phase 1, la structure est pensée pour accueillir compilation, linting, et liaison centrale sans refactor ultérieur.
- **Documenter les décisions.** Toute règle ou convention appliquée au cerveau est écrite dans `_meta/CONVENTIONS.md` — la mémoire du système sur lui-même.
