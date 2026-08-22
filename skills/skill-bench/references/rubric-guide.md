# Guide de construction des rubrics

Un rubric mal construit note un style générique ("c'est bien écrit") au lieu
de l'objectif réel de la cible. Trois règles avant de pondérer quoi que ce
soit.

## 1. Le rubric vient du contrat déclaré, jamais d'une intuition

Chaque critère doit être traçable à une phrase précise du fichier cible :
- Une ligne d'`Inputs attendus` non respectée → critère "Respect des inputs".
- Une étape du `Processus` sautée → critère dédié à cette étape.
- Une règle bloquante explicite (ex. "ne jamais halluciner un besoin RH",
  "aucune slide rédigée avant validation du storyboard") → critère à poids
  fort, jamais un simple bonus — une règle bloquante violée est un échec net,
  pas une pénalité légère.

Si un critère ne peut pas être rattaché à une phrase du fichier cible, il ne
va pas dans le rubric — c'est un avis personnel sur le style, pas un test de
conformité.

### Cible dotée d'une section `## Contrat`

Certaines cibles séparent explicitement un **Contrat** (contraignant, versionné)
d'une **Méthode** (indicative). Dans ce cas le rubric ne se construit pas, il se
recopie : une clause du Contrat = un critère, toutes bloquantes, aucune ajoutée,
aucune retirée. Un rubric régénéré au jugement à chaque passage dérive autant que
ce qu'il est censé mesurer — c'est précisément ce que la section Contrat existe
pour empêcher.

Corollaire, aussi important : **un écart à la Méthode n'est pas un défaut.** Ordre
des étapes changé, étapes fusionnées, salves de questions regroupées autrement —
tout cela est admis tant que les clauses du Contrat tiennent, et ne doit jamais
apparaître dans les findings. Ne reporter un écart de méthode que s'il fait tomber
une clause, et alors le reporter sous cette clause.

Noter la version du Contrat (`v1`, `v2`…) dans le rapport : une note qui baisse à
version de contrat inchangée accuse le modèle ou le contexte, pas le skill.

## 2. Le critère "aval" n'est pas optionnel quand un consommateur existe

Repéré en Phase 1 du skill-bench. Formulation type :
```json
{
  "nom": "Exploitable par <consommateur>",
  "description": "Le livrable respecte le format attendu par <consommateur>.Inputs attendus, sans reformulation nécessaire",
  "poids": 3
}
```
Un livrable "beau" mais qui oblige le consommateur suivant à reformuler avant
de l'utiliser est un échec sur ce critère, même si tout le reste du rubric
est excellent — c'est précisément ce que `skill-bench` existe pour détecter,
un audit isolé du skill ne le voit pas.

## 3. Un critère par comportement observable, pas par qualité abstraite

Mauvais : "Pertinence" (poids 3) — personne ne sait ce qui ferait échouer ce
critère.
Bon : "Les compétences indispensables du besoin RH sont toutes couvertes ou
leur absence signalée explicitement" (poids 3) — un juge peut trancher sans
ambiguïté.

## Cas particulier : persona du scénario

Le champ `persona` du fichier eval décrit qui répond aux questions fermées
que la cible pose pendant son exécution (Phase 3 du skill-bench). Le rédiger
comme une fiche courte et cohérente :
```json
"persona": "Développeuse React 4 ans d'XP, cherche un poste lead technique
en remote, CV en français, budget non négociable en dessous de 55k."
```
Un persona vague ("un utilisateur normal") produit des réponses incohérentes
d'une question à l'autre pendant l'exécution — le sous-agent d'exécution doit
pouvoir répondre à toute question fermée sans inventer un nouveau trait de
personnage à chaque fois.

## Seuil de réussite par scénario

`seuil_succes` = 70% de `score_max` par défaut (aligné sur le seuil déjà
utilisé par `score_eval.py` de `skill-optimizer`). Remonter ce seuil (80-90%)
uniquement pour un critère bloquant explicite (ex. règle de non-hallucination)
où un score partiel n'a pas de sens — soit la règle est respectée, soit non.
