"""
Unit Tests for NLP Test Generator
"""

import pytest
from libraries.ai.nlp_generator import NLPTestGenerator, GeneratedTest


class TestGeneratedTest:
    """Tests for GeneratedTest dataclass."""
    
    def test_to_robot_format_basic(self):
        """Test basic test case generation."""
        test = GeneratedTest(
            name="Sample Test",
            description="A sample test",
            tags=["smoke"],
            steps=["Log    Hello World"],
        )
        
        result = test.to_robot_format()
        
        assert "Sample Test" in result
        assert "[Documentation]    A sample test" in result
        assert "[Tags]    smoke" in result
        assert "Log    Hello World" in result
    
    def test_to_robot_format_with_setup_teardown(self):
        """Test generation with setup and teardown."""
        test = GeneratedTest(
            name="Test With Setup",
            description="",
            tags=[],
            steps=["Click Button"],
            setup="Open Browser",
            teardown="Close Browser",
        )
        
        result = test.to_robot_format()
        
        assert "[Setup]    Open Browser" in result
        assert "[Teardown]    Close Browser" in result
    
    def test_to_robot_format_multiple_tags(self):
        """Test generation with multiple tags."""
        test = GeneratedTest(
            name="Multi Tag Test",
            description="",
            tags=["smoke", "e2e", "critical"],
            steps=["Log    Test"],
        )
        
        result = test.to_robot_format()
        
        assert "[Tags]    smoke    e2e    critical" in result


class TestNLPTestGenerator:
    """Tests for NLPTestGenerator class."""
    
    @pytest.fixture
    def generator(self):
        """Create generator instance without API key."""
        return NLPTestGenerator(api_key=None)
    
    def test_generate_test_name(self, generator):
        """Test automatic test name generation."""
        description = "User logs in with valid credentials"
        name = generator._generate_test_name(description)
        
        assert "User" in name
        assert "Logs" in name
        assert len(name.split()) <= 6
    
    def test_generate_filename(self, generator):
        """Test filename generation from description."""
        description = "User logs in successfully!"
        filename = generator._generate_filename(description)
        
        assert filename == "user_logs_in_successfully"
        assert " " not in filename
        assert "!" not in filename
    
    def test_get_keyword_suggestions_login(self, generator):
        """Test keyword suggestions for login action."""
        suggestions = generator.get_keyword_suggestions("login")
        
        assert len(suggestions) > 0
        assert any("Login" in s for s in suggestions)
    
    def test_get_keyword_suggestions_unknown(self, generator):
        """Test keyword suggestions for unknown action."""
        suggestions = generator.get_keyword_suggestions("unknown_action_xyz")
        
        assert "No suggestions found" in suggestions[0]
    
    def test_generate_with_templates_login(self, generator):
        """Test template-based generation for login test."""
        test = generator._generate_with_templates(
            "User logs in with valid credentials",
            None,
            None
        )
        
        assert "Login With Credentials" in test
        assert "Close Browser" in test  # Teardown
    
    def test_generate_with_templates_invalid_login(self, generator):
        """Test template-based generation for invalid login."""
        test = generator._generate_with_templates(
            "User cannot login with invalid password",
            None,
            ["negative"]
        )
        
        assert "invalid" in test.lower() or "wrong" in test.lower()
        assert "[Tags]" in test
    
    def test_generate_with_templates_locked_user(self, generator):
        """Test template-based generation for locked user."""
        test = generator._generate_with_templates(
            "Locked user cannot login",
            None,
            None
        )
        
        assert "locked_out_user" in test
        assert "Login Error Should Be Visible" in test
    
    def test_generate_with_templates_empty_credentials(self, generator):
        """Test template-based generation for empty credentials."""
        test = generator._generate_with_templates(
            "User clicks login with empty fields",
            None,
            None
        )
        
        assert "Click Login Button" in test
        assert "Login Error Should Be Visible" in test
    
    def test_generate_with_templates_generic(self, generator):
        """Test template-based generation for unknown scenario."""
        test = generator._generate_with_templates(
            "Something completely different",
            None,
            None
        )
        
        # Should include TODO comment for manual implementation
        assert "TODO" in test or "Log" in test
    
    def test_build_suite(self, generator):
        """Test suite building with multiple tests."""
        tests = [
            "Test One\n    Log    First test",
            "Test Two\n    Log    Second test"
        ]
        
        suite = generator._build_suite("My Test Suite", tests)
        
        assert "*** Settings ***" in suite
        assert "*** Test Cases ***" in suite
        assert "Test One" in suite
        assert "Test Two" in suite
        assert "My Test Suite" in suite
    
    def test_generate_test_from_description_returns_string(self, generator):
        """Test that generate_test_from_description returns valid string."""
        result = generator.generate_test_from_description(
            "User performs login"
        )
        
        assert isinstance(result, str)
        assert len(result) > 0


class TestNLPGeneratorAvailableKeywords:
    """Tests for the available keywords documentation."""
    
    def test_available_keywords_contains_login(self):
        """Verify login keywords are documented."""
        assert "Input Username" in NLPTestGenerator.AVAILABLE_KEYWORDS
        assert "Click Login Button" in NLPTestGenerator.AVAILABLE_KEYWORDS
    
    def test_available_keywords_contains_test_data(self):
        """Verify test data is documented."""
        assert "standard_user" in NLPTestGenerator.AVAILABLE_KEYWORDS
        assert "saucedemo.com" in NLPTestGenerator.AVAILABLE_KEYWORDS
