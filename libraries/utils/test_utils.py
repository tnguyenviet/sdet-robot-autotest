"""
Unit Tests for Utility Libraries
"""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from libraries.utils.config_loader import ConfigLoader
from libraries.utils.logger import AutomationLogger


class TestConfigLoader:
    """Tests for ConfigLoader class."""
    
    @pytest.fixture
    def config_loader(self):
        """Create ConfigLoader instance."""
        return ConfigLoader()
    
    @pytest.fixture
    def temp_yaml_file(self, tmp_path):
        """Create temporary YAML config file."""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text("""
database:
  host: localhost
  port: 5432
  name: testdb

browser:
  headless: true
  timeout: 30

features:
  - login
  - cart
  - checkout
""")
        return str(config_file)
    
    def test_load_config(self, config_loader, temp_yaml_file):
        """Test loading YAML configuration."""
        config = config_loader.load_config(temp_yaml_file)
        
        assert "database" in config
        assert config["database"]["host"] == "localhost"
        assert config["database"]["port"] == 5432
    
    def test_load_config_file_not_found(self, config_loader):
        """Test error when config file not found."""
        with pytest.raises(FileNotFoundError):
            config_loader.load_config("/nonexistent/config.yaml")
    
    def test_get_config_value_simple(self, config_loader, temp_yaml_file):
        """Test getting simple config value."""
        config_loader.load_config(temp_yaml_file)
        
        value = config_loader.get_config_value("database.name")
        
        assert value == "testdb"
    
    def test_get_config_value_nested(self, config_loader, temp_yaml_file):
        """Test getting nested config value."""
        config_loader.load_config(temp_yaml_file)
        
        value = config_loader.get_config_value("browser.timeout")
        
        assert value == 30
    
    def test_get_config_value_not_found(self, config_loader, temp_yaml_file):
        """Test default value when key not found."""
        config_loader.load_config(temp_yaml_file)
        
        value = config_loader.get_config_value("nonexistent.key", "default")
        
        assert value == "default"
    
    def test_set_config_value(self, config_loader):
        """Test setting config value at runtime."""
        config_loader.set_config_value("new.setting.value", 42)
        
        value = config_loader.get_config_value("new.setting.value")
        
        assert value == 42
    
    def test_get_env(self, config_loader):
        """Test getting environment variable."""
        with patch.dict(os.environ, {"TEST_VAR": "test_value"}):
            value = config_loader.get_env("TEST_VAR")
            
            assert value == "test_value"
    
    def test_get_env_default(self, config_loader):
        """Test default value for missing env var."""
        value = config_loader.get_env("NONEXISTENT_VAR", "default")
        
        assert value == "default"
    
    def test_get_browser_config(self, config_loader):
        """Test browser configuration retrieval."""
        with patch.dict(os.environ, {
            "BROWSER": "firefox",
            "HEADLESS": "false",
            "IMPLICIT_WAIT": "5",
        }):
            config = config_loader.get_browser_config()
            
            assert config["browser"] == "firefox"
            assert config["headless"] is False
            assert config["implicit_wait"] == 5
    
    def test_get_browser_config_defaults(self, config_loader):
        """Test browser configuration with defaults."""
        # Remove env vars if they exist
        with patch.dict(os.environ, {}, clear=True):
            config = config_loader.get_browser_config()
            
            assert config["browser"] == "chrome"
            assert config["headless"] is True
            assert config["implicit_wait"] == 10
    
    def test_get_saucedemo_credentials(self, config_loader):
        """Test getting SauceDemo credentials."""
        creds = config_loader.get_saucedemo_credentials("standard")
        
        assert creds["username"] == "standard_user"
        assert "password" in creds
    
    def test_get_saucedemo_credentials_locked(self, config_loader):
        """Test getting locked user credentials."""
        creds = config_loader.get_saucedemo_credentials("locked")
        
        assert creds["username"] == "locked_out_user"
    
    def test_get_saucedemo_credentials_unknown_type(self, config_loader):
        """Test fallback for unknown user type."""
        creds = config_loader.get_saucedemo_credentials("unknown")
        
        assert creds["username"] == "standard_user"


class TestAutomationLogger:
    """Tests for AutomationLogger class."""
    
    @pytest.fixture
    def logger(self, tmp_path):
        """Create AutomationLogger with temp log file."""
        log_file = str(tmp_path / "test.log")
        return AutomationLogger(log_file=log_file)
    
    def test_log_step_increments_counter(self, logger):
        """Test that log_step increments step counter."""
        logger.log_step("First step")
        logger.log_step("Second step")
        
        assert logger._step_count == 2
    
    def test_reset_step_counter(self, logger):
        """Test resetting step counter."""
        logger.log_step("Step one")
        logger.log_step("Step two")
        logger.reset_step_counter()
        
        assert logger._step_count == 0
    
    def test_start_test_timer(self, logger):
        """Test starting test timer."""
        logger.start_test_timer()
        
        assert logger._test_start_time is not None
        assert logger._step_count == 0
    
    def test_stop_test_timer(self, logger):
        """Test stopping test timer."""
        logger.start_test_timer()
        elapsed = logger.stop_test_timer()
        
        assert logger._test_start_time is None
        assert ":" in elapsed  # Format like "0:00:00"
    
    def test_stop_test_timer_not_started(self, logger):
        """Test stopping timer that wasn't started."""
        elapsed = logger.stop_test_timer()
        
        assert elapsed == "Timer not started"
    
    def test_log_info(self, logger, tmp_path):
        """Test logging info message."""
        logger.log_info("Test info message")
        
        log_content = (tmp_path / "test.log").read_text()
        assert "Test info message" in log_content
    
    def test_log_warning(self, logger, tmp_path):
        """Test logging warning message."""
        logger.log_warning("Test warning")
        
        log_content = (tmp_path / "test.log").read_text()
        assert "Test warning" in log_content
    
    def test_log_error(self, logger, tmp_path):
        """Test logging error message."""
        logger.log_error("Test error")
        
        log_content = (tmp_path / "test.log").read_text()
        assert "Test error" in log_content
    
    def test_log_section(self, logger, tmp_path):
        """Test logging section header."""
        logger.log_section("Test Section")
        
        log_content = (tmp_path / "test.log").read_text()
        assert "TEST SECTION" in log_content
        assert "=" in log_content
    
    def test_log_key_value(self, logger, tmp_path):
        """Test logging key-value pair."""
        logger.log_key_value("Username", "test_user")
        
        log_content = (tmp_path / "test.log").read_text()
        assert "Username: test_user" in log_content
    
    def test_log_debug(self, logger, tmp_path):
        """Test logging debug message."""
        # Debug should be logged to file even if console level is INFO
        logger.log_debug("Debug message")
        
        log_content = (tmp_path / "test.log").read_text()
        assert "Debug message" in log_content
