---
name: send-feedback
description: Envoie un retour sur les skills yl-solution en amont, sous forme d'issue GitHub sur YoLaub/skills_stock — reprend les mots de l'utilisateur tels quels, propose le contexte technique autour, anonymise avant publication, dépose via gh ou une URL de navigateur pré-remplie. Utiliser quand un skill s'est mal comporté, qu'il manque quelque chose, ou qu'une idée a émergé, et que l'utilisateur n'a pas de clone du dépôt pour la corriger lui-même.
---

# Send Feedback

Ces skills sont livrés par un marketplace à des gens qui n'ont pas de clone du dépôt
d'où ils viennent. Quand l'un d'eux se comporte mal, la leçon meurt dans la session où
c'est arrivé — la personne qui pourrait le corriger n'en entend jamais parler. Ce skill
est le chemin de retour : transformer ce qui vient de mal se passer en issue sur
`YoLaub/skills_stock`.

Il ne nécessite ni token, ni clone, ni droit d'écriture. Le dépôt est public avec les
issues activées, donc **n'importe quel compte GitHub peut en déposer une** — et là où
il n'y a même pas de compte, le brouillon reste disponible pour être collé à la main.

## Ce qui est déposé

Dépôt cible : `YoLaub/skills_stock`, toujours. Titre : `[<nom-du-skill>] <résumé
court>`, ou `[yls]` quand aucun skill précis n'est en cause. Le nom du skill est dans le
titre plutôt que dans un label car **un non-collaborateur ne peut pas poser de labels**
— voir l'étape 5.

Corps : les mots de l'utilisateur cités, puis le bloc de contexte optionnel. Rien
d'autre.

## Étape 1 — Les mots de l'utilisateur, tels quels

Le bloc cité est le sien, pas le tien. Recopier ce qu'il a écrit, sans y toucher — ne
rien couper, ne rien lisser, ne rien traduire.

C'est la seule règle ici sans marge de jugement, parce qu'une reformulation détruit
exactement ce qui fait la valeur d'un retour. Un bug évident survit à être reformulé ;
une nuance ou une idée à moitié formée non — une reformulation retombe sur ce que le
modèle avait déjà compris, ce qui est précisément la partie qui posait problème.

Si l'utilisateur n'a fait que pointer vaguement ("ce skill sert à rien", "bof"),
demander la phrase qu'il voudrait que le mainteneur lise. Mieux vaut attendre ses mots
que les inventer.

## Étape 2 — Proposer le contexte, ne pas le supposer

Rédiger le contexte environnant et le montrer comme un **bloc séparé que l'utilisateur
peut accepter, couper ou refuser entièrement**. La citation seule constitue déjà une
issue valide.

Proposer uniquement ce qui a été réellement observé dans cette session :
- quel skill s'est déclenché, et à quelle étape ça a mal tourné
- attendu versus obtenu
- la reproduction la plus courte possible
- environnement : version du plugin (`claude plugin list`, lire l'entrée `yls@…`), OS,
  version de Claude Code

Pencher vers un bloc complet pour un bug, un bloc léger pour une idée — des étapes de
reproduction sur une suggestion, c'est du bruit. Demander une fois, prendre la réponse ;
ne pas négocier champ par champ.

## Étape 3 — Anonymiser avant de montrer

L'issue est publique et permanente — indexée, mise en cache même après suppression.
Donc nettoyer le brouillon *avant* de l'afficher, pas après : chemins absolus et noms
d'utilisateur, nom de projet/client/employeur, URLs et noms d'hôte internes, tout ce qui
ressemble à une clé. Remplacer par un placeholder et dire ce qui a été remplacé, pour
que l'utilisateur puisse remettre ce qui était inoffensif.

Anonymiser le bloc de contexte ; laisser la citation de l'utilisateur intacte. Si ses
propres mots contiennent quelque chose de privé, le signaler et le laisser reformuler
lui-même.

## Étape 4 — Valider

Montrer le titre exact et le corps exact, tels qu'ils seront publiés. **Ne rien publier
avant un oui explicite.**

Cette règle-là n'est pas une suggestion : publier sur un tracker public sous le compte
de l'utilisateur est une action visible de l'extérieur, irréversible. Avoir demandé le
skill n'est pas une approbation du texte.

## Étape 5 — Déposer

Essayer dans l'ordre, s'arrêter au premier qui marche.

**`gh`, si `gh auth status` réussit :**

```bash
gh issue create --repo YoLaub/skills_stock --title "<titre>" --body-file <fichier> --label feedback
```

Écrire le corps dans un fichier temporaire plutôt que de le passer en argument inline —
un corps multi-lignes dans un argument shell est un champ de mines de quoting sur
chaque plateforme.

Si ça échoue sur le label (un non-collaborateur reçoit un `422` / "not have
permission"), réessayer la commande identique **sans** `--label`. C'est le chemin
attendu pour la plupart des utilisateurs, pas une erreur à signaler : le titre porte le
routage.

**Sinon, le navigateur.** Construire une URL pré-remplie contre le formulaire d'issue et
la donner à l'utilisateur — GitHub l'authentifie, et le formulaire applique lui-même les
labels selon ses droits. Lire `references/submitting.md` pour la forme de l'URL,
l'encodage, et la marche à suivre si le corps est trop long pour tenir dedans.

**Sinon, laisser sur disque.** Pas de compte GitHub : écrire le corps final dans un
fichier, donner le chemin plus `https://github.com/YoLaub/skills_stock/issues/new`, et
s'arrêter là.

## Étape 6 — Rendre compte

Donner l'URL de l'issue. Si c'est passé par le chemin navigateur, dire clairement que
rien n'est déposé tant que l'utilisateur n'a pas cliqué sur envoyer.
