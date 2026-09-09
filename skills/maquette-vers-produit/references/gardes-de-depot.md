# Catalogue des gardes de dépôt

Un **garde** est un test qui échoue quand un défaut systémique revient, à l'échelle du
dépôt et non d'un composant. Il se justifie quand le défaut est (a) invisible à la revue
de code, (b) réintroductible par mégarde, (c) déjà arrivé.

Catalogue ouvert : ajouter une section par garde, sans toucher aux existantes.

## Règle commune — un garde doit prouver qu'il sait échouer

Un garde qui passe peut très bien ne rien inspecter : chemin mal résolu, regex qui ne
matche jamais, liste vide parcourue. Chaque garde embarque donc ses **sondes** — deux ou
trois cas connus qu'il doit détecter — et **un contre-exemple** qu'il doit laisser
passer. Sans ça, un garde vert n'est pas une information.

## Accessibilité des écrans

**Défaut attrapé** : un écran codé, testé, et joignable par aucun chemin de navigation.
13 sur LOAR.

**Forme** : parcours du graphe de navigation depuis les racines (onglets, écran d'entrée).
Tout écran déclaré et non atteint fait échouer le test.

**Le piège** : résoudre route → fichier par le **nom du composant exporté** donne un faux
positif dès qu'un fichier d'attente (`placeholders/index.tsx`) exporte des homonymes des
vrais écrans — le garde valide alors le stub. Résoudre par les **imports du navigateur**.

## Graisse de police nommée

**Défaut attrapé** : `fontWeight` posé à côté d'une `fontFamily` personnalisée. Sur
Android c'est **ignoré en silence**, et le rendu retombe sur la Regular.

**Forme** : refus, à l'échelle du dépôt, de toute rencontre entre `fontWeight` et une
famille personnalisée — sous ses trois formes : composition de styles, même objet, et
attribut de balise. Chaque graisse est une famille déclarée (`Outfit-Bold`), pas un poids.

**Attention en corrigeant** : la conversion doit être consciente de la famille. Toutes
n'ont pas toutes les graisses ; une conversion aveugle change la typographie.

## Aucune couleur littérale

**Défaut attrapé** : un `rgba(...)` en dur qui échappe au thème — donc au thème nuit.

**Forme** : refus de tout littéral de couleur hors du module de thème. Sur LOAR il a
attrapé le voile d'une modale, qui a donné un token `scrim`.

## La porte de typage

**Défaut attrapé** : `navigate('x' as never, params as never)` compile en `[never, never]`
et casse au typage — piège déjà journalisé, redocumenté dans un écran, et **repassé**,
parce que ni la commande de test ni celle de lint ne typaient.

**Forme** : ce n'est pas un test mais une commande manquante. Vérifier qu'une cible
`typecheck` existe et tourne. Un piège connu qui revient signale une **porte absente**,
pas une inattention.

## Consommateur obligatoire

**Défaut attrapé** : un réglage exposé dans les paramètres que rien ne lit — modifiable,
sans effet.

**Forme** : pour toute donnée de configuration, un test qui prouve qu'un consommateur
existe.
