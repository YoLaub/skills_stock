# Corpus d'anti-patterns — définitions d'agents

Matériau de référence pour `agent-optimizer`. Chaque entrée est autonome : signal de détection, test de décision, correction, extrait avant/après. Cas source : `business-strategist` (agent de conseil en stratégie, ~450 lignes).

---

## 0. Préalable — agent ≠ skill

Trancher avant toute optimisation, les passes divergent ensuite.

| | Skill | Agent |
|---|---|---|
| Chargement | Métadonnées permanentes, corps à la demande, `references/` à la demande | Prompt injecté en entier au démarrage |
| Levier principal | `description` (déclenchement) + progressive disclosure | Densité du prompt + protocole d'entrée/sortie |
| Gain d'un split `references/` | Réel (contexte non chargé si non pertinent) | Nul si l'agent doit les lire de toute façon |
| Optimisation prioritaire | Précision de déclenchement | Élimination du contenu inerte |

Indices de mauvais classement dans le frontmatter : `emoji`, `color`, `vibe`, `tools`, `model` → définition d'agent. `name` + `description` seuls → skill.

**Cas source** : frontmatter `name/emoji/description/color/vibe` = agent. Le passer à un optimiseur de skills produit une version bien structurée d'un prompt qui hallucine toujours.

---

## 1. Principe directeur — le test de contrefactualité

> Une ligne mérite sa place si et seulement si le modèle se comporterait différemment sans elle.

Appliquer à chaque bloc. Trois issues :
- **Discriminante** → garder, densifier.
- **Redondante** (le modèle le fait déjà) → supprimer.
- **Décorative** (aucun effet observable possible) → supprimer.

C'est le filtre qui précède toutes les passes ci-dessous. Sur le cas source, il élimine seul ~60 % du volume.

---

## AP-01 — Mémoire fictive

**Signal** : `You remember:`, `You recall`, `Your memory contains`, `Based on prior sessions`, suivi d'une liste de contexte métier.

**Problème** : aucun mécanisme derrière. L'énoncé n'installe pas une capacité, il installe une *posture*. Le modèle joue l'agent-qui-sait et comble les trous par génération plausible. C'est un amplificateur des AP-02.

**Test** : existe-t-il un fichier, un outil ou une convention de chemin qui alimente réellement ce contenu ? Sinon → fictif.

**Correction** : remplacer la liste de « souvenirs » par un protocole de chargement explicite, ou par une porte d'intake (AP-09).

**Avant**
```
You remember:
- The organization's current business model, revenue streams, and cost structure
- The competitive landscape and key market dynamics
- Strategic priorities and initiatives currently in flight
- Decisions pending and the timeline for making them
```

**Après**
```
## Contexte

Tu ne conserves rien entre sessions. Au démarrage :
1. Cherche `strategy-context.md` à la racine du projet. S'il existe, lis-le.
2. Sinon, ouvre par la porte d'intake (§Intake) — ne produis aucune analyse avant.
Tout élément de contexte non trouvé et non fourni est un trou à signaler,
jamais à combler.
```

**Généralisation** : tout énoncé de capacité non adossé à un mécanisme (mémoire, accès réseau, exécution, perception) relève du même défaut. Chercher aussi `You have access to`, `You can observe`, `You monitor`.

---

## AP-02 — Quantification sans règle de provenance

**Signal** : le prompt exige des chiffres (`Quantify whenever possible`, gabarits `$[amount]`, `NPV`, `IRR`, `CAGR`, `Probability: [must sum to ~100%]`) sans une seule ligne sur l'origine des valeurs.

**Problème** : le défaut le plus dangereux de la catégorie. On ordonne au modèle de produire un artefact chiffré ; il en produit un, avec méthodologie plausible, source crédible et millésime cohérent. La sortie est indistinguable d'une analyse réelle.

**Test** : pour chaque emplacement chiffré du gabarit, le prompt indique-t-il d'où vient la valeur ? Sinon → défaut.

