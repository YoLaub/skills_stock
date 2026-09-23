#!/usr/bin/env python3
"""Verification gates for the test/dev/ux-ui strategy skills.

A worker never decides that its own work is done. A phase opened by a skill can
only be closed by a PASS verdict issued by the matching verifier agent, on the
exact state of the working tree it inspected — or by an explicit escalation to
the user.

State lives in <project>/.claude/gates/<branch>/ (git-ignored):
  <phase>.open             phase in progress, not validated yet
  <phase>.json             last verdict (PASS/FAIL + fingerprint + report)
  <phase>.escalated.json   handed back to the user, not validated
  <phase>.forced.json      stop released after repeated blocks, not validated

Hook usage (stdin = Claude Code hook JSON):
  gate.py hook open <phase>[@path] ...   open phases (path: only if it exists)
  gate.py hook guard                     PreToolUse guard
  gate.py hook stop                      Stop guard

CLI usage (cwd = project):
  gate.py open <phase>
  gate.py verdict <phase> PASS|FAIL --report FILE [--scope PATH ...] [--lock FILE ...]
  gate.py escalate <phase> "<reason>"
  gate.py status
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Which verifier agent may issue each phase's verdict.
PHASE_JUDGES = {
    "coherence": "maquette-spec-coherence",
    "red": "spec-conformity-gate",
    "green": "spec-conformity-gate",
    "design": "design-fidelity-reviewer",
}
GATES_DIR = Path(".claude") / "gates"
MAX_CONSECUTIVE_BLOCKS = 3
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
# Shell fragments that can rewrite a file named on the same command line.
BASH_WRITE_PATTERN = re.compile(
    r"(>|\bsed\s+-i|\bperl\s+-[a-z]*i|\btee\b|\bmv\b|\brm\b|\bcp\b|\btruncate\b"
    r"|\bgit\s+(checkout|restore|reset|stash|rm|mv)\b)"
)


# -- git state ----------------------------------------------------------------

def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True).stdout.strip()


def project_root(cwd):
    return Path(git(cwd, "rev-parse", "--show-toplevel") or cwd)


def branch_dir(root):
    branch = git(root, "branch", "--show-current")
    if not branch:
        branch = "detached-" + git(root, "rev-parse", "--short", "HEAD")
    return root / GATES_DIR / branch.replace("/", "__")


def fingerprint(root, scope=None):
    """Hash of every tracked or untracked (non-ignored) file under scope.

    Covers uncommitted work, so any edit after a verdict makes it stale.
    """
    listed = git(root, "ls-files", "-co", "--exclude-standard", "--", *(scope or ["."]))
    digest = hashlib.sha256()
    for rel in sorted(set(listed.splitlines())):
        if rel.startswith(GATES_DIR.as_posix() + "/"):
            continue
        path = root / rel
        digest.update(rel.encode() + b"\0")
        digest.update(path.read_bytes() if path.is_file() else b"<deleted>")
    return digest.hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


# -- state files ----------------------------------------------------------------

def ensure_dir(root):
    d = branch_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    ignore = root / GATES_DIR / ".gitignore"
    if not ignore.exists():
        ignore.write_text("*\n")
    return d


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def locked_tests(root):
    red = read_json(branch_dir(root) / "red.json")
    if not red or red.get("verdict") != "PASS":
        return {}
    return red.get("locked", {})


def open_phase(root, phase):
    d = ensure_dir(root)
    (d / f"{phase}.open").write_text(now() + "\n")
    for stale in (f"{phase}.escalated.json", f"{phase}.forced.json"):
        (d / stale).unlink(missing_ok=True)


def phase_status(root, phase):
    """Return (ok, reason) for an open phase."""
    judge = PHASE_JUDGES[phase]
    v = read_json(branch_dir(root) / f"{phase}.json")
    if not v:
        return False, f"no verdict yet — run the `{judge}` agent"
    if v.get("verdict") != "PASS":
        return False, (f"last verdict is FAIL — send the worker back on the missing "
                       f"points, then run `{judge}` again")
    if v.get("fingerprint") != fingerprint(root, v.get("scope")):
        return False, f"PASS verdict is stale (files changed since) — run `{judge}` again"
    return True, "PASS"


# -- hook handlers --------------------------------------------------------------

def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    print(reason, file=sys.stderr)
    return 2


def agent_name(event):
    return (event.get("agent_type") or "").rsplit(":", 1)[-1]


def guard(event, root):
    tool = event.get("tool_name", "")
    tin = event.get("tool_input") or {}
    gates_abs = (root / GATES_DIR).resolve()
    locks = locked_tests(root)

    if tool in WRITE_TOOLS:
        target = Path(tin.get("file_path") or tin.get("notebook_path") or "")
        if not target.is_absolute():
            target = Path(event.get("cwd", root)) / target
        target = target.resolve()
        if target == gates_abs or gates_abs in target.parents:
            return deny("Gate state is written only through `gate.py verdict` by the verifier agent.")
        try:
            rel = target.relative_to(root.resolve()).as_posix()
        except ValueError:
            return 0
        if rel in locks:
            return deny(f"{rel} is locked by the RED verdict: the test is the truth, fix the "
                        "production code. Only the user can unlock it.")
        return 0

    if tool == "Bash":
        cmd = tin.get("command", "")
        match = re.search(r"gate\.py\s+(\w+)(?:\s+(\w+))?", cmd)
        if match and match.group(1) == "verdict":
            phase = match.group(2)
            judge = PHASE_JUDGES.get(phase)
            if agent_name(event) != judge:
                return deny(f"Only the `{judge}` agent may issue a `{phase}` verdict. "
                            "A worker never validates its own work.")
            return 0
        if match:
            return 0  # open / escalate / status are safe for anyone
        if GATES_DIR.as_posix() in cmd:
            return deny("Gate state is not edited by hand. Use `gate.py status` or `gate.py escalate`.")
        if locks and BASH_WRITE_PATTERN.search(cmd):
            touched = [p for p in locks if p in cmd]
            if touched:
                return deny(f"{', '.join(touched)} locked by the RED verdict — do not rewrite tests.")
    return 0


def stop(root):
    d = branch_dir(root)
    opened = sorted(p.name[:-len(".open")] for p in d.glob("*.open")) if d.is_dir() else []
    blocked = []
    for phase in opened:
        ok, reason = phase_status(root, phase)
        if ok:
            (d / f"{phase}.open").unlink()
        else:
            blocked.append((phase, reason))

    counter = d / ".stop-blocks"
    if not blocked:
        counter.unlink(missing_ok=True)
        return 0

    count = int(counter.read_text()) + 1 if counter.exists() else 1
    if count > MAX_CONSECUTIVE_BLOCKS:
        counter.unlink()
        for phase, reason in blocked:
            write_json(d / f"{phase}.forced.json", {"at": now(), "reason": reason})
            (d / f"{phase}.open").unlink()
        phases = ", ".join(p for p, _ in blocked)
        print(json.dumps({"systemMessage": (
            f"Gate released after {MAX_CONSECUTIVE_BLOCKS} blocks: {phases} NOT VALIDATED. "
            "Tell the user plainly that this work is not verified.")}))
        return 0

    counter.write_text(str(count))
    lines = [f"- {phase}: {reason}" for phase, reason in blocked]
    print("Work is not validated yet — a worker never declares its own work done.\n"
          + "\n".join(lines)
          + "\nIf you cannot get a PASS, hand it back to the user with "
          "`gate.py escalate <phase> \"<reason>\"` and say so in your answer.",
          file=sys.stderr)
    return 2


def run_hook(args):
    event = json.load(sys.stdin)
    root = project_root(event.get("cwd") or os.getcwd())
    if args.action == "open":
        for spec in args.phases:
            phase, _, cond = spec.partition("@")
            if phase not in PHASE_JUDGES:
                print(f"unknown phase {phase}", file=sys.stderr)
                return 1
            if not cond or (root / cond).exists():
                open_phase(root, phase)
        return 0
    if args.action == "guard":
        return guard(event, root)
    if args.action == "stop":
        return stop(root)
    return 1


# -- CLI ----------------------------------------------------------------------------

def cmd_verdict(args, root):
    report = Path(args.report)
    if not report.is_file():
        print(f"report not found: {report}", file=sys.stderr)
        return 1
    data = {"phase": args.phase, "verdict": args.verdict, "at": now(),
            "scope": args.scope or None,
            "report": report.read_text()}

    if args.phase == "red" and args.verdict == "PASS":
        if not args.lock:
            print("a RED PASS must --lock the test files it validated", file=sys.stderr)
            return 1
        data["locked"] = {p: file_hash(root / p) for p in args.lock}

    if args.verdict == "PASS":
        changed = [p for p, h in locked_tests(root).items() if file_hash(root / p) != h]
        if changed:
            print("locked tests changed since the RED verdict: " + ", ".join(changed)
                  + " — PASS refused", file=sys.stderr)
            return 1

    data["fingerprint"] = fingerprint(root, data["scope"])
    write_json(ensure_dir(root) / f"{args.phase}.json", data)
    print(f"{args.phase}: {args.verdict} recorded")
    return 0


def cmd_escalate(args, root):
    d = ensure_dir(root)
    write_json(d / f"{args.phase}.escalated.json", {"at": now(), "reason": args.reason})
    (d / f"{args.phase}.open").unlink(missing_ok=True)
    print(f"{args.phase}: escalated to the user — NOT VALIDATED")
    return 0


def cmd_status(root):
    d = branch_dir(root)
    for phase in PHASE_JUDGES:
        parts = []
        if (d / f"{phase}.open").exists():
            parts.append("open")
        if (d / f"{phase}.json").exists():
            parts.append(phase_status(root, phase)[1])
        for extra in ("escalated", "forced"):
            if (d / f"{phase}.{extra}.json").exists():
                parts.append(extra.upper())
        if parts:
            print(f"{phase}: " + " | ".join(parts))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("hook")
    h.add_argument("action", choices=["open", "guard", "stop"])
    h.add_argument("phases", nargs="*")

    o = sub.add_parser("open")
    o.add_argument("phase", choices=list(PHASE_JUDGES))

    v = sub.add_parser("verdict")
    v.add_argument("phase", choices=list(PHASE_JUDGES))
    v.add_argument("verdict", choices=["PASS", "FAIL"])
    v.add_argument("--report", required=True)
    v.add_argument("--scope", nargs="+")
    v.add_argument("--lock", nargs="+")

    e = sub.add_parser("escalate")
    e.add_argument("phase", choices=list(PHASE_JUDGES))
    e.add_argument("reason")

    sub.add_parser("status")

    args = parser.parse_args(argv)
    if args.cmd == "hook":
        return run_hook(args)
    root = project_root(os.getcwd())
    if args.cmd == "open":
        open_phase(root, args.phase)
        return 0
    if args.cmd == "verdict":
        return cmd_verdict(args, root)
    if args.cmd == "escalate":
        return cmd_escalate(args, root)
    return cmd_status(root)


if __name__ == "__main__":
    sys.exit(main())
