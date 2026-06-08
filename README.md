# SQA Automation Framework — Job Portal

Selenium + Python automation framework for Login and Registration testing of
[https://jobprtal.alarafafragrance.com](https://jobprtal.alarafafragrance.com).

---

## Project Structure

```
sqa_automation/
├── pages/
│   ├── __init__.py
│   ├── base_page.py          # Base page with reusable Selenium helpers & alert handling
│   ├── login_page.py         # Login page object
│   └── register_page.py      # Registration page object
├── tests/
│   ├── __init__.py
│   ├── test_login.py         # 10 login test cases
│   └── test_registration.py  # 12 registration test cases
├── utils/
│   ├── __init__.py
│   ├── config.py             # Reads .env configuration
│   └── data_generator.py     # Faker-based test data generator
├── reports/                  # Auto-generated HTML test reports
├── drivers/                  # (optional) place chromedriver here
├── conftest.py               # Pytest fixtures (WebDriver setup/teardown)
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
├── .env                      # Local config (do NOT commit)
├── .env.example              # Template — safe to commit
├── .gitignore                # Git ignore rules
└── Test_Cases_SQA.xlsx       # Test case documentation
```

---

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Google Chrome (latest)
- Git

### 2. Clone the Repository
```bash
git clone https://github.com/KafkaScribe/sqa-automation.git
cd sqa-automation
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
cp .env.example .env
```
Edit `.env` and fill in your test credentials:
```
LOGIN_EMAIL=your_email@example.com
LOGIN_PASSWORD=your_password
```

### 6. Run Tests
```bash
# Run all tests
pytest

# Run only login tests
pytest tests/test_login.py

# Run only registration tests
pytest tests/test_registration.py

# Run in headless mode
HEADLESS=true pytest

# Run with verbose output
pytest -v
```

### 7. View HTML Report
After running, open:
```
reports/report.html
```

---

## Test Cases Coverage

| Module       | Total |
|--------------|-------|
| Login        | 10    |
| Registration | 12    |

Full test case documentation: `Test_Cases_SQA.xlsx`

---

## Libraries Used

| Library           | Purpose                                  |
|-------------------|------------------------------------------|
| Selenium          | Browser automation                       |
| Faker             | Generate dummy user data for registration|
| python-dotenv     | Load credentials from `.env` file        |
| pytest            | Test runner                              |
| pytest-html       | HTML test report generation              |
| webdriver-manager | Auto-download ChromeDriver               |

---

## Notes
- `conftest.py` handles driver setup and teardown automatically.
- Page Object Model (POM) pattern is used for maintainability.
- The site uses native JavaScript `alert()` dialogs for success/error feedback.
- Locators may need updating if the site's HTML structure changes.
- Set `HEADLESS=true` in `.env` for CI/CD or headless environments.
