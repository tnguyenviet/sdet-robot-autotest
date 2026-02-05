"""
Page Object Model Classes
=========================

Contains page object classes for SauceDemo website automation.
Each page class provides Robot Framework keywords for interacting with that page.
"""

from libraries.pages.base_page import BasePage
from libraries.pages.login_page import LoginPage

__all__ = [
    "BasePage",
    "LoginPage",
]
