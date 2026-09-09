---
name: brainstorm-cdc
description: >
  Explore une idée de produit encore floue jusqu'à un cahier des charges qui fait foi :
  divergence en conversation ouverte, puis verrouillage de chaque décision par question
  fermée, puis rédaction du CDC. Protocole extrait du cdc.md d'EphemeralOS.
  Intentions déclenchantes : "brainstorm", "on réfléchit à une idée", "j'ai une idée de
  produit", "aide-moi à cadrer", "écris le cahier des charges", "on cadre le projet".
  À utiliser AVANT init-projet (qui écrit le CLAUDE.md d'un projet déjà cadré) et avant
  greenfield-bootstrap (qui construit un produit déjà décidé). Ne pas utiliser pour
  explorer une option à l'intérieur d'un projet déjà cadré : c'est une conversation
  ordinaire, pas ce skill.
---

# Brainstorm → CDC

Amener une idée de l'état « intuition » à l'état « document qui fait foi ». Le livrable
est un `cdc.md` dont les décisions portent leur justification, dont les inconnues sont
nommées, et sur lequel les skills suivants peuvent s'appuyer sans reposer de questions.

Références (à lire au moment indiqué, pas avant) :
- `references/invariants.md` — les règles de rédaction du CDC, avec les exemples réels
  d'EphemeralOS. À lire **avant d'écrire la première section**, pas avant.
- `references/structure-cdc.md` — le squelette en 8 sections. À ouvrir en phase 3.

## Ce que ce skill n'est pas

- Il ne génère aucun code, aucun dépôt, aucun `package.json`.
- Il n'écrit pas le CLAUDE.md : c'est `init-projet`, une fois le CDC validé.
- Il ne produit pas un backlog : c'est `greenfield-bootstrap` en mode coder.
- Il ne remplit pas les blancs par plausibilité. Une inconnue s'écrit `_à décider_`
  accompagnée de ce qui la lèvera.

---

## Phase 0 — Situer le point de départ

Une seule question ouverte, puis écouter : **qu'est-ce qui existe déjà dans ta tête sur
ce projet ?** Ne pas structurer, ne pas reformuler en plan, ne pas proposer de stack.
L'objectif est d'entendre l'idée dans les mots de l'utilisateur avant de la déformer.

Deux choses à repérer pendant cette écoute, sans les interrompre :
- **le critère d'arbitrage** — ce qui, dans ce projet, tranchera entre deux bonnes
  options. Il est rarement dit explicitement ; il se déduit de ce qui revient.
- **le problème n°1** — ce qui, s'il n'est pas résolu, rend tout le reste inutile.

Si l'utilisateur arrive avec un projet déjà cadré (stack choisie, périmètre arrêté),
le dire et proposer de passer directement à `init-projet` plutôt que de simuler une
exploration.

## Phase 1 — Divergence, en conversation ouverte

Pas de QCM ici. Pas de liste à puces d'options équivalentes. La divergence est une
conversation, et l'agent y a une voix.

Obligations pendant cette phase :

1. **Contredire au moins une fois.** Si aucune objection ne vient, c'est que l'idée n'a
   pas été prise au sérieux. Chercher où elle casse : le cas d'usage répété, la panne,
   le mode dégradé, le premier utilisateur qui n'est pas l'auteur.
2. **Proposer un angle non demandé.** Une contrainte du domaine, un produit voisin qui
   a déjà tranché ce problème, une conséquence que l'utilisateur n'a pas vue.
3. **Chercher l'existant** avant d'inventer : ce qui a une spécification ouverte, une
   API officielle ou une implémentation sous licence permissive ne se réécrit pas.
4. **Nommer l'incertitude.** « Je ne sais pas si ça tient sur cette architecture » est
   une contribution ; une justification fabriquée est une dette silencieuse.

Signal de fin de phase 1 : les questions ouvertes ne produisent plus d'information
neuve, et une liste de carrefours non tranchés s'est accumulée.

## Phase 2 — Verrouillage, par questions fermées

Chaque carrefour identifié en phase 1 devient une question fermée (AskUserQuestion),
une par décision structurante. Règles :

- **Options réelles, pas décoratives.** Si une option est manifestement mauvaise, ne
  pas la proposer : la mentionner comme écartée et dire pourquoi.
- **La description de chaque option porte sa conséquence**, pas sa définition.
  « Exclut un compositeur kiosque » vaut mieux que « permet le multi-fenêtres ».
- **Recommander.** L'option recommandée est la première, marquée `(Recommandé)`.
  Un skill qui refuse d'avoir un avis renvoie le travail à l'utilisateur.
- **Une décision prise en verrouille d'autres.** Après chaque réponse, dire à voix haute
  ce qu'elle vient de fermer, et ne plus reposer ces questions-là.

Ne verrouiller que ce qui a une conséquence sur la suite. Ce qui peut attendre une
mesure attend une mesure, et s'écrit `_à décider_`.

## Phase 3 — Rédaction du CDC

Lire `references/invariants.md`, puis `references/structure-cdc.md`, puis écrire.

- Un seul fichier, `cdc.md`, à la racine.
- **Écrire avec l'outil d'écriture de fichier, jamais par heredoc** : au-delà d'une
  centaine de lignes le heredoc est tronqué et laisse une citation ouverte.
- Écrire section par section, en soumettant les sections structurantes (vision,
  architecture, sécurité) à validation avant de continuer. Ne pas livrer 400 lignes
  d'un coup à relire.
- Rien dans le CDC qui n'ait été décidé en phase 2 ou observé pendant la conversation.
  Aucune section remplie « pour faire complet ».

## Critère de sortie

Le CDC est fini quand ces quatre points sont vrais — les vérifier explicitement et
annoncer le résultat, sans arrondir :

1. Chaque décision technique porte sa justification dans le document.
2. Chaque inconnue est marquée `_à décider_` **et** nommée ce qui la lèvera.
3. Le critère de succès est vérifiable par observation, pas par appréciation.
4. Chaque phase du phasage a un critère de sortie démontrable sur la machine cible.

Puis passer la main : proposer `init-projet` pour écrire le CLAUDE.md à partir de ce
CDC. Ne pas enchaîner sans validation.
