"""Product listing."""

from __future__ import annotations

from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select

from framework.money import parse_money
from framework.xpath import literal
from pages.base_page import BasePage
from pages.header import Header


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM = (By.CSS_SELECTOR, "[data-test='inventory-list'] [data-test='inventory-item']")
    NAME = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRICE = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    ACTIVE_SORT = (By.CSS_SELECTOR, "[data-test='active-option']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(self)

    def is_displayed(self) -> bool:
        if "inventory.html" not in self.driver.current_url:
            return False
        titles = self.driver.find_elements(*self.TITLE)
        return bool(titles) and titles[0].is_displayed() and titles[0].text.strip() == "Products"

    def heading(self) -> str:
        return self.text_of(self.TITLE)

    def cards(self) -> list[dict[str, str]]:
        self.find(self.ITEM)
        cards: list[dict[str, str]] = []
        for item in self.driver.find_elements(*self.ITEM):
            cards.append(
                {
                    "name": item.find_element(*self.NAME).text.strip(),
                    "price": item.find_element(*self.PRICE).text.strip(),
                    "action": item.find_element(By.TAG_NAME, "button").text.strip(),
                }
            )
        return cards

    def names(self) -> list[str]:
        self.find(self.NAME)
        return [element.text.strip() for element in self.driver.find_elements(*self.NAME)]

    def prices(self) -> list[Decimal]:
        self.find(self.PRICE)
        return [parse_money(element.text) for element in self.driver.find_elements(*self.PRICE)]

    def sort_by(self, label: str) -> None:
        def _applied(driver: WebDriver) -> bool:
            active = driver.find_elements(*self.ACTIVE_SORT)
            if active and active[0].text.strip() == label:
                return True
            Select(driver.find_element(*self.SORT)).select_by_visible_text(label)
            return False

        self.wait.until(_applied)

    def add(self, name: str) -> None:
        self._set_action(name, "remove")

    def remove(self, name: str) -> None:
        self._set_action(name, "add to cart")

    def open_product(self, name: str) -> None:
        def _opened(driver: WebDriver) -> bool:
            return "inventory-item.html" in driver.current_url

        def _click_name(driver: WebDriver) -> bool:
            if _opened(driver):
                return True
            item = driver.find_element(By.XPATH, _item_xpath(name))
            link = item.find_element(By.XPATH, ".//a[.//*[@data-test='inventory-item-name']]")
            self._scroll_into_view(link)
            driver.execute_script("arguments[0].click();", link)
            return False

        self.wait.until(_click_name)

    def _set_action(self, name: str, label: str) -> None:
        expected = label.lower()

        def _done(driver: WebDriver) -> bool:
            button = driver.find_element(By.XPATH, _item_xpath(name)).find_element(By.TAG_NAME, "button")
            if button.text.strip().lower() == expected:
                return True
            self._scroll_into_view(button)
            driver.execute_script("arguments[0].click();", button)
            return False

        self.wait.until(_done)

    def wait_for_badge(self, count: int) -> None:
        self.header.wait_for_count(count)


def _item_xpath(name: str) -> str:
    return (
        "//*[@data-test='inventory-list']//*[@data-test='inventory-item']"
        f"[.//*[@data-test='inventory-item-name' and normalize-space()={literal(name)}]]"
    )