**Correction** : règle de provenance obligatoire + marquage typographique imposé. La règle doit précéder les gabarits dans l'ordre de lecture.

**Avant**
```
4. **Quantify whenever possible.** "Large market opportunity" is not strategy.
   "$4.2B TAM with 12% CAGR, and we can realistically capture 2-3% in 5 years"
   is strategy.
```

**Après**
```
4. **Quantifier, jamais fabriquer.** Tout nombre a exactement trois origines
   licites, et son origine est visible dans la sortie :
   - fourni par l'utilisateur → tel quel
   - issu d'une recherche → avec source et millésime
   - construit par toi → préfixé `[HYP]` + la formule de calcul + le point
     de sensibilité

   Un TAM sans `[HYP]` ni source est une faute. En l'absence de données,
   la sortie correcte est la *structure* du calcul avec ses entrées vides —
   pas une estimation d'illustration.
```

**Généralisation** : s'applique à toute production d'artefact à haute crédibilité apparente — citations, références bibliographiques, benchmarks, versions de bibliothèques, chiffres réglementaires, dates.

---

## AP-03 — Redondance canonique

**Signal** : reproduction in extenso de savoirs standards du domaine — ici Porter, SWOT, Business Model Canvas, BCG, Ansoff, 7-S, avec leurs gabarits complets.

**Problème** : ces contenus sont déjà dans les poids. Le coût en contexte est réel, l'apport marginal quasi nul. Pire, la présence du gabarit complet induit AP-04.

**Test** : demander la même chose au modèle sans le prompt. Si la sortie est équivalente → redondant.

**Correction** : ne garder que ce qui est non-évident — critères de *sélection* entre frameworks, pièges spécifiques, format de sortie attendu, conventions maison. Déplacer les gabarits en `references/` (skill) ou les réduire à une ligne de rappel (agent).

**Avant** : ~180 lignes de gabarits ASCII (Five Forces, Canvas, SWOT, scénarios, business case).

**Après**
```
## Choix du cadre

| Question posée | Cadre | Piège principal |
|---|---|---|
| Ce marché est-il attractif ? | Five Forces | Décrit l'industrie, pas ta position dedans |
| Pourquoi on gagne ? | Chaîne de valeur + moat | « on fait mieux » n'est pas un moat |
| Le modèle tient-il ? | Unit economics avant Canvas | Le Canvas masque une LTV:CAC cassée |
| Quoi faire face à l'incertitude ? | Scénarios 2×2 | Probabilités inventées → AP-02 |

Gabarits détaillés : `references/frameworks.md`. Ne les charger que si
l'analyse est effectivement produite, pas pour répondre à une question ponctuelle.
```

---

## AP-04 — Absence d'échelle de réponse

**Signal** : gabarits lourds présents, aucune règle disant quand les utiliser. Symptôme observable : une question simple déclenche un livrable en neuf sections.

**Problème** : en présence d'un gabarit, le modèle traite le gabarit comme la sortie par défaut. Le prompt devient un générateur de sur-livraison.

**Test** : simuler trois requêtes de tailles différentes. Si les trois produisent le même format → défaut.

**Correction** : échelle explicite en trois paliers, placée avant les gabarits.

**Après**
```
## Dimensionnement

| Entrée | Sortie |
|---|---|
| Question ponctuelle (« forfait ou TJM ? ») | 3-8 lignes, position tranchée, zéro cadre |
| Arbitrage cadré (2-3 options nommées) | Critères + recommandation + ce qu'on sacrifie |
| Décision structurante (engagement capital/pivot) | Cadre complet, après intake |

En cas de doute, prendre le palier inférieur et proposer de monter.
Jamais l'inverse.
```

---

## AP-05 — Règles en tension non arbitrée

**Signal** : deux directives applicables au même moment sans ordre de priorité.

**Cas source** : « ne jamais recommander avant d'avoir compris » (règle 2) + « minimum 3 options avant recommandation » (métrique) + « direct et opinionated, donne ton avis » (style). Le modèle arbitre au hasard selon la formulation de la question.

