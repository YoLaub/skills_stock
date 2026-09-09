# Pièges connus

Append-only, sections datées. Un piège se note **au moment où il mord**, avec sa cause,
pas seulement son symptôme.

## 2026-09 — Refonte LOAR (React Native / Expo, FastAPI, SQLAlchemy async)

### Mobile

- **`fontWeight` + police personnalisée** — ignoré sur Android, retombe sur la Regular.
  Déclarer une famille par graisse.
- **Fichier d'attente à homonymes** — `screens/placeholders/index.tsx` exporte des noms
  identiques aux vrais écrans ; toute résolution par nom exporté attrape le stub.
- **Double inset** — poser un inset haut dans le conteneur partagé casse les écrans qui
  ont déjà leur propre zone sûre. Prévoir la coupure (`header={false}`), et un test
  symétrique dans les deux sens.
- **`as never` en double** — `navigate('x' as never, params as never)` compile en
  `[never, never]`. Ne caster que la route.
- **`Alert.prompt` est iOS-only** — sur Android il ne lève pas : il ne fait **rien**.
  Ni dialogue, ni erreur, ni journal. Un composant unique, pas un aiguillage par
  plateforme : deux chemins garantissent qu'un seul soit testé.
- **Un moteur de rendu de test ne met pas en page** — élongations et chevauchements ne
  sont visibles qu'à l'écran. Un `ScrollView` horizontal dans un conteneur flex prend la
  hauteur libre et étire ses enfants (`flexGrow: 0`).

### Backend / Python

- **`patch.multiple` ne rend pas ses mocks** dans son `as` quand on lui passe des valeurs
  explicites. Rencontré trois fois avant d'être extrait en utilitaire partagé — un piège
  qui revient trois fois est un outil manquant.
- **`round()` arrondit au pair** : `round(28.5)` → 28, `round(29.5)` → 30. Sur une donnée
  affichée, cette incohérence est pire que l'un ou l'autre choix.
- **`bool` est un `int`** : `True` passe pour `1` sans rejet explicite.
- **Élargir une colonne en nullable** réveille des bugs latents partout où elle était
  supposée présente. Passer le typeur avant de conclure.
- **`zoneinfo` n'est pas `pytz`** : `.replace(tzinfo=ZoneInfo(...))` donne le bon offset,
  là où `pytz` aurait posé un LMT historique. Une correction de fuseau ne corrompt pas
  forcément les données déjà écrites — le vérifier avant d'écrire une migration.
- **Un formateur qui reformate entre la lecture et l'écriture** fait échouer en silence
  toute édition par correspondance exacte. Relire le fichier réel après un formatage.

### Outillage et process

- **Tests conditionnés à un service** — une suite qui skippe faute de base démarrée
  paraît verte. 52 tests silencieux sur LOAR. Lire le couple (passés, **skippés**).
- **Fermeture automatique des issues** — elle ne joue que sur la branche par défaut du
  dépôt. Un flux qui merge vers `dev` laisse toutes les issues ouvertes malgré les
  « Closes #N ».
