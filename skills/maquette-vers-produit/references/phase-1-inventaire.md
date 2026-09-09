# Phase 1 — Inventaire exhaustif et extraction

## La méthode rejetée, et pourquoi

Premier réflexe sur LOAR : compter les libellés de la maquette présents dans le code, et
en déduire un taux de couverture par écran. **Cette méthode ment.** Elle mesure la
présence d'une chaîne de caractères, pas l'existence d'un comportement : un écran qui
affiche « Voir les pépites » sans rien derrière compte comme couvert. Elle a produit un
audit optimiste que la suite a démenti sur presque chaque écran.

La méthode retenue, dictée par l'utilisateur :

> « tu les listes, puis tu vérifies, tu extrais la logique et tu coches, et tu vérifies
> la liste, et ainsi de suite ; une fois chaque coche faite tu pourras enfin dire j'ai
> tout vérifié »

Trois propriétés qui font la différence : la liste est **écrite avant** la vérification
(on ne peut pas rétrécir le périmètre en cours de route), une case se coche sur une
**logique extraite** et non sur un libellé aperçu, et la liste **se relit** à la fin.

## Le fichier de cases à cocher

Un fichier, hors du code, une ligne par écran ou bloc de la maquette :

```markdown
- [ ] `cycle` — Cycle · 11 modules d'observation, prédiction + marge, historique
- [x] `trousse` — Pilulier · prises du jour groupées par moment, « au besoin » plafonné
```

Règles :
- l'inventaire se fait **depuis la maquette**, jamais depuis le code — sinon on ne peut
  trouver que ce qui existe déjà ;
- un bloc répété (un segment persistant, un en-tête) est UNE ligne, pas une par écran ;
- rien n'est coché « à moitié ». Un écran aux deux tiers reste décoché, avec sa note.

## Ce qu'on extrait, écran par écran

Pour chaque écran, six questions. Les six, systématiquement — c'est leur mécanicité qui
attrape ce qu'une lecture attentive laisse passer :

1. **Les données affichées** — chaque valeur, avec son unité et son format.
2. **Les états** — vide, chargement, erreur, et l'état « pas assez d'historique ».
3. **Les actions** — chaque bouton, ce qu'il écrit, où il mène.
4. **Les portes d'entrée et de sortie** — par où on arrive sur cet écran, par où on
   en part.
5. **Les règles implicites** — seuils, bornes, arrondis, tri, ce que la maquette
   affirme dans ses textes d'exemple (« 3 à 4 protections, changées toutes les 4 à 6 h »
   est une échelle, pas une décoration).
6. **Le vocabulaire** — les mots exacts. Ils deviennent les noms du code.

## L'accessibilité ne se vérifie pas à l'œil

Sur LOAR, la revue manuelle a trouvé 5 écrans inatteignables ; un test parcourant le
graphe de navigation depuis les racines d'onglets en a trouvé **13**. Huit écrans codés,
testés, et morts.

Installer le garde correspondant (`gardes-de-depot.md`, « accessibilité des écrans »)
AVANT de conclure la phase 1. Le piège de résolution route → fichier est documenté dans
`pieges.md`.

## Discipline de comptage

Ne jamais annoncer un chiffre de mémoire. Sur LOAR j'ai annoncé « treize specs livrées »
là où le fichier disait 11 complètes et 1 aux deux tiers, et « tout est vert » alors que
52 tests étaient skippés faute de base démarrée.

Avant tout compte annoncé : relire le fichier, et distinguer *livré* de *commencé*.
