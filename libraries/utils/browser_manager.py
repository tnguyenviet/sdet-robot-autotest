"""
Browser Manager
===============

Provides browser setup with webdriver-manager for automatic driver management.
"""

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager


class BrowserManager:
    """Library for managing browser instances with automatic driver setup."""

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self._driver = None

    @keyword("Create Chrome Browser")
    def create_chrome_browser(self, headless: bool = True) -> webdriver.Chrome:
        """
        Creates a Chrome browser instance with webdriver-manager.
        
        Args:
            headless: Run browser in headless mode (default: True)
            
        Returns:
            WebDriver instance
        """
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        
        # Use webdriver-manager to automatically get correct chromedriver
        service = ChromeService(ChromeDriverManager().install())
        
        self._driver = webdriver.Chrome(service=service, options=options)
        return self._driver

    @keyword("Open Chrome To URL")
    def open_chrome_to_url(self, url: str, headless: bool = True):
        """
        Creates Chrome browser and navigates to URL, registering with SeleniumLibrary.
        
        Args:
            url: URL to navigate to
            headless: Run browser in headless mode (default: True)
        """
        driver = self.create_chrome_browser(headless=headless)
        
        # Register with SeleniumLibrary
        selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
        selenium_lib.register_driver(driver, "Chrome")
        
        driver.get(url)
        driver.maximize_window()

    @keyword("Get Browser Driver")
    def get_browser_driver(self):
        """Returns the current browser driver instance."""
        return self._driver

    @keyword("Close Browser Driver")
    def close_browser_driver(self):
        """Closes the browser driver."""
        if self._driver:
            self._driver.quit()
            self._driver = None
