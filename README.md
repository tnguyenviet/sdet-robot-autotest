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

```bash
python -m libraries.ai.nlp_generator "User logs in with valid credentials"
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
