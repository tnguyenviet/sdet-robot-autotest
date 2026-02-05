"""
NLP Test Case Generator
=======================

AI-powered test case generator that creates Robot Framework test cases
from natural language descriptions using OpenAI GPT.

Key Features:
- Natural language to Robot Framework conversion
- Smart keyword recognition and suggestion
- Test structure validation
- Integration with existing keyword libraries
"""

import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from robot.api import logger

load_dotenv()


@dataclass
class GeneratedTest:
    """Represents a generated test case."""
    name: str
    description: str
    tags: List[str]
    steps: List[str]
    setup: Optional[str] = None
    teardown: Optional[str] = None
    
    def to_robot_format(self) -> str:
        """Convert to Robot Framework test case format."""
        lines = [f"{self.name}"]
        
        if self.description:
            lines.append(f"    [Documentation]    {self.description}")
        
        if self.tags:
            lines.append(f"    [Tags]    {'    '.join(self.tags)}")
        
        if self.setup:
            lines.append(f"    [Setup]    {self.setup}")
        
        if self.teardown:
            lines.append(f"    [Teardown]    {self.teardown}")
        
        for step in self.steps:
            lines.append(f"    {step}")
        
        return "\n".join(lines)


class NLPTestGenerator:
    """
    Robot Framework library for generating test cases from natural language.
    
    Uses OpenAI GPT to convert plain English descriptions into Robot Framework
    test cases, leveraging knowledge of available keywords.
    
    Example usage:
        Library    libraries.ai.NLPTestGenerator
        
        ${test}=    Generate Test From Description
        ...    User should be able to login with valid credentials
        Log    ${test}
    """
    
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "TEXT"
    
    DEFAULT_MODEL = "gpt-4o"
    
    AVAILABLE_KEYWORDS = """
Available Keywords from SauceDemo Framework:

LOGIN PAGE KEYWORDS:
- Input Username    <username>
- Input Password    <password>
- Click Login Button
- Login With Credentials    <username>    <password>
- Get Login Error Message
- Verify Login Error Message    <expected_message>
- Login Error Should Be Visible
- Login Error Should Not Be Visible
- Clear Login Form
- Verify Login Page Is Displayed

SELENIUM LIBRARY KEYWORDS:
- Open Browser    <url>    <browser>
- Close Browser
- Go To    <url>
- Wait Until Page Contains Element    <locator>
- Page Should Contain    <text>
- Element Should Be Visible    <locator>
- Capture Page Screenshot

TEST DATA:
- Base URL: https://www.saucedemo.com
- Valid User: standard_user / secret_sauce
- Locked User: locked_out_user / secret_sauce
"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        output_dir: Optional[str] = None,
    ):
        """Initialize NLPTestGenerator."""
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._model = model
        self._output_dir = output_dir or str(
            Path(__file__).parent.parent.parent / "tests" / "generated"
        )
        
        self._openai_available = False
        try:
            import openai
            self._openai = openai
            if self._api_key:
                self._client = openai.OpenAI(api_key=self._api_key)
                self._openai_available = True
        except ImportError:
            logger.warn("OpenAI package not installed. Using templates.")
    
    def generate_test_from_description(
        self,
        description: str,
        test_name: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        """Generate a Robot Framework test case from natural language."""
        if self._openai_available:
            return self._generate_with_openai(description, test_name, tags)
        else:
            return self._generate_with_templates(description, test_name, tags)
    
    def generate_test_suite(
        self,
        descriptions: List[str],
        suite_name: str = "Generated Tests",
    ) -> str:
        """Generate a complete Robot Framework test suite."""
        tests = []
        for desc in descriptions:
            test = self.generate_test_from_description(desc)
            tests.append(test)
        
        return self._build_suite(suite_name, tests)
    
    def save_generated_test(self, test_content: str, filename: str) -> str:
        """Save generated test to a file."""
        os.makedirs(self._output_dir, exist_ok=True)
        file_path = os.path.join(self._output_dir, f"{filename}.robot")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        logger.info(f"Saved generated test to {file_path}")
        return file_path
    
    def generate_and_save_test(
        self,
        description: str,
        filename: Optional[str] = None,
    ) -> str:
        """Generate test and save to file."""
        test = self.generate_test_from_description(description)
        
        if filename is None:
            filename = self._generate_filename(description)
        
        suite = self._build_suite("Generated Test", [test])
        return self.save_generated_test(suite, filename)
    
    def get_keyword_suggestions(self, action: str) -> List[str]:
        """Get keyword suggestions for a given action."""
        suggestions = []
        action_lower = action.lower()
        
        keyword_map = {
            "login": [
                "Login With Credentials    <username>    <password>",
                "Input Username    <username>",
                "Input Password    <password>",
                "Click Login Button",
            ],
            "error": [
                "Get Login Error Message",
                "Verify Login Error Message    <expected_message>",
                "Login Error Should Be Visible",
            ],
            "verify": [
                "Verify Login Page Is Displayed",
                "Wait Until Page Contains Element    <locator>",
            ],
        }
        
        for key, keywords in keyword_map.items():
            if key in action_lower:
                suggestions.extend(keywords)
        
        return suggestions if suggestions else ["No suggestions found"]
    
    def _generate_with_openai(
        self,
        description: str,
        test_name: Optional[str],
        tags: Optional[List[str]],
    ) -> str:
        """Generate test using OpenAI API."""
        prompt = f"""Generate a Robot Framework test case for login functionality.

