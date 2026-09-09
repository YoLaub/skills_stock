# Invariants de rédaction du CDC

Huit règles, chacune tirée d'un passage réel du `cdc.md` d'EphemeralOS. Ce sont les
propriétés qui rendent le document utilisable des mois plus tard — pas des préférences
de style.

---

## 1. La décision et sa justification sur la même ligne

Le tableau des choix techniques a trois colonnes : **domaine, solution retenue,
justification**. Jamais deux. Une décision sans justification écrite sera rouverte à la
première contrariété, et personne ne saura ce qu'elle protégeait.

> | **Chiffrement** | LUKS, phrase demandée au démarrage | Une machine en autologin porte une clé d'API et des données : sans chiffrement, quiconque a le disque a tout. |

La justification dit **ce qui casse sans cette décision**, pas ce que la solution fait.

## 2. Les conséquences en cascade sont écrites, pas laissées à déduire

Une décision qui en ferme une autre le dit sur place, avec le renvoi.

> Conséquence architecturale directe : un compositeur kiosque mono-surface (Cage) est
> exclu. Voir §2 et §4.

Et quand une décision invalide une exigence déjà écrite, on ne la cache pas : on ouvre
une sous-section pour l'acter.

> #### 4.2. Conséquence sur les critères de performance
> Le chiffrement LUKS et la bascule A/B rendent l'objectif de 4 secondes du §6
> inatteignable en l'état. Le §6 est révisé en conséquence.

C'est le test le plus discriminant du document : un CDC où rien ne se contredit est un
CDC où les conséquences n'ont pas été cherchées.

## 3. Le non-périmètre est une section à part entière

« Ce que le système n'est pas » vaut autant que ce qu'il est, et se rédige en phrases
fermes, pas en réserves.

> Pas de barre des tâches, pas de menu d'applications, pas d'icônes de bureau : le
> lancement d'une application passe par le chat.

Cette section est ce qui permet de refuser une demande plus tard sans rediscuter le
projet entier.

## 4. Une inconnue se marque, avec son déclencheur

`_à décider_` seul est un trou. `_à décider_` avec ce qui le lèvera est un plan.

> | Transcription vocale d'un énoncé court | _à décider_ | Après mesure de `whisper.cpp` sur aarch64. |

Jamais de valeur plausible inventée pour éviter un blanc. Un chiffre non mesuré présenté
comme une cible pollue toutes les décisions qui s'y appuient.

## 5. Un seuil porte sa définition de mesure

Trois colonnes : **critère, cible, définition de la mesure**. Sans la troisième, deux
personnes mesureront deux choses différentes et le seuil ne tranchera rien.

> | **Sortie de veille → chat utilisable** | **≤ 2 s** | Critère principal : c'est ce que l'utilisateur subit plusieurs fois par jour. |

Et le statut des seuils s'écrit une fois pour toutes :

> Un seuil qui n'est pas mesuré n'existe pas. Un seuil dépassé et non écrit est un mensonge.

Le dépassement devient une dette explicite inscrite au document — il ne bloque pas le
développement et ne se dissimule pas.

## 6. Un critère d'arbitrage unique, déclaré tôt

Le document nomme, dès la vision, ce qui tranchera les compromis futurs.

> **Cible d'usage : machine secondaire réellement utilisée au quotidien.** Toute
> fonctionnalité doit résister à un usage répété, pas seulement à une démonstration.
> C'est ce critère qui arbitre les compromis entre élégance et robustesse.

Sans ce critère, chaque arbitrage ultérieur redevient une question d'opinion.

## 7. Le document est un graphe, pas une liste

Les renvois croisés (§2, §3.2.1, §5) sont systématiques et dans les deux sens : la
décision renvoie à ce qui la contraint, la contrainte renvoie à ce qu'elle a produit.
Une section qu'aucune autre ne cite est probablement décorative — la supprimer ou la
rattacher.

## 8. Le phasage se termine sur des critères démontrables

Chaque phase a un critère de sortie **vérifiable par observation sur la machine cible**,
et la phase suivante ne commence pas avant. Un échec rouvre nommément les sections
concernées.

> **Critère de sortie :** les points 1, 2 et 3 du §2.4 sont tranchés par l'observation.
> Si le rendu `layer-shell` échoue, les §2 et §3 sont rouverts avant d'aller plus loin.

Une phase dont le critère de sortie ne peut pas encore être écrit l'écrit quand même :
`_à définir_ à l'entrée de la phase`.

---

## Ton

Phrases affirmatives, présent de l'indicatif, pas de conditionnel de politesse. Le CDC
dit ce que le système fait et ce qu'il ne fait pas ; il ne dit pas ce qu'il « pourrait
idéalement » faire. Le gras se réserve aux clauses contraignantes, pas à l'emphase.
