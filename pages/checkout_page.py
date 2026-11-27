"""Checkout information, overview, and confirmation."""

from __future__ import annotations

from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from framework.money import parse_money
from pages.base_page import BasePage
from pages.header import Header


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE = (By.CSS_SELECTOR, "[data-test='continue']")
    CANCEL = (By.CSS_SELECTOR, "[data-test='cancel']")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    FINISH = (By.CSS_SELECTOR, "[data-test='finish']")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    COMPLETE_TEXT = (By.CSS_SELECTOR, "[data-test='complete-text']")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(self)

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.POSTAL_CODE, postal_code)

    def submit_information(self) -> None:
        """Continue, then stop when the overview or a field error is showing."""
        self.click_until(self.CONTINUE, self._information_settled)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def cancel(self) -> None:
        self.click_until(self.CANCEL, lambda driver: "cart.html" in driver.current_url)

    def on_overview(self) -> bool:
        if "checkout-step-two.html" not in self.driver.current_url:
            return False
        labels = self.driver.find_elements(*self.SUBTOTAL)
        return bool(labels) and labels[0].is_displayed()

    def item_names(self) -> list[str]:
        self.find(self.ITEM_NAME)
        return [element.text.strip() for element in self.driver.find_elements(*self.ITEM_NAME)]

    def line_prices(self) -> list[Decimal]:
        self.find(self.ITEM_PRICE)
        return [parse_money(element.text) for element in self.driver.find_elements(*self.ITEM_PRICE)]

    def item_total(self) -> Decimal:
        return parse_money(self.text_of(self.SUBTOTAL))

    def tax(self) -> Decimal:
        return parse_money(self.text_of(self.TAX))

    def total(self) -> Decimal:
        return parse_money(self.text_of(self.TOTAL))

    def finish(self) -> None:
        self.click_until(
            self.FINISH,
            lambda driver: "checkout-complete.html" in driver.current_url,
        )

    def confirmation_header(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)

    def confirmation_text(self) -> str:
        return self.text_of(self.COMPLETE_TEXT)

    def _information_settled(self, driver: WebDriver) -> bool:
        if "checkout-step-two.html" in driver.current_url:
            return True
        errors = driver.find_elements(*self.ERROR)
        return bool(errors) and errors[0].is_displayed() and bool(errors[0].text.strip())
