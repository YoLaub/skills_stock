#!/usr/bin/env python3
"""
compare_bench_runs.py — Compare deux aggregate.json produits par
`skill-optimizer/scripts/score_eval.py --aggregate` (le même script que
skill-bench réutilise en Phase 5) et décide COMMIT/DISCUSSION/REVERT.

Usage:
    python compare_bench_runs.py --before agent-workspace/<slug>/bench-0/aggregate.json \
                                  --after  agent-workspace/<slug>/bench-1/aggregate.json

skill-bench écrase skill-bench/runs/<cible>/ à chaque exécution : archiver
son contenu dans agent-workspace/<slug>/bench-N/ après chaque run (voir
SKILL.md Phase 2 et Phase 4) avant d'appeler ce script.

Règle de décision (identique à skill-optimizer) :
- Delta positif ET aucun scénario en régression → COMMIT
- Delta positif MAIS régression sur au moins un scénario → DISCUSSION
- Delta nul ou négatif → REVERT
"""

import json
import argparse
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compare(before: dict, after: dict) -> dict:
    delta_pct = after["pct_global"] - before["pct_global"]

    before_map = {d["eval_id"]: d for d in before.get("details", [])}
    after_map = {d["eval_id"]: d for d in after.get("details", [])}

    regressions = []
    for eval_id, b in before_map.items():
        a = after_map.get(eval_id)
        if a and (a["pct"] < b["pct"] or (b["passed"] and not a["passed"])):
            regressions.append({"eval_id": eval_id, "avant": b["pct"], "apres": a["pct"]})

    still_failing = [d["eval_id"] for d in after.get("details", []) if not d.get("passed", True)]

    if delta_pct > 0 and not regressions and not still_failing:
        decision = "COMMIT"
    elif delta_pct > 0:
        decision = "DISCUSSION"
    else:
        decision = "REVERT"

    return {
        "avant": {"run": before.get("iteration", "?"), "pct": before["pct_global"]},
        "apres": {"run": after.get("iteration", "?"), "pct": after["pct_global"]},
        "delta_pct": round(delta_pct, 1),
        "regressions": regressions,
        "still_failing": still_failing,
        "decision": decision
    }


def print_result(result: dict):
    print("\n" + "═" * 50)
    print("  AGENT-OPTIMIZER — comparaison de runs skill-bench")
    print("═" * 50)
    print(f"  {result['avant']['run']} : {result['avant']['pct']}%")
    print(f"  {result['apres']['run']} : {result['apres']['pct']}%")
    print(f"  Delta : {result['delta_pct']:+.1f}%")
    if result["regressions"]:
        for r in result["regressions"]:
            print(f"  ⚠️  Scénario {r['eval_id']} régresse : {r['avant']}% → {r['apres']}%")
    if result["still_failing"]:
        print(f"  ⚠️  Scénario(s) encore en échec après édition : {result['still_failing']}")
    symbol = {"COMMIT": "✅", "DISCUSSION": "⚠️", "REVERT": "❌"}[result["decision"]]
    print(f"\n  {symbol} {result['decision']}")
    print("═" * 50 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    args = parser.parse_args()

    before = load(Path(args.before))
    after = load(Path(args.after))
    result = compare(before, after)
    print_result(result)

    out_path = Path(args.after).parent / "decision.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Décision sauvegardée : {out_path}")
