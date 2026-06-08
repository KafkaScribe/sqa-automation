from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    # ── Locators (matched against the actual rendered DOM) ──
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    # Two submit buttons exist on the page ("Toggle theme" & "Log in").
    # Target the one whose visible text is "Log in".
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Log in']")
    REGISTER_LINK = (By.XPATH, "//a[contains(text(),'Register here')]")

    def __init__(self, driver, config):
        super().__init__(driver)
        self.config = config

    def open_login_page(self):
        self.open(self.config.LOGIN_URL)

    def enter_email(self, email):
        self.type(*self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.type(*self.PASSWORD_INPUT, password)

    def click_login(self):
        self.click(*self.LOGIN_BUTTON)

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    # ── Alert-based feedback helpers ──
    # The site fires a native JS alert() on login success/failure.

    def is_error_displayed(self, timeout=5):
        """Return True if a native alert with an error-like message appears."""
        text = self.get_alert_text(timeout=timeout)
        if text is None:
            return False
        # Accept the alert so subsequent actions aren't blocked
        self.accept_alert(timeout=2)
        lower = text.lower()
        return any(kw in lower for kw in [
            "fail", "error", "invalid", "incorrect", "wrong",
            "unauthorized", "not found",
        ])

    def is_success_displayed(self, timeout=5):
        """Return True if a native alert with a success-like message appears."""
        text = self.get_alert_text(timeout=timeout)
        if text is None:
            return False
        self.accept_alert(timeout=2)
        lower = text.lower()
        return any(kw in lower for kw in [
            "success", "welcome", "logged in", "login successful",
        ])

    def get_alert_message(self, timeout=5):
        """Get the alert message text, accept it, and return the text."""
        return self.accept_alert(timeout=timeout)

    def click_register_link(self):
        self.click(*self.REGISTER_LINK)

    def is_login_page(self):
        return "login" in self.safe_get_current_url().lower()
