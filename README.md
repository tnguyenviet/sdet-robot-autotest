# SDET Robot Framework Automation Suite

Test automation framework built with **Robot Framework**, **Python**, and **Selenium** for web application testing. Features AI-enhanced capabilities including NLP-based test generation.

## Features

- **Page Object Model (POM)**: Clean separation of page interactions from test logic
- **NLP Test Generator**: Generate tests from natural language descriptions
- **Allure Reports**: Rich, interactive test reports
- **GitHub Actions**: Automated CI/CD pipeline

## Project Structure

```
sdet-robot-autotest/
├── libraries/
│   ├── ai/                    # AI tools (nlp_generator)
│   ├── pages/                 # Page Object classes
│   └── utils/                 # Utilities (browser_manager, config_loader)
├── resources/
│   ├── keywords/              # Reusable keywords
│   ├── locators/              # Element locators (YAML)
│   └── variables/             # Test data
├── tests/
│   └── login/                 # Login test suite
├── requirements.txt
└── README.md
```

## Installation

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/sdet-robot-autotest.git
cd sdet-robot-autotest

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests
robot --outputdir reports --pythonpath . --pythonpath libraries tests/

# Run login tests
robot --outputdir reports --pythonpath . --pythonpath libraries tests/login/

# Run by tag
robot --include smoke --outputdir reports --pythonpath . --pythonpath libraries tests/

# Headless mode
robot --variable HEADLESS:true --outputdir reports --pythonpath . --pythonpath libraries tests/
```

## Test Data

| User Type | Username        | Password     | Description   |
| --------- | --------------- | ------------ | ------------- |
| Standard  | standard_user   | secret_sauce | Normal user   |
| Locked    | locked_out_user | secret_sauce | Locked out    |
| Problem   | problem_user    | secret_sauce | UI issues     |

## AI Features

### NLP Test Generator

Generate Robot Framework test cases from natural language descriptions using AI (OpenAI GPT-4) or template-based matching.

**Key Features:**
- AI-powered or template-based generation (works without API key)
- Auto-generates test names, tags, and proper Robot Framework syntax
- Integrates with existing keywords and test data
- CLI and Robot Framework library usage

#### Quick Start

```bash
# CLI usage - generates and prints test case
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
```

## Reports

```bash
# Allure reporting
robot --listener allure_robotframework --outputdir reports tests/
allure serve allure-results/
```

## Development

```bash
# Format code
black libraries/

# Run unit tests
pytest libraries/ -v
```

## License

MIT License