**Test** : construire une requête où deux règles pointent en sens opposé. Si le prompt ne tranche pas → défaut.

**Correction** : séquencer en phases nommées avec conditions de passage, plutôt que d'empiler des règles concurrentes.

**Après**
```
## Séquence

INTAKE → ANALYSE → RECOMMANDATION

Passage INTAKE → ANALYSE : modèle économique, question stratégique et
contraintes connus. Sinon, poser au plus 3 questions groupées.

Passage ANALYSE → RECOMMANDATION : ≥3 options réelles évaluées
(« ne rien faire » compte comme option).

En phase RECOMMANDATION, le style direct prime : une position, défendue,
avec le sacrifice explicite. La neutralité y est une faute.
En phase INTAKE et ANALYSE, il ne s'applique pas.
```

---

## AP-06 — Métriques décoratives

**Signal** : table `Success Metrics` / `Quality Bar` dont aucune ligne n'est vérifiable par l'agent lui-même pendant l'exécution.

**Problème** : consomme du contexte, ne change aucun comportement. Cas typique de contenu *décoratif* au sens du §1.

**Test** : l'agent peut-il, avant d'envoyer sa réponse, vérifier cette ligne ? Sinon → supprimer ou convertir.

**Correction** : convertir les lignes convertibles en checklist de sortie auto-vérifiable, supprimer le reste.

**Avant**
```
| Metric | Target |
|---|---|
| Strategic clarity | Every recommendation answers: where to compete, how to win |
| Executive communication | Recommendation fits on one page |
| Assumption documentation | Every analysis identifies and stress-tests its 3 key assumptions |
```

**Après**
```
## Avant d'envoyer

- [ ] Chaque nombre porte source ou `[HYP]`
- [ ] Le sacrifice est nommé (ce qu'on arrête de faire)
- [ ] Les 3 hypothèses de rupture sont listées, avec ce qui les invaliderait
- [ ] La recommandation tient avant l'analyse, pas après
```

---

## AP-07 — Persona-lore

**Signal** : biographie fictive, citation d'ouverture, `vibe`, énumération d'industries « traversées », ton épique.

**Cas source** : « You've worked across industries — technology, healthcare, financial services… helping startups find product-market fit » + exergue en tête de fichier + champ `vibe`.

**Problème** : coût en tokens à effet comportemental proche de zéro. Marginalement nuisible : la posture d'expertise vécue encourage l'assertion non sourcée (couplage avec AP-01/AP-02).

**Nuance** : le lore n'est pas toujours inerte. Il est *discriminant* quand il fixe un registre de sortie qui ne va pas de soi (voix narrative, ton de refus, niveau de familiarité). Conserver dans ce cas, en une ligne.

**Correction** : compresser en une phrase fonctionnelle décrivant le comportement, pas le CV.

**Avant** : 6 lignes de biographie + exergue + `vibe`.

**Après**
```
Registre : consultant senior. Tranche, ne présente pas les options à plat,
assume le désaccord. Langue claire, jamais le jargon de cabinet.
```

---

## AP-08 — Description non opérante

**Signal** : le champ `description` décrit la valeur de l'agent au lieu de spécifier ses conditions de déclenchement. Prose marketing, adjectifs, aucune exclusion.

**Problème** : sur un agent, la description pilote la délégation ; sur un skill, elle pilote le chargement. Une description sans frontière produit du sur-déclenchement (capté sur des tâches adjacentes) ou du sous-déclenchement (jamais choisi).

**Test** : la description permet-elle de répondre « non » à un cas voisin ? Sinon → défaut.

**Correction** : verbes de tâche + contextes déclencheurs + exclusions explicites.

**Avant**
```
description: Senior management consulting specialist for competitive analysis,
market entry strategy, business model design, growth planning, organizational
strategy, and strategic decision-making — translating complex market dynamics
into clear, actionable strategies that create sustainable competitive advantage
```

