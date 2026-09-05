# Template — docs/05_github_backlog.md

Backlog agile prêt à être importé en Epics + Issues GitHub (Phase 2 du mode coder). Le
dernier document rédigé : il découpe les documents 01-04 en tickets exécutables.

```markdown
# Backlog GitHub : Epics & User Stories (Issues) - <Nom du Produit>

Ce document contient le découpage agile complet du projet, prêt à être importé sous
forme d'Epics et d'Issues (User Stories) dans GitHub Issues.

---

## 🗺️ Vue d'Ensemble des Epics

<Diagramme mermaid `graph TD` listant chaque Epic — dans l'ordre de dépendance
technique (ex. architecture core avant fonctionnalités qui en dépendent).>

---

## 📌 Epic <N> : <Nom de l'Epic>
> **Tag / Label** : `epic:<slug>`

### US-<N>.<M> : <Titre de la User Story>
* **Description** : En tant que <rôle>, je veux <action> afin de <bénéfice>.
* **Dépend de** : <aucune | US-<N>.<M>, US-<N>.<M> — issues dont la sienne a besoin pour démarrer>
* **Critères d'Acceptation** :
  * [ ] <critère vérifiable, testable>
  * [ ] <critère vérifiable, testable>
* **Labels** : `<label-domaine>`, `<label-type>`

<Une US par ticket exécutable en une PR — si une US ne tient pas dans une seule branche
+ une seule PR raisonnable, la découper en plusieurs US.>
```

## Règles
- Une US = une PR = une issue. Si en rédigeant une US elle appelle « et aussi », c'est
  déjà deux US.
- Les critères d'acceptation doivent être vérifiables mécaniquement (test, build, e2e) —
  pas des critères d'opinion (« doit être joli »).
- **Dépend de** doit lister les vraies dépendances techniques (fichiers/modules
  partagés, contrat de données), pas l'ordre de préférence — c'est ce champ qui permet
  à la Phase 3 du mode coder de détecter les issues parallélisables.
- L'ordre des Epics dans le diagramme = l'ordre d'exécution recommandé en Phase 3 du
  mode coder (dépendances techniques d'abord).
- Chaque Epic devient un milestone GitHub ; chaque US devient une issue rattachée à ce
  milestone (Phase 2 du mode coder) — le champ **Dépend de** devient une ligne
  `Depends on #<numéro>` dans le corps de l'issue GitHub correspondante.
