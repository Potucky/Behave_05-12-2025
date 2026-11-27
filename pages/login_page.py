"""Sauce Demo login page."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def open(self) -> None:
        super().open(f"{settings.base_url}/")
        self.find(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click_until(self.LOGIN_BUTTON, self._submitted)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def is_displayed(self) -> bool:
        buttons = self.driver.find_elements(*self.LOGIN_BUTTON)
        return bool(buttons) and buttons[0].is_displayed()

    def _submitted(self, driver: WebDriver) -> bool:
        if "inventory.html" in driver.current_url:
            return True
        errors = driver.find_elements(*self.ERROR)
        return bool(errors) and errors[0].is_displayed() and bool(errors[0].text.strip())
