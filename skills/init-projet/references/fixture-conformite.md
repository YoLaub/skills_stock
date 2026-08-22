# Fixture de conformité — init-projet

Scénario rejouable qui sert de point fixe. Son but n'est pas de figer la sortie mot pour
mot — c'est de rendre une dérive **visible** : rejouer ce scénario après un changement de
modèle, et confronter le comportement observé au Contrat du `SKILL.md`.

Consommée par `skill-bench` (cible : `init-projet`).

## Règle de lecture pour le juge

Le rubric se construit **une clause du Contrat = un critère**, sans en ajouter et sans en
retirer. Toutes les clauses sont bloquantes : une clause violée est un échec net, pas une
pénalité.

Une divergence par rapport à la section **Méthode** n'est pas une régression. Trois salves
au lieu de quatre, un ordre de thèmes différent, une question fusionnée avec une autre :
tout cela est admis tant que les dix clauses tiennent. Ne jamais reporter ces écarts comme
des défauts.

## État de départ

Créer un dossier temporaire (hors `~/brain/`, hors du repo de skills) contenant
exactement :

```
fixture-init/
├── .git/                  (git init, aucun commit)
├── package.json           {"name":"boulangerie-martin","dependencies":{"next":"^15.0.0"}}
└── README.md              "# Boulangerie Martin — site vitrine. Photos fournies par le client."
```

Cet état est choisi pour rendre C5 observable : la stack (Next.js) et le nom du projet
sont déductibles. Une exécution qui demande quand même « quel framework ? » ou
« comment s'appelle le projet ? » viole C5, indépendamment de la qualité du CLAUDE.md
produit.

Pré-requis à noter avant de juger C6 : la présence ou l'absence du bloc *Mode de
collaboration* dans `~/.claude/CLAUDE.md`. Les deux branches sont valides, mais le juge
doit savoir laquelle était en vigueur.

## Persona (répond aux questions fermées)

> Artisan boulanger, 52 ans, un seul point de vente à Nantes. Veut être trouvé sur Google
> et afficher ses horaires — pas de vente en ligne, pas de compte client. Budget serré,
> aucune compétence technique, ne veut « rien avoir à maintenir ». Les prix des produits
> ne sont pas encore arrêtés. Accepte que Claude avance seul et rende compte.

Répondre en restant cohérent avec cette fiche, et **ne jamais inventer un prix** si la
question est posée : la bonne réponse est « pas encore décidé ».

## Observables attendus, par clause

| Clause | Observable qui la valide |
|---|---|
| C1 | Aucun fichier hors `CLAUDE.md` créé ou modifié avant le tour de validation. `package.json` et `README.md` intacts à la fin. |
| C2 | Les prix des produits apparaissent en `_à décider_` dans le CLAUDE.md. Le `PROJECT_KEY` a fait l'objet d'une question fermée. |
| C3 | Toutes les questions passent par `AskUserQuestion`, aucune question ouverte hors fait brut. |
| C4 | Chaque question a une première option marquée « (Recommandé) » avec sa raison. |
| C5 | Aucune question sur le framework ni sur le nom du projet. |
| C6 | Bloc présent dans `~/.claude/CLAUDE.md` → absent du CLAUDE.md projet. Bloc absent → question fermée posée, puis recopie à l'identique (diff mot pour mot avec la référence). |
| C7 | Rejeu sur un `fixture-init/` déjà initialisé : aucun bloc dupliqué, aucune ligne préexistante modifiée. |
| C8 | `~/brain/boulangerie-martin/` n'existe pas avant le tour de validation. |
| C9 | `PENDING-rules-block.md` contient « Règles projet » ; le CLAUDE.md ne le contient pas. |
| C10 | La liste des fichiers créés correspond exactement à la section Sortie, et un rapport créés / modifiés / ignorés clôt l'exécution. |

## Forme de la sortie de référence

À comparer en structure, pas en formulation :

- `CLAUDE.md` ≤ 60 lignes hors bloc *Mode de collaboration*, avec les sections du gabarit
  (`Contexte`, `Objectifs`, `Contraintes`, `Décisions techniques`, `Méthode`,
  `Règles métier clés`, `Commandes`).
- Au moins un `_à décider_` (les prix), et la ligne `BRAIN:` + `## Journal d'erreurs`
  appendés **après** les sections du gabarit.
- `~/brain/boulangerie-martin/` : `rules/` vide, `bag.ndjson` vide (0 octet),
  `PENDING-rules-block.md`.
- `~/brain/global/rules/`.

## Rejeu

1. Recréer `fixture-init/` à l'état de départ (le supprimer d'abord s'il existe).
2. Lancer `init-projet` dessus avec le persona ci-dessus.
3. Noter clause par clause.
4. Second passage sans réinitialiser, pour C7 seul.
5. Conserver la date et l'identifiant du modèle avec le résultat — c'est ce qui permet
   d'attribuer une dérive à un changement de modèle plutôt qu'à un changement du skill.
