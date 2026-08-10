# Déposer sans `gh`

À lire seulement si `gh auth status` a échoué. Le chemin navigateur fonctionne pour
n'importe qui a un compte GitHub sans avoir le CLI : GitHub s'occupe de
l'authentification, et le formulaire d'issue applique ses propres labels quels que
soient les droits de l'utilisateur sur le dépôt.

## L'URL pré-remplie

Base :

```
https://github.com/YoLaub/skills_stock/issues/new
```

Forme préférée — cibler le template d'issue et remplir ses champs par `id` :

| Param | Remplit |
|---|---|
| `template=feedback.yml` | sélectionne le formulaire (requis pour que les params de champs se lient) |
| `title` | le titre de l'issue |
| `skill` | quel skill est concerné |
| `verbatim` | les mots cités de l'utilisateur |
| `context` | le bloc de contexte, omis entièrement si l'utilisateur l'a refusé |
| `version` | ligne plugin / environnement |

```
https://github.com/YoLaub/skills_stock/issues/new?template=feedback.yml&title=…&skill=…&verbatim=…&context=…
```

Les noms de champ qui ne correspondent à aucun `id` de `.github/ISSUE_TEMPLATE/feedback.yml`
sont ignorés silencieusement — le formulaire s'ouvre quand même, juste vide. Si un
param arrête de se lier, vérifier les ids du template avant de réécrire l'URL.

Repli, en contournant le template (les issues vierges sont activées, donc ça résout
toujours) :

```
https://github.com/YoLaub/skills_stock/issues/new?title=…&body=…
```

## Encodage

Encoder chaque valeur en percent-encoding. Les caractères qui tronquent ou corrompent
silencieusement un corps :

| Caractère | Encodage |
|---|---|
| retour à la ligne | `%0A` |
| espace | `%20` |
| `#` | `%23` |
| `&` | `%26` |
| `+` | `%2B` |
| `/` | `%2F` |
| `?` | `%3F` |

Les fences markdown, backticks et marqueurs de citation `>` passent bien tels quels —
les encoder quand même si l'URL est construite à la main plutôt qu'avec un encodeur.

## Longueur

Garder l'URL encodée entière sous ~6000 caractères. Le plafond dur est autour de 8 Ko
(navigateur et serveur), et l'encodage gonfle un corps plein de retours à la ligne et
de ponctuation d'environ moitié — un corps brut de plus de ~3500 caractères est déjà à
risque. L'échec est moche : un corps tronqué, ou un `414` qui a l'air d'un lien cassé.

Quand ça ne tient pas, dans l'ordre :

1. Retirer le param `context` et garder la citation — c'est toujours elle qui devait
   survivre en priorité.
2. Toujours trop long : écrire le corps complet dans un fichier, ouvrir l'URL simple
   `issues/new?title=…` avec juste le titre, et dire à l'utilisateur de coller le
   contenu du fichier dans le champ.

## Passer la main

Afficher l'URL et laisser l'utilisateur cliquer. Ne pas lancer `open` / `xdg-open` /
`start` soi-même — ouvrir un onglet de navigateur est une action visible de
l'extérieur, et le but de l'étape 4 était que l'utilisateur décide quand ça devient
public.

Dire explicitement que l'issue n'est pas déposée tant que l'envoi n'a pas été cliqué.
Un formulaire pré-rempli ressemble assez à une issue postée pour que des gens ferment
l'onglet en croyant avoir terminé.
