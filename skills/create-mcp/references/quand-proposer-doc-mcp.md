# Quand proposer un MCP doc chirurgical (vs un outil générique)

Généralisé depuis un cas réel (mcp_hermes, 2026-08) : construction d'un serveur MCP
local exposant la doc d'un produit (Hermes Agent) après discussion sur la pertinence
face à un outil générique (Context7). Ce fichier tranche cette décision — il précède
`phase-construction.md`, il ne le remplace pas.

## Étape 0 — vérifier avant de décider, jamais supposer

Ne jamais juger la couverture d'un outil générique de mémoire ou par intuition —
l'interroger réellement. Pour Context7, requête directe (pas besoin du MCP officiel
si WebFetch suffit) :

```
WebFetch https://context7.com/api/v1/search?query=<nom du produit>
```

Lire la liste de résultats et juger sur deux axes, pas un seul :

- **Existence** — le produit apparaît-il du tout ?
- **Précision** — l'entrée qui correspond couvre-t-elle bien *ce projet précis*, pas un
  homonyme ou un projet voisin ? Un nom générique fait remonter des dizaines d'entrées
  sans rapport (vu sur "Hermes" : ~30 résultats, du moteur JS React Native au relayer
  blockchain IBC, en passant par des projets tiers non-officiels du même nom). Trouver
  un résultat n'est pas trouver LE résultat — vérifier l'éditeur/l'URL source de
  l'entrée avant de conclure qu'elle correspond.

Si un résultat précis et non-ambigu existe avec une couverture réelle (nombre de
snippets significatif) → s'arrêter ici, utiliser Context7, ne pas construire. Sinon,
passer au test en 3 critères ci-dessous pour confirmer que construire vaut le coût.

## Le test en 3 critères

Un MCP doc dédié ne vaut le coût de construction/maintenance que si les **trois**
critères tiennent. Un seul manquant → utiliser l'outil générique, ne pas construire.

1. **Couverture faible ou ambiguë confirmée à l'étape 0.** Absence pure, ou collision
   de nommage qui empêche de cibler la bonne entrée sans connaître le slug exact à
   l'avance.
2. **Un export officiel propre existe.** `llms.txt` / `llms-full.txt` publié par le
   projet lui-même, ou équivalent (export markdown unique, à jour, maintenu par les
   auteurs). Sans ça, construire revient à scraper une doc HTML soi-même — fragile,
   hors du périmètre de ce skill, et le calcul coût/bénéfice bascule contre le MCP
   dédié.
3. **Contrainte réelle de dépendance tierce.** Self-hosted, air-gapped, pas d'appel
   réseau externe autorisé par la politique du client, ou besoin de fraîcheur
   contrôlée (re-sync à chaque démarrage plutôt que dépendre du calendrier de crawl
   d'un tiers). Sans cette contrainte, l'outil générique gagne sur le rapport
   effort/valeur — ne pas reconstruire une roue déjà bien faite pour un produit
   mainstream.

## Anti-pattern

Proposer ce pattern comme différenciateur générique ("on construit toujours notre
propre MCP doc") est une erreur : pour une lib mainstream déjà bien indexée par les
outils génériques, c'est du travail d'ingénierie pour un gain nul. Le test des 3
critères existe précisément pour éviter ce réflexe.

## Une fois les 3 critères validés

Basculer sur `phase-construction.md` — le MCP doc dédié se construit comme n'importe
quel serveur MCP de ce skill, avec la même prudence sur les couches de sécurité
pertinentes au contexte (typiquement : usage local mono-utilisateur en lecture seule
→ couches identité/OAuth/cloisonnement/rate-limit non pertinentes, seule
l'observabilité reste utile — voir `couches.md` pour la substance de chaque couche
avant de décider laquelle s'applique).
