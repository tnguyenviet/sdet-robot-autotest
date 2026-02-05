"""
Login Page Object
=================

Page Object for the SauceDemo login page.
Provides keywords for login operations and validation.
"""

from typing import Optional, Tuple

from robot.api.deco import keyword
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from libraries.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Robot Framework library for SauceDemo Login Page interactions.
    
    This page object provides keywords for:
    - Entering credentials
    - Submitting login form
    - Verifying error messages
    - Handling login edge cases
    
    Example usage in Robot Framework:
        Library    libraries.pages.LoginPage
        
        Input Username    standard_user
        Input Password    secret_sauce
        Click Login Button
        Verify Successful Login
    """
    
    ROBOT_LIBRARY_SCOPE = "TEST SUITE"
    ROBOT_LIBRARY_DOC_FORMAT = "TEXT"
    
    # ==================== Locators ====================
    
    # Input fields
    USERNAME_INPUT: Tuple[str, str] = (By.ID, "user-name")
    PASSWORD_INPUT: Tuple[str, str] = (By.ID, "password")
    
    # Buttons
    LOGIN_BUTTON: Tuple[str, str] = (By.ID, "login-button")
    
    # Error messages
    ERROR_MESSAGE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON: Tuple[str, str] = (By.CLASS_NAME, "error-button")
    
    # Logo
    LOGIN_LOGO: Tuple[str, str] = (By.CLASS_NAME, "login_logo")
    
    # Credentials list (for reference display on page)
    CREDENTIALS_WRAPPER: Tuple[str, str] = (By.ID, "login_credentials")
    
    @property
    def page_url(self) -> str:
        """Login page URL path."""
        return "/"
    
    def is_page_loaded(self) -> bool:
        """Verify login page is fully loaded."""
        return (
            self.is_element_visible(self.USERNAME_INPUT) and
            self.is_element_visible(self.PASSWORD_INPUT) and
            self.is_element_visible(self.LOGIN_BUTTON)
        )
    
    # ==================== Robot Framework Keywords ====================
    
    @keyword("Input Username")
    def input_username(self, username: str) -> None:
        """
        Enter username into the username field.
        
        Args:
            username: Username to enter
            
        Example:
            | Input Username | standard_user |
        """
        self.type_text(self.USERNAME_INPUT, username)
    
    @keyword("Input Password")
    def input_password(self, password: str) -> None:
        """
        Enter password into the password field.
        
        Args:
            password: Password to enter
            
        Example:
            | Input Password | secret_sauce |
        """
        self.type_text(self.PASSWORD_INPUT, password)
    
    @keyword("Click Login Button")
    def click_login_button(self) -> None:
        """
        Click the login button to submit the form.
        
        Example:
            | Click Login Button |
        """
        self.click(self.LOGIN_BUTTON)
    
    @keyword("Login With Credentials")
    def login_with_credentials(self, username: str, password: str) -> None:
        """
        Complete login flow with given credentials.
        
        Args:
            username: Username to enter
            password: Password to enter
            
        Example:
            | Login With Credentials | standard_user | secret_sauce |
        """
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()
    
    @keyword("Submit Login With Enter Key")
    def submit_login_with_enter_key(self) -> None:
        """
        Submit the login form by pressing Enter in password field.
        
        Example:
            | Submit Login With Enter Key |
        """
        element = self.find_visible_element(self.PASSWORD_INPUT)
        element.send_keys(Keys.RETURN)
    
    @keyword("Get Login Error Message")
    def get_login_error_message(self) -> str:
        """
        Get the error message displayed on login failure.
        
        Returns:
            Error message text
            
        Example:
            | ${error}= | Get Login Error Message |
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    @keyword("Verify Login Error Message")
    def verify_login_error_message(self, expected_message: str) -> bool:
        """
        Verify the login error message matches expected text.
        
        Args:
            expected_message: Expected error message text
            
        Returns:
            True if message matches
            
        Example:
            | Verify Login Error Message | Username is required |
        """
        actual_message = self.get_login_error_message()
        if expected_message not in actual_message:
            raise AssertionError(
                f"Expected error message containing '{expected_message}', "
                f"but got '{actual_message}'"
            )
        return True
    
    @keyword("Login Error Should Be Visible")
    def login_error_should_be_visible(self) -> bool:
        """
        Verify that a login error message is displayed.
        
        Returns:
            True if error is visible
            
        Example:
            | Login Error Should Be Visible |
        """
        if not self.is_element_visible(self.ERROR_MESSAGE):
            raise AssertionError("Expected login error message to be visible")
        return True
    
    @keyword("Login Error Should Not Be Visible")
    def login_error_should_not_be_visible(self) -> bool:
        """
        Verify that no login error message is displayed.
        
        Returns:
            True if no error visible
            
        Example:
            | Login Error Should Not Be Visible |
        """
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=1):
            raise AssertionError("Expected no login error message to be visible")
        return True
    
    @keyword("Dismiss Login Error")
    def dismiss_login_error(self) -> None:
        """
        Click the X button to dismiss the login error.
        
        Example:
            | Dismiss Login Error |
        """
        self.click(self.ERROR_BUTTON)
    
    @keyword("Clear Login Form")
    def clear_login_form(self) -> None:
        """
        Clear both username and password fields.
        
        Example:
            | Clear Login Form |
        """
        username_elem = self.find_visible_element(self.USERNAME_INPUT)
        username_elem.clear()
        
        password_elem = self.find_visible_element(self.PASSWORD_INPUT)
        password_elem.clear()
    
    @keyword("Verify Login Page Is Displayed")
    def verify_login_page_is_displayed(self) -> bool:
        """
        Verify the login page is currently displayed.
        
        Returns:
            True if login page is displayed
            
        Example:
            | Verify Login Page Is Displayed |
        """
        if not self.is_page_loaded():
            raise AssertionError("Login page is not displayed")
        return True
    
    @keyword("Get Username Field Value")
    def get_username_field_value(self) -> str:
        """
        Get the current value in the username field.
        
        Returns:
            Username field value
            
        Example:
            | ${username}= | Get Username Field Value |
        """
        return self.get_attribute(self.USERNAME_INPUT, "value") or ""
    
    @keyword("Get Password Field Value")
    def get_password_field_value(self) -> str:
        """
        Get the current value in the password field.
        
        Returns:
            Password field value (masked)
            
        Example:
            | ${password}= | Get Password Field Value |
        """
        return self.get_attribute(self.PASSWORD_INPUT, "value") or ""
    
    @keyword("Verify Username Field Is Empty")
    def verify_username_field_is_empty(self) -> bool:
        """
        Verify username field is empty.
        
        Returns:
            True if empty
            
        Example:
            | Verify Username Field Is Empty |
        """
        value = self.get_username_field_value()
        if value:
            raise AssertionError(f"Username field is not empty, contains: {value}")
        return True
    
    @keyword("Verify Password Field Is Empty")
    def verify_password_field_is_empty(self) -> bool:
        """
        Verify password field is empty.
        
        Returns:
            True if empty
            
        Example:
            | Verify Password Field Is Empty |
        """
        value = self.get_password_field_value()
        if value:
            raise AssertionError("Password field is not empty")
        return True
    
    @keyword("Login Button Should Be Enabled")
    def login_button_should_be_enabled(self) -> bool:
        """
        Verify login button is enabled.
        
        Returns:
            True if enabled
            
        Example:
            | Login Button Should Be Enabled |
        """
        if not self.is_element_enabled(self.LOGIN_BUTTON):
            raise AssertionError("Login button is not enabled")
        return True
