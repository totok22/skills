#!/usr/bin/env python3
"""Unit tests for check_fidelity.py."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import check_fidelity as cf  # noqa: E402


class TestCheckFidelity(unittest.TestCase):
    def test_unchanged_passes(self) -> None:
        self.assertEqual(cf.check_fidelity("The voltage is 5 V.", "The voltage is 5 V."), [])

    def test_number_drift_is_error(self) -> None:
        issues = cf.check_fidelity("The voltage was 5 V.", "The voltage was 6 V.")
        self.assertTrue(cf.has_errors(issues))

    def test_duplicate_number_drop_is_error(self) -> None:
        issues = cf.check_fidelity("5 V and 5 V", "5 V")
        self.assertTrue(cf.has_errors(issues))

    def test_allow_dedup_for_consolidating_rewrites(self) -> None:
        src = "CAN bus ran at 50 ms. Later note: CAN bus latency was 50 ms."
        ok = "The CAN bus maintained a 50 ms latency."
        missing_detail = "The CAN bus maintained low latency."
        fabricated = "The CAN bus maintained a 50 ms latency across 4 channels."
        self.assertEqual(cf.check_fidelity(src, ok, task="rewrite", protect=["CAN"], allow_dedup=True), [])
        self.assertTrue(
            cf.has_errors(cf.check_fidelity(src, missing_detail, task="rewrite", protect=["CAN"], allow_dedup=True))
        )
        self.assertTrue(
            cf.has_errors(cf.check_fidelity(src, fabricated, task="rewrite", protect=["CAN"], allow_dedup=True))
        )

    def test_unicode_minus_sign_preservation(self) -> None:
        self.assertEqual(cf.check_fidelity("−5 °C", "-5 °C"), [])
        self.assertTrue(cf.has_errors(cf.check_fidelity("−5 V", "5 V")))

    def test_scientific_notation(self) -> None:
        self.assertEqual(cf.check_fidelity("2.5 × 10^-4", "2.5×10^{-4}"), [])
        self.assertTrue(cf.has_errors(cf.check_fidelity("1e-3", "1e-4")))

    def test_cjk_adjacent_numbers_and_fullwidth(self) -> None:
        self.assertEqual(cf.check_fidelity("温度为４５°C", "温度为 45 °C"), [])
        self.assertTrue(cf.has_errors(cf.check_fidelity("温度为45°C", "温度为40°C")))

    def test_compound_units_and_exponents(self) -> None:
        self.assertEqual(
            cf.check_fidelity("Acceleration reached 9.8 m/s².", "Acceleration reached 9.8 m/s^2."),
            [],
        )
        issues = cf.check_fidelity("Energy density was 250 Wh/kg.", "Energy density was 250 kW/kg.")
        self.assertFalse(cf.has_errors(issues))
        self.assertTrue(cf.has_warnings(issues))

    def test_currency_not_misread_as_latex_math(self) -> None:
        src = "The budget rose from $5 million to $10 million."
        ok = "Funding increased from $5 million to $10 million."
        bad = "Funding increased from $5 million to $12 million."
        self.assertEqual(cf.check_fidelity(src, ok), [])
        self.assertTrue(cf.has_errors(cf.check_fidelity(src, bad)))

    def test_latex_math_and_citations(self) -> None:
        self.assertTrue(
            cf.has_errors(
                cf.check_fidelity(r"$P = UI$ \parencite{smith2020}", r"$P = I^2R$ \parencite{smith2020}")
            )
        )
        self.assertTrue(cf.has_errors(cf.check_fidelity(r"\cite{one}", r"\cite{two}")))
        self.assertEqual(
            cf.check_fidelity(r"See \cref{fig:1} and [@doe2024].", r"Refer to \cref{fig:1} and [@doe2024]."),
            [],
        )

    def test_markdown_link_url_preserved_when_anchor_translated(self) -> None:
        src = "详见[技术规范](https://example.com/spec/v2)."
        ok = "See the [technical specification](https://example.com/spec/v2)."
        bad = "See the [technical specification](https://example.com/spec/v3)."
        self.assertEqual(cf.check_fidelity(src, ok, task="translate"), [])
        self.assertTrue(cf.has_errors(cf.check_fidelity(src, bad, task="translate")))

    def test_protected_literals(self) -> None:
        self.assertTrue(cf.has_errors(cf.check_fidelity("CAN bus", "vehicle bus", protect=["CAN"])))
        self.assertEqual(cf.check_fidelity("CAN bus", "CAN network", protect=["CAN"]), [])

    def test_allow_change_normalizes_numbers_and_units(self) -> None:
        self.assertEqual(
            cf.check_fidelity(
                "Peak load was 1,000 N at 9.8 m/s².",
                "Peak load was 1,200 N at 10 m/s^2.",
                allow_change=["1,000", "1,200", "1,000 N", "1,200 N", "9.8", "10", "9.8 m/s²", "10 m/s^2"],
            ),
            [],
        )

    def test_draft_allows_subset_blocks_hallucinated_numbers(self) -> None:
        self.assertEqual(cf.check_fidelity("Notes: 5 V and 10 A.", "Voltage was 5 V.", task="draft"), [])
        self.assertTrue(
            cf.has_errors(cf.check_fidelity("Notes: 5 V.", "Voltage was 5 V across 12 samples.", task="draft"))
        )

    def test_translate_unchanged_is_error(self) -> None:
        issues = cf.check_fidelity("该接口仅用于诊断。", "该接口仅用于诊断。", task="translate")
        self.assertTrue(cf.has_errors(issues))

    def test_empty_candidate_is_error(self) -> None:
        self.assertTrue(cf.has_errors(cf.check_fidelity("Hello.", "   ")))

    def test_semantic_limitation_documented(self) -> None:
        self.assertEqual(cf.check_fidelity("A did not cause B.", "A caused B."), [])

    def test_cli_exit_codes_and_dedup_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            src = root / "src.md"
            ok = root / "ok.md"
            warn = root / "warn.md"
            fail = root / "fail.md"
            src.write_text("Voltage was 5 V. Repeated: 5 V.\n", encoding="utf-8")
            ok.write_text("The measured voltage was 5 V.\n", encoding="utf-8")
            warn.write_text("The measured voltage was 5 A.\n", encoding="utf-8")
            fail.write_text("The measured voltage was 6 V.\n", encoding="utf-8")

            script = str(SCRIPT_DIR / "check_fidelity.py")
            # Without --allow-dedup, dropping a duplicate fails.
            r_strict = subprocess.run([sys.executable, script, str(src), str(ok)], capture_output=True, text=True)
            self.assertEqual(r_strict.returncode, 2)

            # With --allow-dedup, consolidating duplicate 5 V passes.
            r_ok = subprocess.run(
                [sys.executable, script, str(src), str(ok), "--task", "rewrite", "--allow-dedup"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(r_ok.returncode, 0)
            self.assertEqual(json.loads(r_ok.stdout)["status"], "pass")

            r_warn = subprocess.run(
                [sys.executable, script, str(src), str(warn), "--allow-dedup", "--format", "text"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(r_warn.returncode, 1)
            self.assertIn("Status: warning", r_warn.stdout)

            r_fail = subprocess.run(
                [sys.executable, script, str(src), str(fail), "--allow-dedup"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(r_fail.returncode, 2)
            self.assertEqual(json.loads(r_fail.stdout)["status"], "fail")


if __name__ == "__main__":
    unittest.main()