{self.AVAILABLE_KEYWORDS}

DESCRIPTION: {description}
{f'TEST NAME: {test_name}' if test_name else ''}
{f'TAGS: {", ".join(tags)}' if tags else ''}

Generate a single test case in valid Robot Framework format.
"""
        
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": "You are a Robot Framework expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000,
            )
            
            generated = response.choices[0].message.content.strip()
            generated = re.sub(r"```robot\n?", "", generated)
            generated = re.sub(r"```\n?", "", generated)
            
            return generated
            
        except Exception as e:
            logger.warn(f"OpenAI API error: {e}. Falling back to templates.")
            return self._generate_with_templates(description, test_name, tags)
    
    def _generate_with_templates(
        self,
        description: str,
        test_name: Optional[str],
        tags: Optional[List[str]],
    ) -> str:
        """Generate test using template matching."""
        description_lower = description.lower()
        
        if not test_name:
            test_name = self._generate_test_name(description)
        
        test = GeneratedTest(
            name=test_name,
            description=description,
            tags=tags or [],
            steps=[],
        )
        
        if "invalid" in description_lower or "wrong" in description_lower:
            test.steps = [
                "Open Browser    ${BASE_URL}    ${BROWSER}",
                "Verify Login Page Is Displayed",
                "Login With Credentials    invalid_user    wrong_password",
                "Login Error Should Be Visible",
                "Verify Login Error Message    Username and password do not match",
            ]
            test.tags.append("negative")
        elif "locked" in description_lower:
            test.steps = [
                "Open Browser    ${BASE_URL}    ${BROWSER}",
                "Verify Login Page Is Displayed",
                "Login With Credentials    locked_out_user    secret_sauce",
                "Login Error Should Be Visible",
                "Verify Login Error Message    locked out",
            ]
            test.tags.append("negative")
        elif "empty" in description_lower:
            test.steps = [
                "Open Browser    ${BASE_URL}    ${BROWSER}",
                "Verify Login Page Is Displayed",
                "Click Login Button",
                "Login Error Should Be Visible",
                "Verify Login Error Message    Username is required",
            ]
            test.tags.append("negative")
        elif "login" in description_lower:
            test.steps = [
                "Open Browser    ${BASE_URL}    ${BROWSER}",
                "Verify Login Page Is Displayed",
                "Login With Credentials    standard_user    secret_sauce",
                "Wait Until Page Contains Element    css=.inventory_list",
            ]
            test.tags.append("smoke")
        else:
            test.steps = [
                f"# TODO: Implement test for: {description}",
                "Log    Test case needs manual implementation",
            ]
            test.tags.append("todo")
        
        test.teardown = "Close Browser"
        
        return test.to_robot_format()
    
    def _generate_test_name(self, description: str) -> str:
        """Generate test name from description."""
        name = re.sub(r"[^\w\s]", "", description)
        words = name.split()[:6]
        return " ".join(word.capitalize() for word in words)
    
    def _generate_filename(self, description: str) -> str:
        """Generate filename from description."""
        name = re.sub(r"[^\w\s]", "", description.lower())
        words = name.split()[:4]
        return "_".join(words)
    
    def _build_suite(self, suite_name: str, tests: List[str]) -> str:
        """Build complete test suite with settings."""
        settings = f"""*** Settings ***
Documentation     {suite_name} - Auto-generated by NLP Test Generator
...               Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Library           SeleniumLibrary
Library           libraries.pages.LoginPage

Resource          ../resources/keywords/common.resource

Suite Teardown    Close All Browsers

*** Variables ***
${{BASE_URL}}        https://www.saucedemo.com
${{BROWSER}}         chrome

*** Test Cases ***
"""
        return settings + "\n\n".join(tests)


def main():
    """CLI entry point for NLP test generation."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m libraries.ai.nlp_generator \"Test description\"")
        print("\nExamples:")
        print('  python -m libraries.ai.nlp_generator "User logs in with valid credentials"')
        print('  python -m libraries.ai.nlp_generator "User cannot login with wrong password"')
        sys.exit(1)
    
    description = " ".join(sys.argv[1:])
    
    generator = NLPTestGenerator()
    test = generator.generate_test_from_description(description)
    
    print("\n" + "=" * 60)
    print("Generated Test Case:")
    print("=" * 60)
    print(test)
    print("=" * 60)


if __name__ == "__main__":
    main()
