from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegisterPage(BasePage):
    # ── Locators (matched against the actual rendered DOM) ──
    FIRST_NAME_INPUT       = (By.NAME, "first_name")
    LAST_NAME_INPUT        = (By.NAME, "last_name")
    EMAIL_INPUT            = (By.NAME, "email")
    PHONE_INPUT            = (By.NAME, "phone")
    PASSWORD_INPUT         = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "confirm_password")
    # Two submit buttons exist ("Toggle theme" & "Register").
    REGISTER_BUTTON        = (By.XPATH,
                              "//button[@type='submit' and normalize-space()='Register']")
    LOGIN_LINK             = (By.XPATH, "//a[contains(text(),'Log in here')]")

    def __init__(self, driver, config):
        super().__init__(driver)
        self.config = config

    def open_register_page(self):
        self.open(self.config.REGISTER_URL)

    def enter_first_name(self, first_name):
        self.type(*self.FIRST_NAME_INPUT, first_name)

    def enter_last_name(self, last_name):
        self.type(*self.LAST_NAME_INPUT, last_name)

    def enter_email(self, email):
        self.type(*self.EMAIL_INPUT, email)

    def enter_phone(self, phone):
        self.type(*self.PHONE_INPUT, phone)

    def enter_password(self, password):
        self.type(*self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, password):
        self.type(*self.CONFIRM_PASSWORD_INPUT, password)

    def click_register(self):
        self.click(*self.REGISTER_BUTTON)

    def register(self, name, email, phone, password, confirm_password=None):
        """Split full name into first/last and fill all fields."""
        parts = name.split() if name else [""]
        first = parts[0]
        last = parts[1] if len(parts) > 1 else parts[0]
        self.enter_first_name(first)
        self.enter_last_name(last)
        self.enter_email(email)
        self.enter_phone(phone)
        self.enter_password(password)
        self.enter_confirm_password(confirm_password or password)
        self.click_register()

    def register_with_data(self, user_data):
        self.register(
            name=user_data["name"],
            email=user_data["email"],
            phone=user_data["phone"],
            password=user_data["password"],
        )

    # ── Alert-based feedback helpers ──
    # The site fires a native JS alert() on registration success/failure.

    def is_error_displayed(self, timeout=5):
        """Return True if a native alert with an error-like message appears."""
        text = self.get_alert_text(timeout=timeout)
        if text is None:
            return False
        self.accept_alert(timeout=2)
        lower = text.lower()
        return any(kw in lower for kw in [
            "fail", "error", "invalid", "incorrect", "already",
            "exists", "taken", "mismatch", "short", "required",
        ])

    def is_success_displayed(self, timeout=5):
        """Return True if a native alert with a success-like message appears."""
        text = self.get_alert_text(timeout=timeout)
        if text is None:
            return False
        self.accept_alert(timeout=2)
        lower = text.lower()
        return any(kw in lower for kw in [
            "success", "registered", "created", "welcome",
        ])

    def get_alert_message(self, timeout=5):
        """Get the alert message text, accept it, and return the text."""
        return self.accept_alert(timeout=timeout)

    def click_login_link(self):
        self.click(*self.LOGIN_LINK)

    def is_register_page(self):
        return "register" in self.safe_get_current_url().lower()
