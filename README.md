# SDET Robot Framework Automation Suite

> **SDET Technical Exercise**: Test automation framework demonstrating advanced Robot Framework, Python, Selenium, and AI integration capabilities.

**Target Application**: [SauceDemo](https://www.saucedemo.com)  
**Tech Stack**: Robot Framework, Python, Selenium, OpenAI GPT-4

---

## 🎯 Project Highlights

This project showcases:

- ✅ **Custom AI Tool**: NLP Test Generator for natural language test creation
- ✅ **Page Object Model**: Clean, maintainable architecture with custom libraries
- ✅ **Comprehensive Testing**: 10 test cases covering positive, negative, and edge cases
- ✅ **CI/CD Pipeline**: Automated testing with GitHub Actions
- ✅ **Best Practices**: Modular design, reusable components, proper documentation

---

## 📁 Project Structure

```
sdet-robot-autotest/
├── libraries/
│   ├── ai/                    # Custom AI tools
│   │   └── nlp_generator.py   # NLP test generator (OpenAI GPT-4)
│   ├── pages/                 # Page Object Model
│   │   ├── base_page.py       # Base page class with reusable methods
│   │   └── login_page.py      # Login page with 20+ custom keywords
│   └── utils/                 # Utilities
│       ├── browser_manager.py # Browser configuration and management
│       ├── config_loader.py   # YAML configuration loader
│       └── logger.py          # Custom logging
├── resources/
│   ├── keywords/              # Reusable Robot Framework keywords
│   ├── locators/              # YAML-based element locators
│   └── variables/             # Test data and variables
├── tests/
│   └── login/                 # Login test suite (10 test cases)
├── .github/workflows/         # CI/CD pipeline
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/tnguyenviet/sdet-robot-autotest.git
cd sdet-robot-autotest

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
robot --outputdir reports --pythonpath . --pythonpath libraries tests/

# Run login tests only
robot --outputdir reports --pythonpath . --pythonpath libraries tests/login/

# Run by tag
robot --include smoke --outputdir reports --pythonpath . --pythonpath libraries tests/
robot --include negative --outputdir reports --pythonpath . --pythonpath libraries tests/

# Headless mode
robot --variable HEADLESS:true --outputdir reports --pythonpath . --pythonpath libraries tests/
```

---

## ⭐ Custom AI Tool - NLP Test Generator

### Overview

**Innovation**: A custom AI-powered tool that converts natural language descriptions into fully-formed Robot Framework test cases.

**Key Features**:
- **Dual Mode**: OpenAI GPT-4 integration OR template-based fallback (works without API key)
- **Smart Generation**: Auto-generates test names, tags, proper syntax, and teardown
- **Framework Integration**: Uses existing keywords and test data
- **Multiple Interfaces**: CLI, Robot Framework library, Python API

### Setup

```bash
# Optional: Enable AI mode with OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Or add to .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

**Note**: The generator works without an API key using intelligent template matching.

### Usage

#### Command Line Interface

```bash
# CLI usage - generates and prints test case
# Generate test case (prints to console)
python -m libraries.ai.nlp_generator "User logs in with valid credentials"

# Optional: Enable AI mode with OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

#### Usage Examples

**Command Line:**
```bash
python -m libraries.ai.nlp_generator "User cannot login with wrong password"
python -m libraries.ai.nlp_generator "Locked user sees error message"
```

**Robot Framework Library:**
```robot
*** Settings ***
Library    libraries.ai.NLPTestGenerator

*** Test Cases ***
Generate And Save Test
    ${filepath}=    Generate And Save Test
    ...    User cannot login with invalid credentials
    ...    filename=invalid_login_test
```

**Python API:**
```python
from libraries.ai.nlp_generator import NLPTestGenerator

generator = NLPTestGenerator()
test = generator.generate_test_from_description("User logs in successfully")
filepath = generator.save_generated_test(test, "login_test")
```

#### Example Output

Input: `"User logs in with valid credentials"`

```robot
User Logs In With Valid Credentials
    [Documentation]    User logs in with valid credentials
    [Tags]    smoke
    Open Browser    ${BASE_URL}    ${BROWSER}
    Verify Login Page Is Displayed
    Login With Credentials    standard_user    secret_sauce
    Wait Until Page Contains Element    css=.inventory_list
    [Teardown]    Close Browser

# Generate negative test
python -m libraries.ai.nlp_generator "User cannot login with wrong password"

# Generate validation test
python -m libraries.ai.nlp_generator "Locked user sees error message"
```

#### Robot Framework Library

```robot
*** Settings ***
Library    libraries.ai.NLPTestGenerator

*** Test Cases ***
Generate And Save Test
    ${filepath}=    Generate And Save Test
    ...    User cannot login with invalid credentials
    ...    filename=invalid_login_test
    Log    Test saved to: ${filepath}
```

#### Python API

```python
from libraries.ai.nlp_generator import NLPTestGenerator

generator = NLPTestGenerator()
test = generator.generate_test_from_description("User logs in successfully")
filepath = generator.save_generated_test(test, "login_test")
```

### Example Output

**Input**: `"User cannot login with wrong password"`

**Generated Test**:
```robot
User Cannot Login With Wrong Password
    [Documentation]    User cannot login with wrong password
    [Tags]    negative
    Open Browser    ${BASE_URL}    ${BROWSER}
    Verify Login Page Is Displayed
    Login With Credentials    invalid_user    wrong_password
    Login Error Should Be Visible
    Verify Login Error Message    Username and password do not match
    [Teardown]    Close Browser
```

---

## 🏗️ Custom Page Object Library

### BasePage Class

Provides reusable methods for all page objects:
- Smart wait strategies (explicit waits, element visibility)
- Element interaction methods (click, type, get text)
- Error handling and assertions
- Screenshot capture on failures

### LoginPage Class

**20+ Custom Keywords** including:
- `Login With Credentials` - Complete login flow
- `Verify Login Error Message` - Assert error messages
- `Login Error Should Be Visible` - Verify error display
- `Clear Login Form` - Clear input fields
- `Verify Login Page Is Displayed` - Page validation

**Features**:
- Type-safe locators using Python tuples
- Proper Robot Framework `@keyword` decorators
- Comprehensive error handling
- Full documentation and examples

---

## 🧪 Test Coverage

### Test Suite: Login Functionality (10 Test Cases)

#### ✅ Positive Scenarios
- Valid login with standard user
- Valid login with performance glitch user

#### ❌ Negative Scenarios
- Invalid login with wrong password
- Invalid login with wrong username
- Locked user cannot login

#### 🔍 Validation Tests
- Empty username validation
- Empty password validation
- Empty credentials validation

#### 🎨 UI Interaction Tests
- Login error can be dismissed
- Login form can be cleared

### Test Organization

- **Clear Documentation**: Each test has detailed documentation
- **Proper Tagging**: `smoke`, `negative`, `security`, `validation`, `ui`, `critical`
- **Data-Driven**: Uses variables for test data
- **Reusable Keywords**: Shared keywords for common operations

### Test Data

| User Type         | Username              | Password     | Expected Result |
|-------------------|-----------------------|--------------|-----------------|
| Standard User     | standard_user         | secret_sauce | ✅ Success      |
| Performance User  | performance_glitch_user | secret_sauce | ✅ Success (slow) |
| Locked User       | locked_out_user       | secret_sauce | ❌ Locked error |
| Invalid User      | invalid_user          | wrong_pass   | ❌ Auth error   |

---

## 📊 Reports

### Allure Reports

```bash
# Run tests with Allure listener
robot --listener allure_robotframework --outputdir reports tests/

# Serve Allure report
allure serve allure-results/
```

### Robot Framework Reports

After test execution, reports are available in the `reports/` directory:
- `report.html` - Test execution report
- `log.html` - Detailed test log
- `output.xml` - Machine-readable results

---

## 🔄 CI/CD Integration

### GitHub Actions

**Automated workflows**:
- ✅ Run tests on push/pull request
- ✅ Unit tests for custom libraries
- ✅ Headless browser execution
- ✅ Test report generation
- ✅ Artifact upload

**Workflow files**:
- `.github/workflows/test.yml` - Main test execution
- `.github/workflows/unit-tests.yml` - Library unit tests

---

## 🛠️ Development

### Code Formatting

```bash
# Format Python code
black libraries/

# Check code style
flake8 libraries/
```

### Unit Tests

```bash
# Run unit tests for custom libraries
pytest libraries/ -v

# Run with coverage
pytest libraries/ --cov=libraries --cov-report=html
```

### Adding New Tests

1. Create test file in `tests/` directory
2. Use existing keywords from `resources/keywords/`
3. Follow naming conventions and tagging standards
4. Add documentation for each test case

---
## 📝 License

MIT License

---

**Built with ❤️ for SDET Technical Exercise**
