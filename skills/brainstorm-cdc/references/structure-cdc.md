# Squelette du CDC — 8 sections

Structure éprouvée sur EphemeralOS. Les intitulés s'adaptent au domaine ; l'ordre et le
rôle de chaque section, non : chacune répond à une question que la suivante suppose déjà
résolue.

Les sections sont numérotées et référencées entre elles (§4.1, §6.2). La numérotation
n'est pas cosmétique : c'est l'adressage qui rend les renvois croisés possibles.

---

## 1. Vision et objectifs

Ce que le système est, avant toute considération technique.

- Trois ou quatre phrases de définition, en une puce chacune.
- **1.x Nature et ambition** — la forme de livraison, et la **cible d'usage qui servira
  de critère d'arbitrage** (invariant 6).
- **1.x Périmètre** — ce qui entre. Chaque inclusion qui contraint l'architecture porte
  sa conséquence sur place (invariant 2).
- **1.x Modularité** — ce qui est optionnel, et la règle : le noyau ne dépend jamais
  d'un module.
- **1.x Comportement dégradé** — ce que fait le système quand sa dépendance principale
  est absente. Section presque toujours oubliée, presque toujours structurante.
- **1.x Ce que le système n'est pas** — le non-périmètre (invariant 3).
- **1.x Critère de succès** — une phrase, vérifiable par observation, qui renvoie aux
  scénarios du §8.

## 2. Architecture globale

Un schéma ASCII des composants et de leurs canaux de communication, puis les
sous-sections qui justifient les frontières : pourquoi ce processus est séparé, ce qui
survit à quoi, quels points restent à trancher par l'observation.

Le schéma sert de carte au reste du document ; les §3 à §5 s'y réfèrent.

## 3. Spécifications fonctionnelles

Ce que l'utilisateur fait, du point de vue de l'utilisateur. Une sous-section par
grande capacité. C'est la section la plus longue et la plus révisée — la garder
descriptive, sans choix d'implémentation (ils sont au §4).

## 4. Spécifications techniques

**Le tableau à trois colonnes** : domaine · solution retenue · justification
(invariant 1). Une ligne par choix structurant, pas de bibliothèque anecdotique.

Puis les sous-sections pour ce qui ne tient pas en une ligne : une interface à plusieurs
implémentations, une règle commune à tous les backends, et **les conséquences de cette
section sur les seuils du §6** (invariant 2).

## 5. Sécurité, isolation et autorisations

Le modèle de menace et les barrières. Pour un système qui exécute du code ou des
commandes, cette section est aussi contraignante que le §4.

Écrire ici les règles qui ne se négocient jamais, sous une forme opposable : qui
attribue un niveau de risque, ce qui vaut approbation, ce qui ne peut pas être modifié
par le système lui-même.

## 6. Contraintes et critères de performance

- **6.1 Seuils** — tableau à trois colonnes : critère · cible · définition de la mesure
  (invariant 5). Les inconnues en `_à décider_` avec leur déclencheur (invariant 4).
- **6.2 Statut des seuils** — qui mesure, quand, et ce qui arrive en cas de dépassement.
- **6.3 Robustesse et modes dégradés** — tableau « ce qui tombe » / « ce qui doit
  survivre », une ligne par composant du schéma du §2.

## 7. Feuille de route

Une phase par saut de nature, pas par lot de fonctionnalités. Chaque phase :
son contenu en liste numérotée, puis **un critère de sortie démontrable** (invariant 8).

La première phase est un **essai jetable** qui valide l'hypothèse la plus risquée de
l'architecture, avant toute ligne de code de production. Si elle échoue, elle rouvre
nommément les sections concernées — c'est son intérêt.

## 8. Scénarios de validation

Trois à cinq scénarios narratifs, du point de vue de l'utilisateur, qui traversent tout
le système. Ils sont cités comme critères de sortie par les phases du §7.

**Inclure au moins un scénario qui doit échouer** : une tentative d'action interdite,
une panne, une entrée hostile. Un jeu de scénarios qui réussissent tous ne valide rien.
