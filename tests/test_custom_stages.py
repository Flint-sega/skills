#!/usr/bin/env python3
"""Свой набор стадий ранжируется порядком из state, а не встроенной восьмёркой.

Каноническое поведение ap.py покрыто tests/test_ap.py; здесь — одно расширение
foreman: stage set программы (чужие канону id) закрывается close_passed по
порядку state, а не отбрасывается фильтром константного ORDER.
"""

import importlib.util
import os
import pathlib
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
AP_PATH = str(REPO / "skills" / "foreman" / "tools" / "ap.py")
_spec = importlib.util.spec_from_file_location("ap", AP_PATH)
ap = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ap)


class OrderOfState(unittest.TestCase):
    def test_canonical_partial_stays_canonical(self):
        """Неполный канонический набор (резюм) — канон, не своя дорожка."""
        state = {"stages": [{"id": "preflight", "status": "done"},
                            {"id": "manifest", "status": "active"}]}
        self.assertEqual(ap.order_of(state), ap.ORDER)

    def test_foreign_ids_become_canon(self):
        """Чужой канону id — своя дорожка в порядке state."""
        state = {"stages": [{"id": "survey", "status": "active"},
                            {"id": "repair", "status": "active"},
                            {"id": "land", "status": "pending"}]}
        self.assertEqual(ap.order_of(state), ["survey", "repair", "land"])

    def test_reordered_canon_becomes_canon(self):
        """Канонические id в другом порядке — тоже своя дорожка."""
        state = {"stages": [{"id": "build", "status": "active"},
                            {"id": "spec", "status": "done"}]}
        self.assertEqual(ap.order_of(state), ["build", "spec"])

    def test_close_passed_closes_early_foreign_stage(self):
        """Ранняя своя стадия закрывается временем открытия поздней."""
        state = {"updatedAt": "2026-01-01T05:00:00+00:00",
                 "stages": [{"id": "survey", "status": "active",
                             "startedAt": "2026-01-01T01:00:00+00:00"},
                            {"id": "repair", "status": "active",
                             "startedAt": "2026-01-01T03:00:00+00:00"},
                            {"id": "land", "status": "pending"}]}
        closed = ap.close_passed(state)
        by_id = {s["id"]: s for s in state["stages"]}
        self.assertEqual(by_id["survey"]["status"], "done")
        self.assertEqual(by_id["survey"]["finishedAt"], "2026-01-01T03:00:00+00:00")
        self.assertEqual(by_id["repair"]["status"], "active")
        self.assertEqual(len(closed), 1)


if __name__ == "__main__":
    unittest.main()
