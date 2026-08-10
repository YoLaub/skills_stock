# Template — docs/04_catalogue_items.md

Catalogue du contenu ou des unités fonctionnelles concrètes du MVP — utile quand le
produit est porté par un contenu structuré et répétitif (fiches, gabarits, recettes,
templates, cas d'usage...). **Si le produit n'a pas ce genre de contenu répétitif,
sauter ce document et le retirer de `docs/README.md`.**

```markdown
# Catalogue des <N> <Unités> du MVP - <Nom du Produit>

Ce document détaille la liste complète des <N> <unités> intégrées au lancement du MVP.

---

## 1. Répartition par Module

| Module | Nombre d'<unités> | Format |
| :--- | :--- | :--- |

---

## 2. Détail des <N> <Unités>

### <Emoji> Module A : <nom>

1. **<Nom de l'unité>**
   * *Description* : <une ligne>
   * *<Ce qu'elle requiert>* : <liste>
   * *<Ce qu'elle produit>* : <une ligne>

<Numérotation continue à travers tous les modules — c'est cette numérotation qui sert
de référence dans les critères d'acceptation du document 05.>
```

## Règles
- Chaque unité numérotée ici doit être traçable jusqu'à une User Story du document 05
  (au moins l'Epic « ingestion de contenu » doit les référencer toutes).
- Pas de détail d'implémentation (pas de JSON de structure ici — c'est le document 02
  qui porte le modèle de données générique appliqué à CHAQUE unité).
