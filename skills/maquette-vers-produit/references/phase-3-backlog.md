# Phase 3 — Du diagnostic au backlog

## Une issue par écart

Chaque case non cochée en phase 1 devient une issue. Le format qui a marché :

```markdown
# [MAQ-007] — Modules d'observation du cycle

## Ce que la maquette montre
> « Flux · 1 à 2 protections, jamais saturées »   ← citation VERBATIM, avec sa source

## Ce que le produit fait aujourd'hui
7 libellés rendus sur 147 maquettés ; `details` accepte n'importe quelle valeur.

## Ce qu'il faut
- [ ] ...

## Critère d'acceptation
- [ ] ...
```

Ce qui compte : la **citation verbatim** de la maquette. Sans elle, l'issue devient une
reformulation, et la reformulation dérive. Ajouter un préfixe de domaine (`MAQ-`, `UI-`,
`BUG-`), un label et un jalon, pour que le lot se compte tout seul.

## La maquette gagne sur le vocabulaire

Les mots de la maquette deviennent les noms du code, des routes et des colonnes. Quand
le code appelle « monnaie » ce que la maquette appelle « éclats », la conversation avec
l'utilisateur se met à coûter une traduction à chaque phrase, et les deux camps finissent
par ne plus parler du même objet.

Cas particulier vécu : un même mot peut désigner **deux choses** dans la maquette (chez
LOAR, « pépite » est à la fois une catégorie de contenu et une monnaie). Ne pas trancher
en silence pour « faire propre » : le noter, et demander.

## Les conflits ne s'arbitrent pas tout seuls

Quand un document de cadrage existant et la maquette se contredisent, **remonter à
l'utilisateur**, en citant les deux verbatim.

L'exemple qui a bloqué un lot entier sur LOAR : le cadrage écrit « rien d'autre n'est en
vente : ni contenu éditorial, ni fonctionnalité », la maquette vend des méditations
audio et un guide de 42 pages. Vendre du contenu thérapeutique dans une app de santé
n'est pas la même proposition que vendre des cosmétiques, et le cadrage motivait sa
position. Aucun choix de développeur ne pouvait être le bon.

Signaux qu'on est devant un arbitrage et non devant une décision technique : les deux
sources sont **datées et intentionnelles**, le choix change la proposition de valeur, ou
il touche à de l'argent, de la santé ou de la vie privée.

## Questions de périmètre : les poser tôt

Toute la maquette n'est pas destinée à l'app. Sur LOAR, les entités « wiki » étaient des
données saisies dans le hub pour spécialiser l'assistant — invisibles côté app. Une
demi-heure de question a économisé un lot de specs inutiles.

## Ordonner les specs

L'ordre est au développeur, sauf indication contraire — mais il se choisit pour la
**cohérence de domaine**, pas pour la facilité : les specs d'un même domaine partagent
une migration et une fiche. Une PR non mergée oblige à chaîner la suivante sur elle ;
c'est la vraie raison de ne pas laisser traîner une PR verte.
