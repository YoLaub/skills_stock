# Template — docs/01_concept.md

Cadre de projet. Rédigé après la salve de questions « vision produit » et « piliers
fonctionnels ». Une seule lecture doit suffire à comprendre ce que fait le produit et
pour qui, sans détail technique (ça, c'est le document 03).

```markdown
# Cadre de Projet : <Nom du Produit> - <accroche en une ligne>

## 1. Vision & Positionnement du Produit

<Ce qu'est le produit en 2-3 phrases : à qui il s'adresse, quel problème n°1 il résout,
ce qui le différencie d'une alternative évidente.>

### Direction Graphique & UX (si le produit a une identité visuelle forte)
* **Esthétique** : <référence(s) visuelle(s) explicites, pas un adjectif vague>
* **Palette** : <couleurs clés et pourquoi, ex. contrainte de lisibilité/accessibilité>
* **Typographie & Icônes** : <choix et raison>
* **Ergonomie** : <règle d'usage n°1, ex. nombre de taps pour l'action critique>

---

## 2. Piliers Fonctionnels & Modules Principaux

<Diagramme mermaid `graph TD` : le produit au sommet, un nœud par pilier/module,
un niveau de détail (fonctions clés) par pilier.>

### Module 1 : <nom>
* <fonction clé> : <une ligne>
* <fonction clé> : <une ligne>

<Un sous-titre par module, dans l'ordre du diagramme.>

---

## 3. Architecture Technique & Stratégie <si applicable : hybride / multi-mode>

<Tableau comparatif si le produit a plusieurs modes de fonctionnement structurants
(ex. connecté/déconnecté, gratuit/payant, mobile/desktop) — sinon supprimer la section.>

| Composant | <Mode A> | <Mode B> |
| :--- | :--- | :--- |
| <capacité clé> | <comportement> | <comportement> |

---

## 4. Spécifications UI/UX des Écrans Principaux

<Liste numérotée des écrans/vues structurants — une ligne de description chacun, assez
pour cadrer le document 02 (maquettes) sans le dupliquer.>
```

## Règles
- Rester au niveau produit : aucune mention de framework, de librairie ou de schéma de
  base de données ici (→ document 03).
- Le diagramme mermaid doit tenir en un écran ; s'il déborde, le produit a trop de
  piliers pour un MVP — le signaler à l'utilisateur avant de continuer.
