"""
Base Page Object
================

Abstract base class for all Page Objects in the framework.
Provides common functionality for page interactions.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)

from SeleniumLibrary import SeleniumLibrary


class BasePage(ABC):
    """
    Abstract base class for Page Objects.
    
    Provides common methods for:
    - Element location with explicit waits
    - Safe interactions (click, type, etc.)
    - Page state verification
    - Screenshot capture
    
    Subclasses must implement:
    - page_url: Property returning the page URL path
    - is_page_loaded: Method to verify page is loaded
    """
    
    ROBOT_LIBRARY_SCOPE = "TEST SUITE"
    ROBOT_LIBRARY_DOC_FORMAT = "TEXT"
    
    # Default timeout in seconds
    DEFAULT_TIMEOUT = 10
    
    def __init__(self, selenium_lib: Optional[SeleniumLibrary] = None):
        """
        Initialize BasePage.
        
        Args:
            selenium_lib: SeleniumLibrary instance. If None, gets from Robot context.
        """
        self._selenium_lib = selenium_lib
        self._timeout = self.DEFAULT_TIMEOUT

    def _get_selenium_lib(self) -> SeleniumLibrary:
        """Get SeleniumLibrary instance from Robot context or cached."""
        if self._selenium_lib is None:
            try:
                self._selenium_lib = BuiltIn().get_library_instance("SeleniumLibrary")
            except Exception:
                self._selenium_lib = SeleniumLibrary()
        return self._selenium_lib
    
    @property
    def driver(self) -> WebDriver:
        """Get the underlying Selenium WebDriver."""
        return self._get_selenium_lib().driver
    
    @property
    @abstractmethod
    def page_url(self) -> str:
        """Return the URL path for this page (without base URL)."""
        pass
    
    @abstractmethod
    def is_page_loaded(self) -> bool:
        """Verify that the page is fully loaded."""
        pass
    
    def set_selenium_library(self, selenium_lib: SeleniumLibrary) -> None:
        """
        Set the SeleniumLibrary instance.
        
        Args:
            selenium_lib: SeleniumLibrary instance to use.
        """
        self._selenium_lib = selenium_lib
    
    def set_timeout(self, timeout: int) -> None:
        """
        Set the default timeout for waits.
        
        Args:
            timeout: Timeout in seconds.
        """
        self._timeout = timeout
    
    # ==================== Element Location Methods ====================
    
    def find_element(
        self, 
        locator: Tuple[str, str], 
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Find a single element with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds (uses default if None)
            
        Returns:
            WebElement if found
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        timeout = timeout or self._timeout
        wait = WebDriverWait(
            self.driver, 
            timeout,
            ignored_exceptions=[StaleElementReferenceException]
        )
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(
        self, 
        locator: Tuple[str, str], 
        timeout: Optional[int] = None
    ) -> List[WebElement]:
        """
        Find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            List of WebElements (may be empty)
        """
        timeout = timeout or self._timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return self.driver.find_elements(*locator)
        except TimeoutException:
            return []
    
    def find_clickable_element(
        self, 
        locator: Tuple[str, str], 
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Find an element that is clickable.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            Clickable WebElement
        """
        timeout = timeout or self._timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def find_visible_element(
        self, 
        locator: Tuple[str, str], 
        timeout: Optional[int] = None
    ) -> WebElement:
        """
        Find an element that is visible.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Wait timeout in seconds
            
        Returns:
            Visible WebElement
        """
        timeout = timeout or self._timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    # ==================== Element Interaction Methods ====================
    
    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """
        Click on an element.
        
        Args:
            locator: Element locator tuple
            timeout: Wait timeout
        """
        element = self.find_clickable_element(locator, timeout)
        element.click()
    
    def type_text(
        self, 
        locator: Tuple[str, str], 
        text: str, 
        clear_first: bool = True,
        timeout: Optional[int] = None
    ) -> None:
        """
        Type text into an input element.
        
        Args:
            locator: Element locator tuple
            text: Text to type
            clear_first: Whether to clear existing text first
            timeout: Wait timeout
        """
        element = self.find_visible_element(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(
        self, 
        locator: Tuple[str, str], 
        timeout: Optional[int] = None
    ) -> str:
        """
        Get text content of an element.
        
        Args:
            locator: Element locator tuple
            timeout: Wait timeout
            
        Returns:
            Element text content
        """
        element = self.find_visible_element(locator, timeout)
        return element.text
    
    def get_attribute(
        self, 
        locator: Tuple[str, str], 
        attribute: str,
        timeout: Optional[int] = None
    ) -> Optional[str]:
        """
        Get an attribute value from an element.
        
        Args:
            locator: Element locator tuple
            attribute: Attribute name
            timeout: Wait timeout
            
        Returns:
            Attribute value or None
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute)
    
    # ==================== State Verification Methods ====================
    
    def is_element_present(
        self, 
        locator: Tuple[str, str], 
        timeout: int = 2
    ) -> bool:
        """
        Check if element is present in DOM.
        
        Args:
            locator: Element locator tuple
            timeout: Short timeout for check
            
        Returns:
            True if element present, False otherwise
        """
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(
        self, 
        locator: Tuple[str, str], 
        timeout: int = 2
    ) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Element locator tuple
            timeout: Short timeout for check
            
        Returns:
            True if element visible, False otherwise
        """
        try:
            self.find_visible_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_enabled(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is enabled.
        
        Args:
            locator: Element locator tuple
            
        Returns:
            True if element enabled, False otherwise
        """
        try:
            element = self.find_element(locator)
            return element.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def wait_for_element_not_visible(
        self, 
        locator: Tuple[str, str], 
        timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for element to become invisible.
        
        Args:
            locator: Element locator tuple
            timeout: Wait timeout
            
        Returns:
            True if element became invisible
        """
        timeout = timeout or self._timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    # ==================== Navigation Methods ====================
    
    def navigate_to(self, base_url: str) -> None:
        """
        Navigate to this page.
        
        Args:
            base_url: Base URL of the application
        """
        url = f"{base_url.rstrip('/')}/{self.page_url.lstrip('/')}"
        self.driver.get(url)
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """Get the current page title."""
        return self.driver.title
    
    def refresh(self) -> None:
        """Refresh the current page."""
        self.driver.refresh()
    
    # ==================== Utility Methods ====================
    
    def take_screenshot(self, filename: str) -> str:
        """
        Take a screenshot of the current page.
        
        Args:
            filename: Screenshot filename (without extension)
            
        Returns:
            Path to saved screenshot
        """
        return self._get_selenium_lib().capture_page_screenshot(f"{filename}.png")
    
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """
        Scroll element into view.
        
        Args:
            locator: Element locator tuple
        """
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        Wait for page to fully load.
        
        Args:
            timeout: Wait timeout
        """
        timeout = timeout or self._timeout
        wait = WebDriverWait(self.driver, timeout)
        wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    def execute_javascript(self, script: str, *args) -> any:
        """
        Execute JavaScript on the page.
        
        Args:
            script: JavaScript code to execute
            args: Arguments to pass to the script
            
        Returns:
            Script execution result
        """
        return self.driver.execute_script(script, *args)