**Après**
```
description: Analyse concurrentielle, entrée sur un marché, conception de
business model, arbitrage d'allocation de ressources, dossier d'investissement.
Déclencher quand l'utilisateur pose une question d'arbitrage engageant des
ressources ou une position de marché. NE PAS déclencher pour : pricing tactique
d'une offre, rédaction commerciale, modélisation financière pure, choix
technique d'architecture.
```

---

## AP-09 — Absence de porte d'intake

**Signal** : l'agent est censé produire une analyse contextuelle mais rien ne définit le contexte minimal requis pour commencer.

**Problème** : conséquence directe d'AP-01 — si l'agent « se souvient », il n'a jamais besoin de demander. Sans porte, il produit une analyse générique habillée en analyse spécifique.

**Correction** : contexte minimal listé + comportement en cas d'absence + plafond de questions.

**Après**
```
## Intake

Minimum requis avant toute analyse :
- comment l'organisation gagne de l'argent aujourd'hui
- la décision précise à prendre, et sa date
- la contrainte dure (capital, temps, compétence, réglementation)

Manquant → poser au plus 3 questions, groupées, en un seul tour.
Refus de répondre → produire l'analyse en marquant chaque trou `[INCONNU]`
et en indiquant ce que sa résolution changerait. Ne jamais inventer le contexte.
```

---

## Grille de scoring

Noter 0-2 par axe. Total ≤ 10 sur 18 → réécriture de fond avant compression.

| Axe | 0 | 1 | 2 |
|---|---|---|---|
| Capacités déclarées réelles | mémoire/accès fictifs | ambigu | mécanisme explicite |
| Provenance des données | aucune règle | mention vague | règle + marquage imposé |
| Densité (contrefactualité) | >50 % redondant | mixte | chaque bloc discriminant |
| Dimensionnement | absent | implicite | échelle explicite |
| Cohérence des règles | contradictions | tensions mineures | séquencé |
| Vérifiabilité de sortie | métriques décoratives | partielle | checklist auto-vérifiable |
| Déclenchement | prose marketing | verbes de tâche | + exclusions |
| Porte d'entrée | absente | suggérée | contexte minimal + fallback |
| Ratio lore/comportement | >20 % lore | ~10 % | ≤1 ligne fonctionnelle |

---

## Ordre des passes

L'ordre n'est pas indifférent : compresser avant de corriger le fond produit une version dense et bien structurée d'un prompt qui ment toujours.

1. **Classer** — agent ou skill (§0).
2. **Fond** — AP-01, AP-02, AP-09. Ce sont les défauts qui produisent des sorties fausses.
3. **Contrôle** — AP-04, AP-05. Défauts qui produisent des sorties mal calibrées.
4. **Compression** — AP-03, AP-06, AP-07. Volume.
5. **Déclenchement** — AP-08, en dernier, sur le contenu stabilisé.
6. **Vérification** — rejouer 3 requêtes de tailles différentes, comparer avant/après.

---

## Ce que l'optimiseur ne décide pas seul

Remonter à l'utilisateur plutôt que trancher :

- la suppression d'une capacité déclarée qui pourrait correspondre à un mécanisme externe non visible dans le fichier
- le choix agent vs skill quand les deux sont défendables
- toute règle métier dont l'auteur pourrait avoir une raison non écrite
- les frontières d'exclusion de la `description` (dépendent des autres agents du parc, invisibles depuis un fichier isolé)

---

## Résultat sur le cas source

| | Avant | Après |
|---|---|---|
| Lignes | ~450 | ~110 + `references/frameworks.md` |
| Défauts de fond | 3 (AP-01, AP-02, AP-09) | 0 |
| Règles conservées telles quelles | — | 4 sur 10 (choix négatif, mauvaise nouvelle, moat défendable, faisabilité) |
| Règles ajoutées | — | 2 (provenance, dimensionnement) |

Les six règles supprimées relevaient du test de contrefactualité : le modèle les applique déjà sans qu'on les écrive.
