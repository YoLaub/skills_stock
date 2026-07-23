# Bonnes pratiques CLAUDE.md

## Ce qu'est un CLAUDE.md
Un fichier chargé automatiquement en début de **chaque** session. Chaque ligne coûte du
contexte à chaque session : il doit être court, dense, et ne contenir que ce que Claude
ne peut pas déduire seul du code.

## Gabarit

```markdown
# CLAUDE.md — Conventions du repo <NOM>

## Contexte
<Qui est le client, quel est le problème n°1 à résoudre, en 3-5 lignes.
Mettre en gras le problème central : c'est lui qui arbitre toutes les décisions.>

## Objectifs
<Liste numérotée, ordonnée par priorité. Le n°1 répond au problème n°1.>

## Contraintes
<Ce qui limite les choix : budget, compétences du client, mobile-first, délais.>

## Décisions techniques
<Stack, hébergement, domaine. Marquer `_à décider_` ce qui n'est pas tranché —
ne JAMAIS inventer une décision.>

## Méthode
<Stratégie git, tests, index de session (ex. OKF dans docs/index/), niveau
d'autonomie accordé à Claude.>

## Règles métier clés
<Les règles que le code doit respecter et que Claude ne peut pas deviner :
exigences légales, sources de vérité des données, interdits.>

## Commandes
<dev / test / build / deploy. Compléter dès que la stack est choisie.>
```

## Règles de rédaction
1. **Court** : viser ≤ 60 lignes. Si une section grossit, la déplacer dans `docs/` et
   ne garder qu'un pointeur.
2. **Impératif et vérifiable** : « les prix vivent dans `src/data/` », pas « il serait
   bien de centraliser les prix ». Une règle qu'on ne peut pas vérifier ne sert à rien.
3. **Rien de déductible** : pas de description de l'arborescence, pas d'historique —
   le code et git les portent déjà. Le CLAUDE.md porte l'**intention** et les
   **interdits**.
4. **Source de vérité unique** : toute donnée métier (prix, horaires, coordonnées) a
   un emplacement canonique désigné dans le fichier.
5. **Jamais inventer** : un fait métier inconnu (prix, horaire, nom de domaine) est
   marqué `_à décider_` et redemandé au client — jamais rempli avec une valeur plausible.
6. **Mettre à jour, pas empiler** : quand une décision `_à décider_` est tranchée,
   remplacer la mention ; quand une règle change, réécrire la ligne. Le fichier décrit
   l'état courant, pas son historique.
7. **Le gras arbitre** : une seule idée en gras par section maximum — celle qui doit
   trancher les conflits de priorité.
