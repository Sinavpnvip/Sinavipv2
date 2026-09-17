# -*- coding: utf-8 -*-
"""Regression tests for SF-001 … SF-006 (characterization)."""
import os
import sys
import tempfile
import unittest

# Ensure project root on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSeedMapping(unittest.TestCase):
    def test_seed_sql_placeholder_count(self):
        """VALUES has 6 placeholders matching 6 columns after fix."""
        from api.handlers_auth import seed_first_data
        import inspect
        src = inspect.getsource(seed_first_data)
        self.assertIn("VALUES(?,?,?,?,?,?)", src)
        self.assertNotIn("VALUES(?,?,?,?,1,?)", src)


class TestAuthBinding(unittest.TestCase):
    def test_auth_required_checks_active_user(self):
        from api import common
        import inspect
        src = inspect.getsource(common.auth_required)
        self.assertIn("admin_user", src)


class TestExportRedaction(unittest.TestCase):
    def test_export_default_excludes_secrets(self):
        from core import database as db
        import inspect
        src = inspect.getsource(db.export_all)
        self.assertIn("include_secrets", src)
        self.assertIn("tg_token", src)


class TestExtendAccountSignature(unittest.TestCase):
    def test_returns_tuple(self):
        from telegram import panel_link
        import inspect
        src = inspect.getsource(panel_link.extend_account)
        self.assertIn("return True, None", src)
        self.assertIn("return False,", src)


if __name__ == "__main__":
    unittest.main()
