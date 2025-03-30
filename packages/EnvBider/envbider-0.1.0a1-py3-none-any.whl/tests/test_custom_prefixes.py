"""Tests for custom prefixes functionality in EnvBider."""

import os
import unittest
from typing import Optional

from envbider.core import env_binder, ConfigurationError


@env_binder(prefix="DB")
class DatabaseConfig:
    """Database configuration with custom prefix."""
    host: str
    port: int = 5432
    username: str
    password: str


@env_binder(prefix="LOG")
class LoggingConfig:
    """Logging configuration with custom prefix."""
    level: str = "INFO"
    file_path: Optional[str] = None


@env_binder
class AppConfig:
    """Main application configuration."""
    app_name: str
    debug_mode: bool = False
    
    # Nested configuration objects
    database: DatabaseConfig = None
    logging: LoggingConfig = None


class TestCustomPrefixes(unittest.TestCase):
    """Test cases for custom prefixes functionality."""
    
    def setUp(self):
        """Clear environment variables before each test."""
        # Clear any existing environment variables before each test
        for key in list(os.environ.keys()):
            if any(key.startswith(prefix) for prefix in ['APP_', 'DEBUG_', 'DB_', 'LOG_']):
                del os.environ[key]
    
    def test_custom_prefix_direct_access(self):
        """Test that custom prefixes work for direct access to configuration classes."""
        os.environ.update({
            'DB_HOST': 'testdb.example.com',
            'DB_PORT': '1234',
            'DB_USERNAME': 'testuser',
            'DB_PASSWORD': 'testpass'
        })
        
        db_config = DatabaseConfig()
        self.assertEqual(db_config.host, 'testdb.example.com')
        self.assertEqual(db_config.port, 1234)
        self.assertEqual(db_config.username, 'testuser')
        self.assertEqual(db_config.password, 'testpass')
    
    def test_custom_prefix_nested_config(self):
        """Test that custom prefixes work for nested configuration objects."""
        os.environ.update({
            'APP_NAME': 'TestApp',
            'DEBUG_MODE': 'true',
            'DB_HOST': 'localhost',
            'DB_PORT': '5432',
            'DB_USERNAME': 'admin',
            'DB_PASSWORD': 'secure_password',
            'LOG_LEVEL': 'DEBUG',
            'LOG_FILE_PATH': '/var/log/test.log'
        })
        
        config = AppConfig()
        
        # Check main config
        self.assertEqual(config.app_name, 'TestApp')
        self.assertTrue(config.debug_mode)
        
        # Check database config with custom prefix
        self.assertIsInstance(config.database, DatabaseConfig)
        self.assertEqual(config.database.host, 'localhost')
        self.assertEqual(config.database.port, 5432)
        self.assertEqual(config.database.username, 'admin')
        self.assertEqual(config.database.password, 'secure_password')
        
        # Check logging config with custom prefix
        self.assertIsInstance(config.logging, LoggingConfig)
        self.assertEqual(config.logging.level, 'DEBUG')
        self.assertEqual(config.logging.file_path, '/var/log/test.log')
    
    def test_custom_prefix_override(self):
        """Test that custom prefixes override the default nested prefixing behavior."""
        # Set up environment variables with both patterns to verify which one is used
        os.environ.update({
            'APP_NAME': 'TestApp',
            
            # These should be used (custom prefix)
            'DB_HOST': 'db.example.com',
            'DB_USERNAME': 'dbuser',
            'DB_PASSWORD': 'dbpass',  # Added missing required password field
            
            # These should be ignored (default nested prefix)
            'DATABASE_HOST': 'wrong.example.com',
            'DATABASE_USERNAME': 'wronguser'
        })
        
        config = AppConfig()
        
        # Verify that the custom prefix values are used
        self.assertEqual(config.database.host, 'db.example.com')
        self.assertEqual(config.database.username, 'dbuser')
        
        # Verify default values are still respected
        self.assertEqual(config.database.port, 5432)
    
    def test_missing_required_fields_with_custom_prefix(self):
        """Test that required fields with custom prefixes raise appropriate errors."""
        # Only set some of the required fields
        os.environ.update({
            'APP_NAME': 'TestApp',
            'DB_HOST': 'localhost',
            # Missing DB_USERNAME and DB_PASSWORD
        })
        
        # This should raise an error because required fields are missing
        with self.assertRaises(ConfigurationError):
            AppConfig()


if __name__ == '__main__':
    unittest.main()