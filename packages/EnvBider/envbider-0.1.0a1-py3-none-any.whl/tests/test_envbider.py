"""Tests for the EnvBider package."""

import unittest
from envbider import __version__


class TestEnvBider(unittest.TestCase):
    """Test cases for EnvBider."""

    def test_version(self):
        """Test that version is a string."""
        self.assertIsInstance(__version__, str)


if __name__ == "__main__":
    unittest.main()