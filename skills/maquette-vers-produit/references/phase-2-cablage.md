# Phase 2 — Vérification du câblage backend

## Les trois niveaux

Pour chaque donnée que la maquette affiche, trois questions. **Répondre aux trois** :
s'arrêter à la première produit une spec livrée à moitié.

| Niveau | Question | Comment on vérifie |
|---|---|---|
| 1 · Route | l'endpoint existe-t-il ? | grep des routeurs, pas de la doc |
| 2 · Appel | le client l'appelle-t-il vraiment ? | grep du client depuis l'écran |
| 3 · Charge | la réponse porte-t-elle le champ affiché ? | lire le schéma de sortie, pas le modèle |

Le niveau 3 est celui qu'on saute. Une route qui existe et qui est appelée peut très
bien ne pas renvoyer le champ que la maquette met au centre de l'écran — le schéma de
sortie et le modèle ORM ne coïncident pas toujours.

Corollaire tiré d'un retour utilisateur : **une spec backend sans ticket de consommation
est à moitié livrée.** Ouvrir la spec back ET le ticket qui la branche à l'écran, sinon
la donnée existe et personne ne la voit.

## Chercher le point d'extension dormant AVANT de modéliser

Sur LOAR, une spec semblait réclamer onze nouvelles tables pour les modules
d'observation du cycle. La colonne `details_schema` (JSON) existait depuis la migration
initiale, sur la bonne table, **utilisée nulle part** : ni service, ni test, ni seed.
La spec ne demandait pas de modéliser, elle demandait d'activer.

Réflexe à prendre avant toute migration : grep les modèles pour une colonne JSON, un
champ `type`, un enum ou une table de référence qui couvrirait déjà le besoin. Un point
d'extension dormant ne se voit pas dans le code applicatif — précisément parce que rien
ne l'utilise.

## Le compte ne doit pas mentir

Un écran affiche presque toujours un compteur à côté d'une liste filtrée (« Voir les
pépites (3) »). Si le comptage et le listage n'appliquent pas **les mêmes critères**, le
bouton ment — et le mensonge n'apparaît qu'avec des données réelles, jamais en test
unitaire.

Faire porter les critères par une fonction unique, partagée par `lister` et `compter`,
et commenter ce partage à l'endroit où il vit : c'est lui, l'invariant.

## Ce qui doit être tenu dans le code, pas seulement à l'écran

Quand la maquette fait une promesse à l'utilisatrice — « rien ne repart vers ces
applis », « tes données ne sortent pas d'ici » — cette promesse est une **contrainte de
code**, pas un libellé. Elle se teste : une garde qui échoue si un appel sortant
apparaît, une portée en lecture seule vérifiée sur la requête compilée.

## Tester au niveau où la règle vit

Les tests de repository assertent sur le **SQL compilé**, pas sur ce que rend un mock :
une règle d'isolation posée en jointure est invisible à un mock qui renvoie l'objet
attendu. C'est ce qui distingue « le test passe » de « la règle est appliquée ».
