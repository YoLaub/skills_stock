# Exécution Phase 3 (mode coder) — superviseur / sous-agents

Protocole autonome (aucune dépendance à un autre skill du dépôt) pour dérouler les
issues d'un milestone. Le thread principal ne code jamais lui-même une issue dès qu'il
y a plus d'une issue non bloquée à traiter : il devient superviseur et délègue.

## 1. Calculer le lot exécutable

1. Lister les issues ouvertes du milestone en cours (`gh issue list --milestone ...`).
2. Une issue est **non bloquée** si toutes les issues listées dans sa ligne
   `Depends on #<numéro>` sont fermées (ou si elle n'en a pas).
3. Le lot = toutes les issues non bloquées à cet instant. S'il n'y en a qu'une, la
   traiter directement en Phase 3 classique (pas besoin de sous-agent : le coût de
   délégation ne se justifie pas pour une seule issue séquentielle). S'il y en a deux ou
   plus, appliquer la délégation ci-dessous.

## 2. Isoler chaque issue (worktree dédié)

Pour chaque issue du lot, avant de lancer le sous-agent :

```bash
git worktree add ../<repo>-issue-<numéro> -b issue-<numéro>-<slug> main
```

- Un worktree par issue évite que deux sous-agents modifient le même arbre de travail
  en parallèle (checkout conflictuel, fichiers de build partagés).
- Nommer le dossier de façon prévisible (`<repo>-issue-<numéro>`) pour pouvoir le
  retrouver et le nettoyer après merge.
- Si deux issues du même lot touchent manifestement les mêmes fichiers malgré l'absence
  de `Depends on` déclarée (le backlog s'est trompé), ne pas les paralléliser : les
  repasser en séquentiel et corriger `Depends on` dans l'issue GitHub pour la suite.

## 3. Déléguer un sous-agent par issue

Lancer un agent indépendant par issue du lot (type général, pas un fork — chaque issue
est un contexte propre, rien à hériter de la session en cours). Le prompt doit être
autonome puisque l'agent démarre sans mémoire de cette conversation :

- Chemin du worktree à utiliser comme répertoire de travail.
- Corps complet de l'issue GitHub (description + critères d'acceptation), copié tel
  quel — ne pas résumer, les critères doivent rester vérifiables mécaniquement.
- Chemin de `CLAUDE.md` du projet (conventions, commandes).
- Chemin de `references/pieges.md` du skill parent + rappel de ne lire que la section
  générique et celle de la stack du projet.
- Chemin de `references/okf-fiche-template.md` du skill parent.
- Consigne d'exécution, identique à la Phase 3 séquentielle :
  1. Tests d'abord sur la logique pure (`services/`), UI/routes en orchestration mince.
     Toute logique = un service unique consommé par UI et interfaces machine.
  2. Suite verte → build → E2E réel.
  3. Ouvrir la PR (`Closes #<numéro>`) depuis la branche du worktree.
  4. Écrire la fiche OKF `docs/index/<feature>.md`.
  5. Ajouter les pièges rencontrés à `retro.md` (et à `references/pieges.md` du skill
     parent si générique).
  6. Ne jamais merger soi-même — s'arrêter une fois la PR ouverte et la CI lancée, et
     rendre la main au superviseur.
- Consigne de reporting : à la fin, résumer en quelques lignes (issue traitée, PR
  ouverte, tests verts ou bloquant rencontré) — pas besoin de détail, le superviseur ne
  garde que ce résumé en contexte.

## 4. Superviser

1. Attendre que chaque sous-agent du lot ait ouvert sa PR (ou remonté un blocage).
2. Pour chaque PR : vérifier que la CI est verte (`gh pr checks`).
3. **Demander confirmation à l'utilisateur avant chaque merge** (action visible par
   l'équipe, identique à la Phase 3 séquentielle) — un merge à la fois, pas de merge
   groupé silencieux même si toutes les CI sont vertes.
4. Merger (squash ou merge selon la convention consignée en Phase 2/CLAUDE.md).
   L'issue se ferme automatiquement.
5. Supprimer le worktree traité :
   ```bash
   git worktree remove ../<repo>-issue-<numéro>
   ```
6. Si un sous-agent remonte un blocage (tests rouges persistants, ambiguïté sur les
   critères d'acceptation), ne pas le laisser réessayer en boucle : le superviseur
   décide — corriger le prompt et relancer une fois, ou escalader à l'utilisateur.
   Les autres issues du lot continuent en parallèle, non affectées par ce blocage.

## 5. Relancer

Une fois le lot mergé, recalculer les issues nouvellement non bloquées (étape 1) et
répéter. S'arrêter quand le milestone n'a plus d'issue ouverte → Phase 4.

## Pourquoi ce protocole

- Sans lui, le thread principal accumule dans son propre contexte les logs de test, les
  diffs et les allers-retours de build de **toutes** les issues du projet, à la suite.
  Sur un mode coder qui vise un produit complet (pas juste un module), ça sature vite.
- Le backlog (`docs/05_github_backlog.md`) identifie déjà l'ordre de dépendance des
  Epics ; ce protocole est ce qui manquait pour exploiter cette info au niveau issue et
  paralléliser réellement, au lieu de dérouler une issue à la fois même quand rien ne
  les bloque l'une par rapport à l'autre.
