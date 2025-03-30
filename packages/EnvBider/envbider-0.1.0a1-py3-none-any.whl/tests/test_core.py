"""Tests for the core functionality of EnvBinder."""

import os
import unittest
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from envbider.core import env_binder, ConfigurationError

def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

@env_binder
class NestedConfig:
    name: str
    value: int

@env_binder
class TestConfig:
    db_host: str
    db_port: int = 5432
    debug_mode: bool = False
    api_keys: List[str] = []
    max_connections: Optional[int] = None
    created_at: datetime = None
    nested: NestedConfig = None

class TestEnvBinder(unittest.TestCase):
    def setUp(self):
        # Clear any existing environment variables before each test
        for var in ['DB_HOST', 'DB_PORT', 'DEBUG_MODE', 'API_KEYS', 'MAX_CONNECTIONS', 'CREATED_AT', 'NESTED_NAME', 'NESTED_VALUE']:
            if var in os.environ:
                del os.environ[var]

    def test_required_field(self):
        """Test that required fields raise an error when not set."""
        with self.assertRaises(ConfigurationError):
            TestConfig()

    def test_default_values(self):
        """Test that default values are used when environment variables are not set."""
        os.environ['DB_HOST'] = 'localhost'
        config = TestConfig()
        self.assertEqual(config.db_host, 'localhost')
        self.assertEqual(config.db_port, 5432)
        self.assertEqual(config.debug_mode, False)
        self.assertEqual(config.api_keys, [])

    def test_type_conversion(self):
        """Test that values are correctly converted to their target types."""
        os.environ.update({
            'DB_HOST': 'example.com',
            'DB_PORT': '8080',
            'DEBUG_MODE': 'true',
            'API_KEYS': 'key1,key2,key3'
        })

        config = TestConfig()
        self.assertEqual(config.db_host, 'example.com')
        self.assertEqual(config.db_port, 8080)
        self.assertTrue(config.debug_mode)
        self.assertEqual(config.api_keys, ['key1', 'key2', 'key3'])

    def test_invalid_type_conversion(self):
        """Test that invalid type conversions raise an error."""
        os.environ.update({
            'DB_HOST': 'localhost',
            'DB_PORT': 'not_an_integer'
        })

        with self.assertRaises(ConfigurationError):
            TestConfig()

    def test_optional_fields(self):
        """Test optional fields with None default values."""
        os.environ.update({
            'DB_HOST': 'localhost',
            'MAX_CONNECTIONS': '100'
        })
        config = TestConfig()
        self.assertEqual(config.max_connections, 100)
        self.assertIsNone(config.created_at)

    def test_custom_type_conversion(self):
        """Test custom type conversion for datetime."""
        os.environ.update({
            'DB_HOST': 'localhost',
            'CREATED_AT': '2023-01-01 12:00:00'
        })
        config = TestConfig()
        self.assertEqual(
            config.created_at,
            datetime(2023, 1, 1, 12, 0, 0)
        )

    def test_nested_config(self):
        """Test nested configuration objects."""
        os.environ.update({
            'DB_HOST': 'localhost',
            'NESTED_NAME': 'test',
            'NESTED_VALUE': '42'
        })
        config = TestConfig()
        self.assertIsInstance(config.nested, NestedConfig)
        self.assertEqual(config.nested.name, 'test')
        self.assertEqual(config.nested.value, 42)

    def test_empty_list(self):
        """Test empty list handling."""
        os.environ.update({
            'DB_HOST': 'localhost',
            'API_KEYS': ''
        })
        config = TestConfig()
        self.assertEqual(config.api_keys, [])

    def test_special_characters(self):
        """Test handling of special characters in values."""
        os.environ.update({
            'DB_HOST': 'localhost',
            'API_KEYS': 'key1,key2=value,key3;value'
        })
        config = TestConfig()
        self.assertEqual(
            config.api_keys,
            ['key1', 'key2=value', 'key3;value']
        )

if __name__ == '__main__':
    unittest.main()