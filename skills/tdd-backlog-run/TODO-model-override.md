# À trancher — override de modèle dans tdd-backlog-run

Note de travail, pas une référence active du skill (rien ici n'est lu pendant
l'exécution). Sert à reprendre la réflexion si on décide d'ajouter des `model:`
overrides comme ailleurs dans le dépôt (`candidate-screener`, `rh-needs-analyst`,
`gap-analyser` → `opus` en frontmatter ; porte de contrôle de `presentation-builder` et
juge de `skill-bench` → `opus` sur le dispatch). Pas encore fait ici.

## Pourquoi ce n'est pas un ajout direct comme les autres

Les overrides déjà posés visaient un **rôle de juge/classification fixe** porté par un
fichier agent dédié ou un point de dispatch unique. `tdd-backlog-run` dispatche deux
types de sous-agents dans `references/execution.md` :

- **Les codeurs d'issue** (§3) : des exécutants (TDD, build, E2E), pas des juges contre
  un rubric fixe. Le bon modèle dépend de la nature de l'issue, pas du rôle — ne se fige
  pas en frontmatter.
- **La porte de conformité** (§4) : un 2e sous-agent frais qui vérifie chaque critère
  d'acceptation = code + test et rejoue la suite. **Ça, c'est un rôle de juge fixe** —
  candidat naturel pour `model: opus`, par le même raisonnement que les autres juges du
  dépôt (un relecteur plus faible que l'auteur du code a des angles morts).

## Deux pistes si on y revient

### 1. Tiering par complexité d'issue (codeurs, §3)

Le superviseur choisirait `model: opus` pour les issues fondatrices/architecturales
(celles dont dépendent beaucoup d'autres via `Depends on`, ou qui posent un choix
structurant) et le modèle par défaut pour les issues routinières (CRUD, ajustements UI).
Suppose d'ajouter un critère de classification à côté du calcul du lot non bloqué (§1) —
un vrai choix à documenter : sur quel signal (nombre de dépendants, mention dans
`docs/05_github_backlog.md`, ou jugement du superviseur).

### 2. `model: opus` sur la porte de conformité (§4)

La porte existe déjà dans `execution.md` §4 (« Vérification de conformité »), sans
override. Lui ajouter `model: opus` sur le dispatch serait cohérent avec la porte de
`presentation-builder` et le juge de `skill-bench`. Coût maîtrisé : un seul sous-agent
opus par PR, pas par sous-agent d'issue. **C'est la piste la plus simple et la mieux
justifiée** — à faire passer par `skill-bench` avant/après pour mesurer.

## Ce qui ne bouge pas sans décision explicite

Ne pas ajouter de `model:` uniforme sur tous les codeurs d'issue (§3) sans trancher la
piste 1 — ça coûterait cher sans bénéfice net sur les issues routinières, majoritaires
dans un backlog typique.
