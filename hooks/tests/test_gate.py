"""Tests for hooks/gate.py — run with: python3 -m unittest discover hooks/tests"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parents[1] / "gate.py"


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class GateTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        git(self.repo, "init", "-q", "-b", "feat/don")
        git(self.repo, "config", "user.email", "t@t")
        git(self.repo, "config", "user.name", "t")
        self.write("src/don.ts", "export const x = 1\n")
        self.write("tests/don.test.js", "test('red', () => expect(1).toBe(2))\n")
        self.write("docs/maquettes/don.html", "<button>Donner</button>\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "init")

    def tearDown(self):
        self._tmp.cleanup()

    # -- helpers ---------------------------------------------------------
    def write(self, rel, content):
        p = self.repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return p

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, str(GATE), *args],
            cwd=self.repo, capture_output=True, text=True,
        )

    def hook(self, *args, payload=None):
        data = {"cwd": str(self.repo), "session_id": "s"}
        data.update(payload or {})
        return subprocess.run(
            [sys.executable, str(GATE), "hook", *args],
            cwd=self.repo, input=json.dumps(data), capture_output=True, text=True,
        )

    def pre_tool(self, tool_name, tool_input, agent_type=None):
        payload = {"hook_event_name": "PreToolUse", "tool_name": tool_name,
                   "tool_input": tool_input}
        if agent_type:
            payload["agent_type"] = agent_type
            payload["agent_id"] = "a1"
        return self.hook("guard", payload=payload)

    def assertDenied(self, result):
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def assertAllowed(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn('"deny"', result.stdout)

    def report(self, text="criterion 1: covered"):
        return str(self.write("report.md", text))

    def gate_dir(self):
        return self.repo / ".claude" / "gates" / "feat__don"


class OpenTests(GateTestCase):
    def test_hook_open_creates_marker_and_gitignore(self):
        r = self.hook("open", "green")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue((self.gate_dir() / "green.open").exists())
        self.assertEqual((self.repo / ".claude/gates/.gitignore").read_text().strip(), "*")

    def test_conditional_phase_opens_only_when_path_exists(self):
        self.hook("open", "red", "coherence@docs/maquettes", "design@docs/absent")
        self.assertTrue((self.gate_dir() / "red.open").exists())
        self.assertTrue((self.gate_dir() / "coherence.open").exists())
        self.assertFalse((self.gate_dir() / "design.open").exists())

    def test_unknown_phase_is_rejected(self):
        self.assertNotEqual(self.cli("open", "whatever").returncode, 0)


class StopTests(GateTestCase):
    def stop(self):
        return self.hook("stop", payload={"hook_event_name": "Stop"})

    def test_no_open_phase_lets_stop_through(self):
        self.assertEqual(self.stop().returncode, 0)

    def test_open_phase_without_verdict_blocks_stop(self):
        self.cli("open", "green")
        r = self.stop()
        self.assertEqual(r.returncode, 2)
        self.assertIn("green", r.stderr)
        self.assertIn("spec-conformity-gate", r.stderr)

    def test_pass_verdict_on_current_state_releases_and_closes_phase(self):
        self.cli("open", "green")
        self.assertEqual(self.cli("verdict", "green", "PASS", "--report", self.report()).returncode, 0)
        self.assertEqual(self.stop().returncode, 0)
        self.assertFalse((self.gate_dir() / "green.open").exists())

    def test_pass_verdict_is_stale_after_code_changes(self):
        self.cli("open", "green")
        self.cli("verdict", "green", "PASS", "--report", self.report())
        self.write("src/don.ts", "export const x = 2\n")
        r = self.stop()
        self.assertEqual(r.returncode, 2)
        self.assertIn("stale", r.stderr.lower())

    def test_untracked_new_file_also_makes_verdict_stale(self):
        self.cli("open", "green")
        self.cli("verdict", "green", "PASS", "--report", self.report())
        self.write("src/extra.ts", "export {}\n")
        self.assertEqual(self.stop().returncode, 2)

    def test_fail_verdict_keeps_blocking(self):
        self.cli("open", "green")
        self.cli("verdict", "green", "FAIL", "--report", self.report("criterion 2: absent"))
        r = self.stop()
        self.assertEqual(r.returncode, 2)
        self.assertIn("FAIL", r.stderr)

    def test_scoped_verdict_ignores_changes_outside_scope(self):
        self.cli("open", "coherence")
        self.cli("verdict", "coherence", "PASS", "--report", self.report(),
                 "--scope", "docs")
        self.write("src/don.ts", "export const x = 3\n")
        self.assertEqual(self.stop().returncode, 0)

    def test_scoped_verdict_goes_stale_when_scope_changes(self):
        self.cli("open", "coherence")
        self.cli("verdict", "coherence", "PASS", "--report", self.report(), "--scope", "docs")
        self.write("docs/maquettes/don.html", "<button>Soutenir</button>\n")
        self.assertEqual(self.stop().returncode, 2)

    def test_escalation_releases_stop_and_is_recorded(self):
        self.cli("open", "design")
        self.assertEqual(self.cli("escalate", "design", "maquette ambiguë").returncode, 0)
        self.assertEqual(self.stop().returncode, 0)
        esc = json.loads((self.gate_dir() / "design.escalated.json").read_text())
        self.assertEqual(esc["reason"], "maquette ambiguë")

    def test_repeated_blocks_end_in_forced_release_to_avoid_loop(self):
        self.cli("open", "green")
        results = [self.stop() for _ in range(4)]
        self.assertEqual([r.returncode for r in results[:3]], [2, 2, 2])
        self.assertEqual(results[3].returncode, 0)
        self.assertIn("NOT VALIDATED", results[3].stdout)
        self.assertTrue((self.gate_dir() / "green.forced.json").exists())

    def test_block_counter_resets_after_a_release(self):
        self.cli("open", "green")
        self.stop(); self.stop()
        self.cli("verdict", "green", "PASS", "--report", self.report())
        self.assertEqual(self.stop().returncode, 0)
        self.cli("open", "green")
        self.write("src/don.ts", "export const x = 4\n")  # new work, verdict now stale
        self.assertEqual([self.stop().returncode for _ in range(3)], [2, 2, 2])

    def test_other_branch_phases_do_not_block(self):
        self.cli("open", "green")
        git(self.repo, "switch", "-q", "-c", "other")
        self.assertEqual(self.stop().returncode, 0)


class VerdictTests(GateTestCase):
    def test_red_pass_requires_locked_tests(self):
        self.assertNotEqual(self.cli("verdict", "red", "PASS", "--report", self.report()).returncode, 0)
        ok = self.cli("verdict", "red", "PASS", "--report", self.report(),
                      "--lock", "tests/don.test.js")
        self.assertEqual(ok.returncode, 0, ok.stderr)

    def test_green_pass_refused_when_a_locked_test_changed(self):
        self.cli("verdict", "red", "PASS", "--report", self.report(), "--lock", "tests/don.test.js")
        self.write("tests/don.test.js", "test('red', () => expect(1).toBe(1))\n")
        r = self.cli("verdict", "green", "PASS", "--report", self.report())
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("tests/don.test.js", r.stderr)

    def test_verdict_requires_existing_report(self):
        self.assertNotEqual(self.cli("verdict", "green", "PASS", "--report", "nope.md").returncode, 0)

    def test_report_can_come_from_stdin(self):
        r = subprocess.run([sys.executable, str(GATE), "verdict", "green", "FAIL", "--report", "-"],
                           cwd=self.repo, input="CA-002 partiel", capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("CA-002 partiel", json.loads((self.gate_dir() / "green.json").read_text())["report"])

    def test_empty_report_is_refused(self):
        r = subprocess.run([sys.executable, str(GATE), "verdict", "green", "PASS", "--report", "-"],
                           cwd=self.repo, input="  \n", capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)

    def test_verdict_stores_report_content(self):
        self.cli("verdict", "green", "FAIL", "--report", self.report("CA-001 absent"))
        v = json.loads((self.gate_dir() / "green.json").read_text())
        self.assertEqual(v["verdict"], "FAIL")
        self.assertIn("CA-001 absent", v["report"])


class GuardTests(GateTestCase):
    def lock_red(self):
        self.cli("verdict", "red", "PASS", "--report", self.report(), "--lock", "tests/don.test.js")

    # locked tests ------------------------------------------------------
    def test_edit_of_locked_test_is_denied(self):
        self.lock_red()
        self.assertDenied(self.pre_tool("Edit", {"file_path": str(self.repo / "tests/don.test.js")}))

    def test_edit_of_unlocked_file_is_allowed(self):
        self.lock_red()
        self.assertAllowed(self.pre_tool("Edit", {"file_path": str(self.repo / "src/don.ts")}))

    def test_nothing_locked_before_red_verdict(self):
        self.assertAllowed(self.pre_tool("Write", {"file_path": str(self.repo / "tests/don.test.js")}))

    def test_bash_rewrite_of_locked_test_is_denied(self):
        self.lock_red()
        self.assertDenied(self.pre_tool("Bash", {"command": "sed -i '' s/2/1/ tests/don.test.js"}))
        self.assertDenied(self.pre_tool("Bash", {"command": "git checkout -- tests/don.test.js"}))

    def test_running_a_locked_test_is_allowed(self):
        self.lock_red()
        self.assertAllowed(self.pre_tool("Bash", {"command": "yarn test tests/don.test.js"}))

    # verdict files -------------------------------------------------------
    def test_direct_write_into_gates_dir_is_denied_even_for_gate_agent(self):
        path = str(self.gate_dir() / "green.json")
        self.assertDenied(self.pre_tool("Write", {"file_path": path}))
        self.assertDenied(self.pre_tool("Write", {"file_path": path}, agent_type="yls:spec-conformity-gate"))

    def test_bash_touching_gates_dir_is_denied(self):
        self.assertDenied(self.pre_tool("Bash", {"command": "rm -rf .claude/gates"}))

    def test_verdict_command_denied_for_worker_or_lead(self):
        cmd = f"python3 {GATE} verdict green PASS --report r.md"
        self.assertDenied(self.pre_tool("Bash", {"command": cmd}))
        self.assertDenied(self.pre_tool("Bash", {"command": cmd}, agent_type="general-purpose"))

    def test_verdict_command_allowed_for_matching_gate_agent(self):
        cmd = f"python3 {GATE} verdict green PASS --report r.md"
        self.assertAllowed(self.pre_tool("Bash", {"command": cmd}, agent_type="yls:spec-conformity-gate"))
        self.assertAllowed(self.pre_tool("Bash", {"command": cmd}, agent_type="spec-conformity-gate"))

    def test_gate_agent_cannot_issue_another_phase_verdict(self):
        cmd = f"python3 {GATE} verdict design PASS --report r.md"
        self.assertDenied(self.pre_tool("Bash", {"command": cmd}, agent_type="spec-conformity-gate"))
        self.assertAllowed(self.pre_tool("Bash", {"command": cmd}, agent_type="design-fidelity-reviewer"))

    def test_status_and_escalate_are_allowed_for_anyone(self):
        self.assertAllowed(self.pre_tool("Bash", {"command": f"python3 {GATE} status"}))
        self.assertAllowed(self.pre_tool("Bash", {"command": f"python3 {GATE} escalate green 'blocked'"}))

    # counter-example -----------------------------------------------------
    def test_ordinary_tool_calls_pass_through(self):
        self.assertAllowed(self.pre_tool("Read", {"file_path": str(self.repo / "tests/don.test.js")}))
        self.assertAllowed(self.pre_tool("Bash", {"command": "git status"}))


if __name__ == "__main__":
    unittest.main()
