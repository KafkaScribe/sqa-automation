from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoAlertPresentException,
    UnexpectedAlertPresentException,
)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()

    def type(self, by, value, text):
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, value):
        return self.find(by, value).text

    def is_visible(self, by, value, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except (TimeoutException, Exception):
            return False

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title

    # --- Alert handling (the site uses native JS alert() for messages) ---

    def is_alert_present(self, timeout=5):
        """Check if a native browser alert dialog is present."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False

    def get_alert_text(self, timeout=5):
        """Get the text of the current alert, or None if no alert."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            return alert.text
        except TimeoutException:
            return None

    def accept_alert(self, timeout=5):
        """Accept (click OK on) the current alert if present."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except TimeoutException:
            return None

    def dismiss_alert(self, timeout=5):
        """Dismiss the current alert if present."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.dismiss()
            return True
        except TimeoutException:
            return False

    def safe_get_current_url(self):
        """Get current URL, handling any unexpected alert first."""
        try:
            return self.driver.current_url
        except UnexpectedAlertPresentException:
            self.accept_alert(timeout=2)
            return self.driver.current_url
