"""
Configuration Loader
====================

Loads configuration from YAML files and environment variables.
Provides a unified interface for accessing test configuration.
"""

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv


class ConfigLoader:
    """
    Robot Framework library for loading and managing configuration.
    
    Provides keywords to load configuration from YAML files and environment variables.
    
    Example usage in Robot Framework:
        Library    libraries.utils.ConfigLoader
        
        ${config}=    Load Config    ${CURDIR}/config.yaml
        ${value}=     Get Config Value    database.host
    """
    
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "TEXT"
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize ConfigLoader.
        
        Args:
            env_file: Path to .env file. If None, searches for .env in project root.
        """
        self._config: dict = {}
        self._env_loaded = False
        
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            # Search for .env in project root
            project_root = Path(__file__).parent.parent.parent
            env_path = project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)
        
        self._env_loaded = True
    
    def load_config(self, file_path: str) -> dict:
        """
        Load configuration from a YAML file.
        
        Args:
            file_path: Path to the YAML configuration file.
            
        Returns:
            Dictionary containing the configuration.
            
        Example:
            | ${config}= | Load Config | ${CURDIR}/config.yaml |
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
        
        self._config.update(config)
        return config
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., "database.host")
            default: Default value if key not found.
            
        Returns:
            Configuration value or default.
            
        Example:
            | ${host}= | Get Config Value | database.host | localhost |
        """
        keys = key.split(".")
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get an environment variable.
        
        Args:
            key: Environment variable name.
            default: Default value if not found.
            
        Returns:
            Environment variable value or default.
            
        Example:
            | ${api_key}= | Get Env | OPENAI_API_KEY |
        """
        return os.getenv(key, default)
    
    def set_config_value(self, key: str, value: Any) -> None:
        """
        Set a configuration value at runtime.
        
        Args:
            key: Configuration key in dot notation.
            value: Value to set.
            
        Example:
            | Set Config Value | browser.headless | ${TRUE} |
        """
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_browser_config(self) -> dict:
        """
        Get browser configuration from environment or defaults.
        
        Returns:
            Dictionary with browser configuration.
        """
        return {
            "browser": self.get_env("BROWSER", "chrome"),
            "headless": self.get_env("HEADLESS", "true").lower() == "true",
            "implicit_wait": int(self.get_env("IMPLICIT_WAIT", "10")),
            "page_load_timeout": int(self.get_env("PAGE_LOAD_TIMEOUT", "30")),
        }
    
    def get_saucedemo_credentials(self, user_type: str = "standard") -> dict:
        """
        Get SauceDemo test credentials.
        
        Args:
            user_type: Type of user (standard, locked, problem, performance, error, visual)
            
        Returns:
            Dictionary with username and password.
            
        Example:
            | ${creds}= | Get Saucedemo Credentials | standard |
        """
        user_map = {
            "standard": "standard_user",
            "locked": "locked_out_user",
            "problem": "problem_user",
            "performance": "performance_glitch_user",
            "error": "error_user",
            "visual": "visual_user",
        }
        
        username = user_map.get(user_type, "standard_user")
        password = self.get_env("SAUCE_PASSWORD", "secret_sauce")
        
        return {"username": username, "password": password}
