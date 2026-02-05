"""
Automation Logger
=================

Custom logging utilities for the automation framework.
Provides structured logging with context for test execution.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from robot.api import logger as robot_logger


class AutomationLogger:
    """
    Robot Framework library for enhanced logging.
    
    Provides logging with multiple outputs (console, file, Robot log)
    and structured context tracking.
    
    Example usage in Robot Framework:
        Library    libraries.utils.AutomationLogger
        
        Log Step    Clicking login button
        Log Warning    Element took longer than expected to appear
    """
    
    ROBOT_LIBRARY_SCOPE = "TEST SUITE"
    ROBOT_LIBRARY_DOC_FORMAT = "TEXT"
    
    def __init__(self, log_file: Optional[str] = None, log_level: str = "INFO"):
        """
        Initialize AutomationLogger.
        
        Args:
            log_file: Path to log file. If None, logs to reports/automation.log
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self._log_level = getattr(logging, log_level.upper(), logging.INFO)
        self._step_count = 0
        self._test_start_time: Optional[datetime] = None
        
        # Setup Python logger
        self._logger = logging.getLogger("AutomationLogger")
        self._logger.setLevel(self._log_level)
        
        # Clear existing handlers
        self._logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self._log_level)
        console_format = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        self._logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            log_path = Path(log_file)
        else:
            log_path = Path(__file__).parent.parent.parent / "reports" / "automation.log"
        
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(file_format)
        self._logger.addHandler(file_handler)
    
    def log_step(self, message: str, level: str = "INFO") -> None:
        """
        Log a test step with automatic numbering.
        
        Args:
            message: Step description.
            level: Log level (default: INFO).
            
        Example:
            | Log Step | Entering username into login form |
        """
        self._step_count += 1
        formatted_message = f"[Step {self._step_count}] {message}"
        
        self._log(formatted_message, level)
    
    def log_info(self, message: str) -> None:
        """
        Log an informational message.
        
        Args:
            message: Message to log.
            
        Example:
            | Log Info | User successfully logged in |
        """
        self._log(message, "INFO")
    
    def log_warning(self, message: str) -> None:
        """
        Log a warning message.
        
        Args:
            message: Warning message.
            
        Example:
            | Log Warning | Element took 5s to appear, expected 2s |
        """
        self._log(message, "WARN")
    
    def log_error(self, message: str) -> None:
        """
        Log an error message.
        
        Args:
            message: Error message.
            
        Example:
            | Log Error | Failed to click button: element not found |
        """
        self._log(message, "ERROR")
    
    def log_debug(self, message: str) -> None:
        """
        Log a debug message.
        
        Args:
            message: Debug message.
            
        Example:
            | Log Debug | Current URL: https://example.com/page |
        """
        self._log(message, "DEBUG")
    
    def start_test_timer(self) -> None:
        """
        Start timing the current test execution.
        
        Example:
            | Start Test Timer |
        """
        self._test_start_time = datetime.now()
        self._step_count = 0
        self._log("Test execution started", "INFO")
    
    def stop_test_timer(self) -> str:
        """
        Stop the test timer and return elapsed time.
        
        Returns:
            Elapsed time as formatted string.
            
        Example:
            | ${elapsed}= | Stop Test Timer |
        """
        if not self._test_start_time:
            return "Timer not started"
        
        elapsed = datetime.now() - self._test_start_time
        elapsed_str = str(elapsed).split(".")[0]  # Remove microseconds
        
        self._log(f"Test execution completed in {elapsed_str}", "INFO")
        self._test_start_time = None
        
        return elapsed_str
    
    def log_section(self, title: str) -> None:
        """
        Log a section header for better log readability.
        
        Args:
            title: Section title.
            
        Example:
            | Log Section | Login Verification |
        """
        separator = "=" * 60
        self._log(separator, "INFO")
        self._log(f"  {title.upper()}", "INFO")
        self._log(separator, "INFO")
    
    def log_key_value(self, key: str, value: str) -> None:
        """
        Log a key-value pair with formatting.
        
        Args:
            key: Key/label.
            value: Value.
            
        Example:
            | Log Key Value | Username | standard_user |
        """
        self._log(f"{key}: {value}", "INFO")
    
    def _log(self, message: str, level: str) -> None:
        """Internal logging method that outputs to both Python logger and Robot log."""
        # Python logger
        log_method = getattr(self._logger, level.lower(), self._logger.info)
        log_method(message)
        
        # Robot Framework logger
        try:
            robot_logger.write(message, level)
        except Exception:
            # Not running in Robot Framework context
            pass
    
    def reset_step_counter(self) -> None:
        """
        Reset the step counter to 0.
        
        Example:
            | Reset Step Counter |
        """
        self._step_count = 0
