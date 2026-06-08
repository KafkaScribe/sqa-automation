# SQA Automation Framework — Job Portal

Selenium + Python automation framework for Login and Registration testing of
[https://jobprtal.alarafafragrance.com](https://jobprtal.alarafafragrance.com).

> **Submitted by:** Nazmul Haque — SQA Automation Task for **Akaar IT**

---

## What Was Done

### Task 1: Automation (Login & Registration)
- Built a complete **Selenium WebDriver** automation framework in **Python** targeting the Job Portal web application.
- Automated the **Login Page** with 10 test cases covering valid login, invalid credentials, empty fields, malformed email, and UI navigation.
- Automated the **Registration Page** with 12 test cases covering valid registration, empty field validations, password mismatch, invalid email format, duplicate email, short password, and UI navigation.
- Used the **Page Object Model (POM)** design pattern for clean, maintainable, and reusable code.
- Integrated the **Faker** library to dynamically generate dummy user data (name, email, phone, password) for registration tests.
- Used a **`.env` file** to store all sensitive/configurable data (credentials, URLs, browser settings) — no hardcoded secrets in source code.
- Configured **pytest-html** for automatic HTML test report generation after each run.
- Handled the site's native JavaScript `alert()` dialogs for success/error feedback within page objects.

### Task 2: Test Case Documentation
- Created a detailed test case document (`Test_Cases_SQA.xlsx`) covering both Login and Registration modules.
- Used a proper test case format with Test Case ID, Description, Pre-conditions, Steps, Expected Result, and Status columns.

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
├── .env                      # Local config — ⚠️ NOT committed (contains real credentials)
├── .env.example              # Template with PLACEHOLDERS — safe to commit
├── .gitignore                # Git ignore rules
└── Test_Cases_SQA.xlsx       # Test case documentation (Excel)
```

---

## Environment Variables (Credentials)

All sensitive and configurable values are stored in a **`.env`** file which is **excluded from version control** via `.gitignore`. A template file **`.env.example`** is provided with placeholder values.

| Variable             | Description                          | Placeholder Value              | Sensitive? |
|----------------------|--------------------------------------|--------------------------------|:----------:|
| `BASE_URL`           | Target web application URL           | `https://jobprtal.alarafafragrance.com` | No  |
| `LOGIN_EMAIL`        | Email for login test account         | `your_email@example.com`       | ⚠️ **Yes** |
| `LOGIN_PASSWORD`     | Password for login test account      | `your_password`                | ⚠️ **Yes** |
| `BROWSER`            | Browser to use (chrome / firefox)    | `chrome`                       | No         |
| `HEADLESS`           | Run in headless mode (true / false)  | `false`                        | No         |
| `IMPLICIT_WAIT`      | Implicit wait timeout in seconds     | `10`                           | No         |
| `PAGE_LOAD_TIMEOUT`  | Page load timeout in seconds         | `30`                           | No         |

> ⚠️ **Important:** Never commit the `.env` file. It contains real credentials. Only `.env.example` (with placeholders) is committed to the repository. Before running tests, copy `.env.example` to `.env` and replace the placeholder values with your actual test account credentials.

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

### 5. Configure Environment (⚠️ Required)
```bash
cp .env.example .env            # Linux / macOS
copy .env.example .env          # Windows
```
Open `.env` and **replace the placeholders** with your actual test credentials:
```env
# ⚠️ Replace these placeholder values with real test account credentials
LOGIN_EMAIL=your_email@example.com
LOGIN_PASSWORD=your_password
```

### 6. Run Tests
```bash
# Run all tests (22 test cases)
pytest

# Run only login tests (10 test cases)
pytest tests/test_login.py

# Run only registration tests (12 test cases)
pytest tests/test_registration.py

# Run in headless mode (no browser window)
set HEADLESS=true && pytest      # Windows
HEADLESS=true pytest             # Linux / macOS

# Run with verbose output
pytest -v
```

### 7. View HTML Report
After running, open the auto-generated report:
```
reports/report.html
```

---

## Test Cases Coverage

| Module       | Test Cases | Scenarios Covered |
|--------------|:----------:|-------------------|
| Login        | 10         | Page load, valid login, invalid email, invalid password, empty fields, malformed email, register link navigation |
| Registration | 12         | Page load, valid registration, empty field validations (name/email/phone/password), password mismatch, invalid email format, duplicate email, short password, login link navigation |

Full test case documentation is available in: **`Test_Cases_SQA.xlsx`**

---

## Libraries Used

| Library           | Version  | Purpose                                  |
|-------------------|----------|------------------------------------------|
| Selenium          | 4.18.1   | Browser automation via WebDriver         |
| Faker             | 24.0.0   | Generate dummy user data for registration|
| python-dotenv     | 1.0.1    | Load credentials from `.env` file        |
| pytest            | 8.1.1    | Test runner and framework                |
| pytest-html       | 4.1.1    | HTML test report generation              |
| webdriver-manager | 4.0.1    | Auto-download ChromeDriver / GeckoDriver |

---

## Notes
- `conftest.py` handles WebDriver setup and teardown automatically via pytest fixtures.
- **Page Object Model (POM)** pattern is used for maintainability and reusability.
- The target site uses native JavaScript `alert()` dialogs for success/error feedback — page objects handle these automatically.
- **Faker** generates unique dummy data on every run, so registration tests won't fail due to duplicate data.
- Locators may need updating if the site's HTML structure changes.
- Set `HEADLESS=true` in `.env` for CI/CD pipelines or headless environments.
- The `.env` file is **never committed** — only `.env.example` with placeholder values is in the repository.
