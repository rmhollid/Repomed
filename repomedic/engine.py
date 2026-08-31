from __future__ import annotations

import difflib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from google import genai


class RepairEngine:
    """A narrow, auditable repair agent for the contest demo."""

    def __init__(self) -> None:
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    @staticmethod
    def _run_tests(workspace: Path) -> dict[str, Any]:
        proc = subprocess.run(
            ["python", "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=workspace,
            text=True,
            capture_output=True,
            timeout=15,
        )
        return {
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "passed": proc.returncode == 0,
        }

    @staticmethod
    def _candidate_patches(source: str) -> list[dict[str, str]]:
        # Deliberately narrow demo tool: generate auditable single-token candidates.
        replacements = [
            ("return a * b", "return a / b"),
            ("return a * b", "return a + b"),
            ("return a * b", "return a - b"),
            ("return a * b", "return a // b"),
            ("return a * b", "return a % b"),
        ]
        candidates = []
        for old, new in replacements:
            if old not in source:
                continue
            candidate = source.replace(old, new, 1)
            diff = "\n".join(
                difflib.unified_diff(
                    source.splitlines(),
                    candidate.splitlines(),
                    fromfile="calculator.py",
                    tofile="calculator.py",
                    lineterm="",
                )
            )
            candidates.append({"replacement": new, "source": candidate, "diff": diff})
        return candidates

    def _ask_gemini(
        self,
        source: str,
        test_failure: str,
        candidates: list[dict[str, str]],
    ) -> dict[str, Any]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        compact = [
            {"index": i, "replacement": c["replacement"], "diff": c["diff"]}
            for i, c in enumerate(candidates)
        ]

        prompt = f"""
You are RepoMedic's repair decision agent.

A deterministic tool has:
1. run the repository tests,
2. captured the real failure,
3. generated a small set of auditable candidate patches.

Your job is to choose the candidate most directly supported by the tests.
Do not invent files or patches outside the supplied candidates.

SOURCE:
{source}

TEST FAILURE:
{test_failure}

CANDIDATES:
{json.dumps(compact, indent=2)}

Return ONLY a JSON object in exactly this form:
{{
  "candidate_index": 0,
  "diagnosis": "short diagnosis grounded in the test failure",
  "reason": "short reason this candidate should repair the defect"
}}
"""
        client = genai.Client(api_key=api_key)
        interaction = client.interactions.create(
            model=self.model_name,
            input=prompt,
            generation_config={"thinking_level": "low"},
        )
        text = interaction.output_text.strip()

        # Accept a JSON object even if a markdown fence slips through.
        match = re.search(r"\{.*\}", text, flags=re.S)
        if not match:
            raise RuntimeError(f"Gemini returned non-JSON output: {text[:500]}")
        data = json.loads(match.group(0))
        idx = int(data["candidate_index"])
        if idx < 0 or idx >= len(candidates):
            raise RuntimeError("Gemini selected an invalid candidate index.")
        return {
            "candidate_index": idx,
            "diagnosis": str(data.get("diagnosis", "")).strip(),
            "reason": str(data.get("reason", "")).strip(),
            "raw": text,
        }

    def run_demo(self) -> dict[str, Any]:
        package_root = Path(__file__).resolve().parents[1]
        demo_root = package_root / "demo_repo"

        with tempfile.TemporaryDirectory(prefix="repomedic-") as tmp:
            workspace = Path(tmp) / "repo"
            shutil.copytree(demo_root, workspace)

            source_path = workspace / "calculator.py"
            source = source_path.read_text(encoding="utf-8")

            before = self._run_tests(workspace)
            if before["passed"]:
                return {"ok": False, "error": "Demo repository is unexpectedly passing before repair."}

            candidates = self._candidate_patches(source)
            if not candidates:
                return {"ok": False, "error": "No candidate repairs were generated."}

            failure_text = (before["stdout"] + "\n" + before["stderr"]).strip()
            decision = self._ask_gemini(source, failure_text, candidates)
            chosen = candidates[decision["candidate_index"]]

            source_path.write_text(chosen["source"], encoding="utf-8")
            after = self._run_tests(workspace)

            return {
                "ok": after["passed"],
                "agent": {
                    "model": self.model_name,
                    "sdk": "Google GenAI SDK",
                    "decision": decision,
                },
                "actions": [
                    "Copied fresh broken demo repository into an isolated workspace.",
                    "Executed the repository's unit tests and captured the failure.",
                    f"Generated {len(candidates)} deterministic candidate patches.",
                    "Asked Gemini to select the candidate best supported by the evidence.",
                    "Applied only the selected candidate patch.",
                    "Re-executed the real unit tests.",
                ],
                "before": before,
                "patch": {
                    "replacement": chosen["replacement"],
                    "diff": chosen["diff"],
                },
                "after": after,
                "report": (
                    "Repair validated: failing tests now pass."
                    if after["passed"]
                    else "Repair attempted but validation still fails."
                ),
            }
