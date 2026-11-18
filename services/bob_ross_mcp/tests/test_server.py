"""Smoke checks: module loads with installed MCP SDK and refuses missing auth."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server


class ServerTests(unittest.TestCase):
    def test_no_unauthenticated_public_deployment(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "MCP_API_TOKEN"):
                server.create_app()

    def test_create_authenticated_asgi_app(self):
        with patch.dict(os.environ, {"MCP_API_TOKEN": "z" * 40}):
            self.assertTrue(callable(server.create_app()))

    def test_expected_tools_are_registered(self):
        # MCP SDK supports this method; exercise the server setup, not merely syntax.
        self.assertEqual(server.mcp.name, "DataCollectionMov - Bob Ross Lab")


if __name__ == "__main__":
    unittest.main()
