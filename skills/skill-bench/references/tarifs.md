# Tarifs modèles — pour le coût observé

Snapshot au 2026-08-14 (prix Anthropic API first-party, $ par million de
tokens). **À revérifier périodiquement** — les tarifs évoluent, et un tarif de
lancement (Sonnet 5) expire à date fixe.

| Modèle | Input $/M | Output $/M |
|---|---|---|
| `claude-opus-5` | 5.00 | 25.00 |
| `claude-sonnet-5` | 3.00 (2.00 jusqu'au 2026-08-31) | 15.00 (10.00 jusqu'au 2026-08-31) |
| `claude-haiku-4-5` | 1.00 | 5.00 |

## Pourquoi c'est une estimation, pas une facture

Les notifications de sous-agent (`Agent`) renvoient un total de tokens
(`subagent_tokens`) sans distinguer input/output. Le coût réel dépend de ce
ratio, qui varie fortement selon la nature de la tâche (un juge qui relit un
long livrable = beaucoup d'input, peu d'output ; un rédacteur = l'inverse).

**Tarif mixte utilisé pour l'estimation** : moyenne pondérée 70% input / 30%
output (approximation raisonnable pour une tâche de lecture-analyse-rédaction
typique d'un agent de ce dépôt — pas une mesure, un ordre de grandeur) :

| Modèle | Tarif mixte estimé $/M tokens |
|---|---|
| `claude-opus-5` | 5.00×0.7 + 25.00×0.3 ≈ 11.00 |
| `claude-sonnet-5` (hors promo) | 3.00×0.7 + 15.00×0.3 ≈ 6.60 |
| `claude-sonnet-5` (promo jusqu'au 2026-08-31) | 2.00×0.7 + 10.00×0.3 ≈ 4.40 |
| `claude-haiku-4-5` | 1.00×0.7 + 5.00×0.3 ≈ 2.20 |

Formule : `coût_estimé = (tokens_observés / 1_000_000) × tarif_mixte(modèle)`.

Toujours présenter ce chiffre comme **estimation**, jamais comme un coût
facturé — le préciser explicitement dans le tableau de notation (Phase 6 du
skill).

## Modèle à utiliser par phase

- Phase 3 (exécution) : modèle par défaut de la session — généralement
  `claude-sonnet-5`, à confirmer si la session tourne sur autre chose.
- Phase 4 (jugement) : `claude-opus-5` (imposé par le skill).
