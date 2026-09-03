# Supervision — délégation par unité isolée (ActivCreew)

À dérouler à l'étape 4 **quand le périmètre contient au moins 2 vues indépendantes**.
Une seule vue → l'intégrer directement, le coût de délégation ne se justifie pas.

**Unité, pour `ux-ui-strategy`** : une vue de maquette (un écran) et le(s) fichier(s) de
prod qui la portent. Deux vues sont indépendantes si elles ne partagent pas de composant
à modifier (un composant `packages/ui` partagé retouché = une seule unité qui couvre les
deux vues, ou une unité "composant" séparée traitée en premier).

Adapté de `greenfield-tdd-okf` (`mode-coder-execution.md`), au modèle de branches imposé
`git-workflow-chantier` et à la stack ActivCreew.

## 1. Le superviseur ne code pas

Dès qu'il y a plus d'une vue non bloquée, le thread principal devient superviseur :
il découpe par vue, délègue, contrôle la non-régression, agrège — il ne restyle
lui-même aucune vue. Raison : sinon il accumule dans son contexte les diffs de markup
et les sorties de build/E2E de toutes les vues, et sature.

## 2. Isoler chaque unité (worktree dédié)

```bash
git worktree add ../full-project-<slug> -b feat/<slug>-ui <base>
```

- `<base>` = **la branche principale du chantier** (`feat/<chantier>`), jamais `main`,
  jamais `dev` (`git-workflow-chantier` §1).
- Un worktree par vue parallèle : deux sous-agents dans le même arbre = checkout
  conflictuel + fichiers de build partagés.
- Ports dev : `dev-worktree.sh` à la racine si une vue doit être lancée pour vérif
  visuelle.

**Point d'agrégation partagé** (`globals.css` pour un token, un barrel `packages/ui`) :
pas un motif de sérialisation si chaque sous-agent n'ajoute qu'UNE entrée. Un **nouveau
composant `packages/ui` partagé** entre deux vues, lui, se traite comme une unité à part,
en premier.

## 3. Déléguer un sous-agent frais par unité

Un sous-agent **général** (pas un fork). Prompt autonome :

- Chemin du worktree = répertoire de travail.
- La vue de maquette concernée (`docs/maquettes/<fichier>#<vue>`) + les fichiers de prod
  cibles + les annotations d'UX de la maquette (règles `DON-XXX` etc.) **copiées
  verbatim**.
- Chemin de `CLAUDE.md` du repo.
- Chemins des `references/` à lire : `design-system-mapping.md` (tokens HSL, composants
  `packages/ui`, table maquette→tokens), `contrat-non-regression.md` (ce que les tests
  savent localiser : `data-testid`, textes assertés, ARIA), `patterns-integration.md`
  (patterns ❌/✅, pièges accents en strings).
- **Contrat à préserver, listé explicitement** : les `data-testid` de la vue, les textes
  cherchés par `getByText` / `getByRole({name})`, les attributs ARIA assertés, les
  handlers / appels API / états. On change la FORME, jamais le FOND.
- Consigne : zéro couleur en dur (tout via tokens), mobile-first, tous les états
  (loading/skeleton, vide, erreur, disabled, focus), `french-accents` sur tout TSX,
  imports `@workspace/...`. Ne toucher qu'aux fichiers de sa vue + aux tokens partagés
  (une ligne).
- **Ne jamais merger soi-même** : quand build + lint + les specs de la vue sont verts,
  rendre la main avec un rapport court (vue intégrée, testid préservés, specs vertes, ou
  blocage).

## 4. Contrôle de conformité avant de déclarer l'unité "faite"

Lancer un **2e** sous-agent frais (général — **jamais** celui qui a intégré la vue).
Entrée seulement : le contrat à préserver copié verbatim + la maquette de la vue + le
diff de l'unité (`git diff <base>...<branche>`).

Consigne, par vue :
1. Chaque `data-testid` / texte asserté / attribut ARIA du contrat est-il **toujours
   présent, sur l'élément qui garde le même rôle d'interaction** ? (absent / déplacé =
   régression)
2. Aucun handler / appel API / état modifié dans le diff ?
3. Rejouer la suite dans un worktree détaché :
   ```bash
   git worktree add ../full-project-verify-<slug> --detach <branche>
   cd frontend && pnpm --filter <package> test
   pnpm exec playwright test <specs de la vue>
   pnpm build && pnpm lint
   ```
4. Conformité visuelle vs maquette : hiérarchie, espacements, couleurs via tokens
   (aucun `#hex` / `gray-XXX` en dur dans le diff), états, responsive.

Régression de contrat, test cassé, ou couleur en dur → **blocage** (§6). Une relance
ciblée de l'intégrateur (si un test casse, c'est le markup, jamais le test), sinon
escalade.

## 5. Gate — non-régression bloquante, non négociable

- Une vue n'est livrable que si **toutes les specs E2E/RTL qui passaient avant passent
  après**, `pnpm build` et `pnpm lint` à 0 erreur.
- Si une spec casse : c'est la forme qui a cassé le fond → corriger le markup, **jamais**
  le test.
- Pas de hand-off / fin de chantier tant qu'une seule vue du périmètre n'a pas passé ce
  gate.

## 6. Agréger — sans merger vers dev

1. Attendre la fin de chaque sous-agent ou son blocage.
2. Contrôle de conformité par vue (§4).
3. Ramener chaque branche de vue sur la branche principale du chantier par MR
   (`glab mr create --target-branch feat/<chantier>`), une à la fois, **confirmation de
   l'utilisateur avant chaque merge**.
4. `git worktree remove ../full-project-<slug>`.
5. **Ne jamais merger vers `dev` de sa propre initiative** (builds Coolify —
   `git-workflow-chantier` §3). Le skill s'arrête après avoir tout ramené sur la branche
   principale + résumé de fin de chantier.
6. Blocage : le superviseur décide — corriger le prompt et relancer **une** fois, ou
   escalader. Les autres vues continuent.

## 7. Relancer

Lot mergé → s'il reste des vues non traitées, recalculer le lot et répéter, sinon
→ étape 5 du SKILL.md (vérification visuelle & non-régression globale).
