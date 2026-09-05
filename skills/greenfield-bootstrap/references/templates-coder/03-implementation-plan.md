# Template — docs/03_implementation_plan.md

Plan d'implémentation technique. Rédigé après validation du document 02, à partir de la
salve de questions « stack technique & contraintes de plateforme ».

```markdown
# Plan d'Implémentation Technique - <Nom du Produit> (<cible : ex. Web, Mobile, CLI>)

Ce document définit l'architecture logicielle, la stack technique et les choix
d'ingénierie pour le développement de <Nom du Produit>.

---

## 1. Choix de la Stack Technique

<Pour chaque brique structurante : le choix, 1-2 avantages CONCRETS pour CE produit
(pas des généralités marketing). Chercher l'existant open source à imiter avant de
choisir — cf. Phase 1 du skill.>

* **<Domaine, ex. Langage & UI>** : **<choix>**
  * *Avantages* : <pourquoi ce choix précisément pour ce produit>
* **<Domaine, ex. Stockage>** : **<choix>**
  * *Avantages* : <...>

---

## 2. Architecture Logicielle

<Diagramme mermaid `graph TD` : couches (UI → domaine/use-cases → données) et leurs
dépendances. Doit rester cohérent avec la règle du skill : logique métier = service
unique consommé par UI ET interfaces machine.>

---

## 3. Structure du Projet

<Arborescence des dossiers clés, commentée en une ligne par dossier — assez pour que
Phase 2 (bootstrap) du skill s'en serve directement.>

```
<racine>/
├── <domaine>/
│   ├── <sous-dossier>/   # <rôle>
```

---

## 4. Matrice de Capacités / Contraintes

<Tableau si le choix natif vs alternative (ex. PWA, low-code) a des conséquences
mesurables — sinon supprimer la section.>

| Fonctionnalité | Choix technique | Avantage par rapport à l'alternative écartée |
| :--- | :--- | :--- |
```

## Règles
- Chaque choix de stack doit répondre à une contrainte énoncée dans le document 01 ou
  02 (offline, latence, plateforme...) — pas de choix par défaut non justifié.
- La structure du projet (section 3) est ce que la Phase 2 « Bootstrap » du skill
  parent va créer : elle doit être assez précise pour ne nécessiter aucune question
  supplémentaire au bootstrap.
