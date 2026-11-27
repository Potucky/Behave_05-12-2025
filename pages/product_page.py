"""Single product details."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.header import Header


class ProductPage(BasePage):
    NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(self)

    def name(self) -> str:
        return self.text_of(self.NAME)

    def price(self) -> str:
        return self.text_of(self.PRICE)
