# Tableau de notation — trio TDD (test/dev/ux-ui-strategy)

Passage : 2026-09-03. Mode léger — 1 scénario nominal par cible, exécution
`claude-sonnet-5` sandboxée, jugement `claude-opus-5`.

| Cible | Type | Scénarios passés | Score global | Tokens observés | Coût estimé | Verdict |
|---|---|---|---|---|---|---|
| `test-strategy` | skill-orchestrateur | 1/1 | 75 % | 107 600 | ~0.94 $ | Conforme |
| `dev-strategy` | skill-orchestrateur | 1/1 | 85 % | 105 900 | ~0.94 $ | Conforme |
| `ux-ui-strategy` | skill-orchestrateur | 1/1 | 100 % | 102 100 | ~0.90 $ | Conforme |

> Coût estimé, pas facturé — tarif mixte 70/30 input/output, voir
> `references/tarifs.md`. Coûts homogènes entre les 3 cibles, aucune n'est
> anormalement chère.

Verdict `Conforme` : `pct_global` ≥ 70 **et** tous les scénarios `passed: true`.

## Points relevés (n'entraînent pas "À corriger", mais à traiter)

1. **Désalignement de contrat test-strategy ↔ dev-strategy (structurel).**
   `dev-strategy` Étape 0 scanne `Strapi v5/tests/**/*.test.js` +
   `frontend/tests/e2e/**/*.spec.ts` pour les marqueurs RED, alors que
   `test-strategy` route désormais les tests unitaires **colocalisés**
   (`src/api/**/<module>.test.ts`, `.ts` pas `.js`). Un test RED unitaire
   généré au bon endroit serait **invisible** pour dev-strategy. Aucun marqueur
   `// RED` n'est non plus imposé par test-strategy. → corriger le glob + la
   convention de marqueur des deux côtés.

2. **test-strategy — sémantique RED ambiguë (75 %).** Le livrable annonce
   "code de prod intact" puis propose de poser un squelette de service pour
   faire basculer l'échec de `Cannot find module` vers l'assertion métier, et
   inclut un test "garde-fou" `passed` dans un lot déclaré RED. Le SKILL.md
   gagnerait à trancher : soit un squelette de structure est autorisé et c'est
   dit explicitement, soit non.

3. **dev-strategy — tension "superviseur ne code pas" (supervision 1.5/3).**
   Le livrable énonce la règle §1 de `supervision.md` puis écrit lui-même
   l'implémentation des 2 unités (Étape 5 "Proposition d'implémentation") et
   ajoute un "arbitrage honnête" qui rouvre la porte à l'inline. L'Étape 5 du
   SKILL.md ("Proposition d'implémentation") entre en tension avec le protocole
   de délégation — clarifier que l'Étape 5 est la validation globale post-merge,
   pas l'endroit où le superviseur code.

## Retour à l'usine

Aucune cible `À corriger`. Les 3 points ci-dessus sont des micro-ajustements de
formulation dans les SKILL.md (et un glob à corriger), pas un passage
`skill-optimizer` complet.
