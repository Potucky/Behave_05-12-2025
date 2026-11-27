"""Shopping cart."""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from framework.xpath import literal
from pages.base_page import BasePage
from pages.header import Header


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    NAME = (By.CSS_SELECTOR, ".cart_item [data-test='inventory-item-name']")
    CHECKOUT = (By.CSS_SELECTOR, "[data-test='checkout']")

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.header = Header(self)

    def is_displayed(self) -> bool:
        if "cart.html" not in self.driver.current_url:
            return False
        titles = self.driver.find_elements(*self.TITLE)
        return bool(titles) and titles[0].is_displayed() and titles[0].text.strip() == "Your Cart"

    def names(self) -> list[str]:
        return [element.text.strip() for element in self.driver.find_elements(*self.NAME)]

    def wait_for_names(self) -> list[str]:
        self.find(self.NAME)
        return self.names()

    def remove(self, name: str) -> None:
        def _gone(driver: WebDriver) -> bool:
            buttons = driver.find_elements(By.XPATH, _remove_xpath(name))
            if not buttons:
                return True
            self._scroll_into_view(buttons[0])
            driver.execute_script("arguments[0].click();", buttons[0])
            return False

        self.wait.until(_gone)

    def checkout(self) -> None:
        self.click_until(
            self.CHECKOUT,
            lambda driver: "checkout-step-one.html" in driver.current_url,
        )


def _remove_xpath(name: str) -> str:
    return (
        f"//*[@class='cart_item'][.//*[@data-test='inventory-item-name' and normalize-space()={literal(name)}]]"
        "//button"
    )
