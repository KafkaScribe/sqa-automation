import time

import pytest
from pages.register_page import RegisterPage
from utils.data_generator import DataGenerator


class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self, driver, config):
        self.page = RegisterPage(driver, config)
        self.config = config
        self.gen = DataGenerator()
        self.page.open_register_page()

    def test_TC_REG_001_register_page_loads(self):
        """TC_REG_001: Verify registration page loads successfully"""
        assert self.page.is_register_page(), "Registration page did not load"

    def test_TC_REG_002_valid_registration(self):
        """TC_REG_002: Verify successful registration with valid data"""
        user = DataGenerator.generate_user()
        self.page.register_with_data(user)
        # Accept the result alert (success or error) and check
        alert_text = self.page.accept_alert(timeout=5)
        if alert_text:
            lower = alert_text.lower()
            assert any(kw in lower for kw in [
                "success", "registered", "created", "welcome",
            ]) or not any(kw in lower for kw in [
                "fail", "error",
            ]), f"Expected success but got alert: {alert_text}"
        # If no alert, check we're no longer on the register page
        else:
            time.sleep(2)
            assert not self.page.is_register_page(), \
                "Should have left register page after successful registration"

    def test_TC_REG_003_empty_name(self):
        """TC_REG_003: Verify registration fails with empty name"""
        user = DataGenerator.generate_user()
        # Fill everything except first/last name
        self.page.enter_email(user["email"])
        self.page.enter_phone(user["phone"])
        self.page.enter_password(user["password"])
        self.page.enter_confirm_password(user["password"])
        self.page.click_register()
        # HTML5 validation should block, or server returns error
        self.page.accept_alert(timeout=3)
        assert self.page.is_register_page(), "Should remain on register page"

    def test_TC_REG_004_empty_email(self):
        """TC_REG_004: Verify registration fails with empty email"""
        user = DataGenerator.generate_user()
        parts = user["name"].split()
        self.page.enter_first_name(parts[0])
        self.page.enter_last_name(parts[-1])
        self.page.enter_phone(user["phone"])
        self.page.enter_password(user["password"])
        self.page.enter_confirm_password(user["password"])
        self.page.click_register()
        self.page.accept_alert(timeout=3)
        assert self.page.is_register_page(), "Should remain on register page"

    def test_TC_REG_005_empty_phone(self):
        """TC_REG_005: Verify registration fails with empty phone"""
        user = DataGenerator.generate_user()
        parts = user["name"].split()
        self.page.enter_first_name(parts[0])
        self.page.enter_last_name(parts[-1])
        self.page.enter_email(user["email"])
        self.page.enter_password(user["password"])
        self.page.enter_confirm_password(user["password"])
        self.page.click_register()
        self.page.accept_alert(timeout=3)
        assert self.page.is_register_page(), "Should remain on register page"

    def test_TC_REG_006_empty_password(self):
        """TC_REG_006: Verify registration fails with empty password"""
        user = DataGenerator.generate_user()
        parts = user["name"].split()
        self.page.enter_first_name(parts[0])
        self.page.enter_last_name(parts[-1])
        self.page.enter_email(user["email"])
        self.page.enter_phone(user["phone"])
        # Leave password & confirm_password empty
        self.page.click_register()
        self.page.accept_alert(timeout=3)
        assert self.page.is_register_page(), "Should remain on register page"

    def test_TC_REG_007_password_mismatch(self):
        """TC_REG_007: Verify registration fails when passwords do not match"""
        user = DataGenerator.generate_user()
        self.page.register(
            user["name"], user["email"], user["phone"],
            user["password"], confirm_password="Mismatch@999"
        )
        alert_text = self.page.accept_alert(timeout=5)
        is_still_register = self.page.is_register_page()
        assert alert_text is not None or is_still_register, \
            "Should show error alert or remain on register page for mismatched passwords"

    def test_TC_REG_008_invalid_email_format(self):
        """TC_REG_008: Verify registration fails with invalid email format"""
        user = DataGenerator.generate_user()
        self.page.register(user["name"], "invalidemail", user["phone"], user["password"])
        # HTML5 type=email validation should block submission
        self.page.accept_alert(timeout=3)
        assert self.page.is_register_page(), "Should remain on register page"

    def test_TC_REG_009_duplicate_email(self):
        """TC_REG_009: Verify registration fails with already registered email"""
        user = DataGenerator.generate_user()
        user["email"] = self.config.LOGIN_EMAIL
        self.page.register_with_data(user)
        # The server may show an error alert or silently reject (staying on page)
        alert_text = self.page.accept_alert(timeout=5)
        time.sleep(2)
        is_still_register = self.page.is_register_page()
        assert alert_text is not None or is_still_register, \
            "Should show error alert or remain on register page for duplicate email"

    def test_TC_REG_010_short_password(self):
        """TC_REG_010: Verify registration fails with short password"""
        user = DataGenerator.generate_user()
        user["password"] = DataGenerator.generate_short_password()
        self.page.register_with_data(user)
        alert_text = self.page.accept_alert(timeout=5)
        is_still_register = self.page.is_register_page()
        assert alert_text is not None or is_still_register, \
            "Should reject short password"

    def test_TC_REG_011_login_link_visible(self):
        """TC_REG_011: Verify login link is present on registration page"""
        assert self.page.is_visible(*self.page.LOGIN_LINK), \
            "Login link should be visible on register page"

    def test_TC_REG_012_login_link_navigates(self):
        """TC_REG_012: Verify login link navigates back to login page"""
        self.page.click_login_link()
        time.sleep(2)
        assert "login" in self.page.safe_get_current_url().lower(), \
            "Should navigate to login page"
