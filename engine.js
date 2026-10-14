// Pellet math - pellet grill honesty.
// The hopper hours on the box belong to a windless 70 F afternoon. The burn
// rate is a labeled norm, and the cold eats from the same bag.
// Verdicts judge the unrounded figure; rounding is for display only.
var PelletMath = (function () {
  function pos(x) { return typeof x === "number" && isFinite(x) && x > 0; }
  function num(x) { return typeof x === "number" && isFinite(x); }
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }
  function money(x) { return r2(x).toFixed(2); }

  // Labeled norms: pounds per hour by dial.
  var RATES = { smoke: 1, "225": 1.5, "275": 2, "350": 2.5, sear: 3.5 };

  function burnPlan(setting) {
    if (!RATES[setting]) return { error: "pick a dial setting" };
    return { rate: RATES[setting] };
  }

  function renderBurn(r, setting) {
    return "Your " + setting + " dial figures about " + r.rate
      + " lb of pellets an hour - a labeled norm; the auger tells the truth by morning.";
  }

  function coldFactor(tempF) {
    if (tempF < 30) return 1.5;
    if (tempF < 50) return 1.25;
    return 1;
  }

  function hopperPlan(hopperLb, setting, tempF) {
    if (!pos(hopperLb)) return { error: "the hopper must be above zero" };
    if (!RATES[setting]) return { error: "pick a dial setting" };
    if (!num(tempF)) return { error: "the temperature must be a number" };
    var hours = hopperLb / (RATES[setting] * coldFactor(tempF));
    return { hours: r1(hours), cold: coldFactor(tempF) };
  }

  function renderHopper(r, hopperLb, setting, tempF) {
    var s = "Your " + hopperLb + " lb hopper at " + setting + " figures about " + r.hours + " hours";
    if (r.cold > 1) s += " on a " + tempF + " F evening - the cold eats from the same bag";
    return s + ".";
  }

  function costPlan(bagPrice, bagLb, hours, setting) {
    if (!pos(bagPrice) || !pos(bagLb) || !pos(hours)) return { error: "bag price, bag weight and hours must all be above zero" };
    if (!RATES[setting]) return { error: "pick a dial setting" };
    var burn = RATES[setting] * hours;
    var cost = burn / bagLb * bagPrice;
    return { burn: r1(burn), cost: r2(cost) };
  }

  function renderCost(r, bagPrice, bagLb, hours, setting) {
    return "Your " + hours + " hour cook at " + setting + " burns about " + r.burn + " lb - $"
      + money(r.cost) + " of a $" + money(bagPrice) + " bag, before the brisket.";
  }

  return {
    burnPlan: burnPlan, renderBurn: renderBurn,
    hopperPlan: hopperPlan, renderHopper: renderHopper,
    costPlan: costPlan, renderCost: renderCost
  };
})();
if (typeof module !== "undefined") module.exports = PelletMath;
