import time

import pytest
from pages.login_page import LoginPage


class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.page = LoginPage(driver, config)
        self.config = config
        self.page.open_login_page()

    def test_TC_LGN_001_login_page_loads(self):
        """TC_LGN_001: Verify login page loads successfully"""
        assert self.page.is_login_page(), "Login page did not load"

    def test_TC_LGN_002_valid_login(self):
        """TC_LGN_002: Verify login with valid credentials"""
        self.page.login(self.config.LOGIN_EMAIL, self.config.LOGIN_PASSWORD)
        # The site may show a success alert; accept it first
        alert_text = self.page.accept_alert(timeout=5)
        time.sleep(2)  # Allow redirect to complete
        current = self.page.safe_get_current_url().lower()
        assert "login" not in current or alert_text is not None, \
            "User should be redirected or see a success alert after login"

    def test_TC_LGN_003_invalid_email(self):
        """TC_LGN_003: Verify login with invalid email"""
        self.page.login("invalid@email.com", self.config.LOGIN_PASSWORD)
        assert self.page.is_error_displayed(), "Error alert should be shown"

    def test_TC_LGN_004_invalid_password(self):
        """TC_LGN_004: Verify login with invalid password"""
        self.page.login(self.config.LOGIN_EMAIL, "WrongPass123")
        assert self.page.is_error_displayed(), "Error alert should be shown"

    def test_TC_LGN_005_empty_email(self):
        """TC_LGN_005: Verify login with empty email"""
        self.page.enter_password(self.config.LOGIN_PASSWORD)
        self.page.click_login()
        # Browser HTML5 validation prevents submission; page stays
        # Dismiss any potential alert just in case
        self.page.accept_alert(timeout=2)
        assert self.page.is_login_page(), "Should remain on login page"

    def test_TC_LGN_006_empty_password(self):
        """TC_LGN_006: Verify login with empty password"""
        self.page.enter_email(self.config.LOGIN_EMAIL)
        self.page.click_login()
        self.page.accept_alert(timeout=2)
        assert self.page.is_login_page(), "Should remain on login page"

    def test_TC_LGN_007_empty_both_fields(self):
        """TC_LGN_007: Verify login with both fields empty"""
        self.page.click_login()
        self.page.accept_alert(timeout=2)
        assert self.page.is_login_page(), "Should remain on login page"

    def test_TC_LGN_008_invalid_email_format(self):
        """TC_LGN_008: Verify login with malformed email"""
        self.page.login("notanemail", self.config.LOGIN_PASSWORD)
        # Browser HTML5 validation (type=email) should block submission
        self.page.accept_alert(timeout=2)
        assert self.page.is_login_page(), "Should remain on login page"

    def test_TC_LGN_009_register_link_visible(self):
        """TC_LGN_009: Verify register link is present on login page"""
        assert self.page.is_visible(*self.page.REGISTER_LINK), \
            "Register link should be visible"

    def test_TC_LGN_010_register_link_navigates(self):
        """TC_LGN_010: Verify register link navigates to registration page"""
        self.page.click_register_link()
        time.sleep(2)
        assert "register" in self.page.safe_get_current_url().lower(), \
            "Should navigate to register page"
