# Template — docs/02_architecture_ui.md

Conception visuelle et modèle de données. Rédigé après validation du document 01.
Fait le pont entre la vision produit et l'implémentation technique (document 03).

```markdown
# Conception Visuelle & Spécifications Écran par Écran

## 1. Maquette Visuelle : <écran le plus structurant>

<Image de maquette si elle existe (`![alt](./assets/...)`), sinon description textuelle
suffisamment précise pour qu'un développeur puisse la construire sans clarification.>

### Analyse des éléments clés de l'interface :
1. **<Zone de l'écran>** : <ce qu'elle affiche/permet>
2. **<Zone de l'écran>** : <ce qu'elle affiche/permet>
<...>

---

## 2. Structure des Données d'une <Entité Centrale> (Data Model)

<Le modèle de données de l'entité que le produit manipule le plus souvent — celle sur
laquelle repose la majorité des écrans. JSON annoté si le stockage est document-oriented,
sinon un schéma de champs équivalent.>

```json
{
  "id": "<exemple d'id>",
  "<champ_1>": "<type/exemple>",
  "<champ_2>": "<type/exemple>"
}
```

---

## 3. Plan de Découpage du Produit Minimum Viable (MVP)

### Phase 1 : <périmètre cœur>
* <ce qui doit fonctionner sans le reste>

### Phase 2 : <extension>
* <ce qui s'ajoute une fois la Phase 1 stable>

### Phase 3 : <extension>
* <...>
```

## Règles
- Le modèle de données ne couvre QUE l'entité centrale ici ; le détail complet des
  entités techniques (tables, DAO) va dans le document 03.
- Le découpage en phases MVP doit être cohérent avec les Epics du document 05 — les
  Epics sont l'implémentation GitHub de ce découpage, pas un découpage indépendant.
