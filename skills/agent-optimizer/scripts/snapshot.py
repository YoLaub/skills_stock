#!/usr/bin/env python3
"""
snapshot.py — Sauvegarde une version d'un agent (agents/*.md) avant modification.

Usage:
    python snapshot.py snapshot --agent chemin/vers/agent.md --workspace agent-optimizer/agent-workspace/<slug>/ --iteration 0
    python snapshot.py diff --before .../iteration-0/ --after .../iteration-1/

Conserve le nom de fichier d'origine (un agent n'est jamais nommé SKILL.md,
contrairement au snapshot de skill-optimizer).
"""

import shutil
import json
import hashlib
import argparse
import difflib
from pathlib import Path
from datetime import datetime


def count_tokens_approx(text: str) -> int:
    return len(text) // 4


def snapshot_agent(agent_path: Path, workspace: Path, iteration: int) -> dict:
    iter_dir = workspace / f"iteration-{iteration}"
    iter_dir.mkdir(parents=True, exist_ok=True)

    dest = iter_dir / agent_path.name
    shutil.copy2(agent_path, dest)

    content = agent_path.read_text(encoding="utf-8")

    metadata = {
        "iteration": iteration,
        "source_path": str(agent_path),
        "snapshot_path": str(dest),
        "timestamp": datetime.now().isoformat(),
        "tokens_approx": count_tokens_approx(content),
        "content_hash": hashlib.md5(content.encode()).hexdigest()[:8],
        "lines": len(content.splitlines()),
        "modifications": []
    }

    (iter_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"✅ Snapshot créé : {dest}")
    print(f"   Tokens (approx) : {metadata['tokens_approx']}")
    print(f"   Lignes : {metadata['lines']}")

    return metadata


def diff_snapshots(iter_before: Path, iter_after: Path) -> str:
    before_files = list(iter_before.glob("*.md"))
    after_files = list(iter_after.glob("*.md"))

    if not before_files or not after_files:
        return "Fichiers snapshot manquants."

    before_lines = before_files[0].read_text(encoding="utf-8").splitlines()
    after_lines = after_files[0].read_text(encoding="utf-8").splitlines()

    diff = list(difflib.unified_diff(
        before_lines, after_lines,
        fromfile=f"{iter_before.name}/{before_files[0].name}",
        tofile=f"{iter_after.name}/{after_files[0].name}",
        lineterm=""
    ))

    return "\n".join(diff) if diff else "Aucune différence détectée."


def save_diff(iter_before: Path, iter_after: Path) -> Path:
    diff_text = diff_snapshots(iter_before, iter_after)

    before_meta = json.loads((iter_before / "metadata.json").read_text()) if (iter_before / "metadata.json").exists() else {}
    after_meta = json.loads((iter_after / "metadata.json").read_text()) if (iter_after / "metadata.json").exists() else {}

    before_tokens = before_meta.get("tokens_approx", "?")
    after_tokens = after_meta.get("tokens_approx", "?")
    modifications = after_meta.get("modifications", [])

    delta = (after_tokens - before_tokens) if isinstance(after_tokens, int) and isinstance(before_tokens, int) else "?"

    diff_md = f"# Diff — {iter_before.name} → {iter_after.name}\n\n"
    diff_md += f"**Tokens :** {before_tokens} → {after_tokens} ({'+' if isinstance(delta, int) and delta > 0 else ''}{delta})\n\n"
    diff_md += "## Micro-éditions appliquées\n\n"

    for i, mod in enumerate(modifications, 1):
        diff_md += f"### Micro-édition #{i}\n"
        diff_md += f"- **Zone :** {mod.get('zone', '?')}\n"
        diff_md += f"- **Type :** {mod.get('type', '?')}\n"
        diff_md += f"- **Anti-pattern visé :** {mod.get('anti_pattern', '?')}\n"
        diff_md += f"- **Motivation :** {mod.get('motivation', '?')}\n\n"

    diff_md += "\n## Diff brut\n\n```diff\n" + diff_text + "\n```\n"

    diff_path = iter_after / "diff.md"
    diff_path.write_text(diff_md, encoding="utf-8")
    print(f"📄 Diff sauvegardé : {diff_path}")
    return diff_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Snapshot et diff d'agents")
    subparsers = parser.add_subparsers(dest="command")

    snap_parser = subparsers.add_parser("snapshot")
    snap_parser.add_argument("--agent", required=True)
    snap_parser.add_argument("--workspace", required=True)
    snap_parser.add_argument("--iteration", type=int, required=True)

    diff_parser = subparsers.add_parser("diff")
    diff_parser.add_argument("--before", required=True)
    diff_parser.add_argument("--after", required=True)

    args = parser.parse_args()

    if args.command == "snapshot":
        snapshot_agent(Path(args.agent), Path(args.workspace), args.iteration)
    elif args.command == "diff":
        save_diff(Path(args.before), Path(args.after))
    else:
        parser.print_help()
