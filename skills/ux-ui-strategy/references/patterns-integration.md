# Patterns d'intégration ActivCreew

Fichier append-only : chaque nouveau pattern d'intégration (traduction maquette →
design system) ou piège rencontré s'ajoute ici, jamais dans SKILL.md. À lire à
l'étape 4 (intégration).

## Traduire un bouton de maquette

```tsx
// ❌ Recopie brute de la maquette (couleurs en dur, pas de composant)
<button class="w-full bg-brand-600 hover:bg-brand-700 text-white font-semibold py-3 rounded-lg">
  Faire un don de 5 &euro;/mois
</button>

// ✅ Traduit vers le design system, logique préservée
import { Button } from '@workspace/ui/components/shadcn/button';

<Button
  type="submit"
  size="lg"
  className="w-full"
  data-testid="don-submit"        // testid de la version dev-strategy préservé
  disabled={isPending}
  onClick={handleDonate}           // handler intact
>
  Faire un don de {amount}&nbsp;&euro;/mois
</Button>
```

## Traduire une carte / conteneur

```tsx
// ❌ <div class="bg-white rounded-2xl border border-gray-200 shadow-sm">
// ✅
import { Card, CardHeader, CardTitle, CardContent } from '@workspace/ui/components/shadcn/card';

<Card className="max-w-lg mx-auto">
  <CardHeader className="bg-primary text-primary-foreground">
    <CardTitle>Soutenez ActivCreew</CardTitle>
  </CardHeader>
  <CardContent>{/* ... */}</CardContent>
</Card>
```

## Décliner les états manquants de la maquette

```tsx
// La maquette ne montre que l'état nominal. Couvre le reste :
if (isLoading) return <DonationFormSkeleton />;       // nextjs-loading
if (error) return <DonationError onRetry={retry} />;   // état erreur
// + disabled pendant submit, état vide si liste, focus clavier
```

## Piège : entités HTML dans les strings JS

Ne JAMAIS mettre une entité HTML (`&nbsp;`, `&eacute;`) DANS une chaîne/template
literal JS (`` `Faire un don de ${x} €` ``) : elle s'afficherait littéralement. Là,
accents natifs + espace ASCII normal (un espace insécable littéral déclenche
`no-irregular-whitespace`). La règle entités-HTML ne vaut que pour le **texte JSX**,
pas pour les strings JS.
