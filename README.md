# Pellet Math

The pellet grill honesty tool. The hopper hours on the box belong to a
windless 70 F afternoon. Pellet Math figures the burn from labeled
pounds-per-hour norms, lets the cold take its cut, and prices the cook
against the bag.

- Live app: https://ilanis-agent.github.io/pelletmath/app.html
- Landing: https://ilanis-agent.github.io/pelletmath/

## What it does

1. **Dial burn norm** - smoke sips about a pound an hour; a sear setting
   pours three and a half.
2. **Hopper hours** - hopper pounds divided by the burn norm, then the
   cold factor (x1.25 below 50 F, x1.5 below 30 F).
3. **Cook cost** - hours times the burn norm, priced against the bag.

## Files

- `engine.js` - pure functions (`burnPlan`, `hopperPlan`, `costPlan`) plus renderers
- `app.html` - the app; `index.html` - the landing page
- `oracle.py` - independent Python mirror of the engine
- `test.js` + `expected.json` - 25 oracle cases, `node test.js` runs green

Burn rates are labeled norms; your hopper keeps its own ledger.
