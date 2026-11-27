"""Store header: menu and cart badge. Present on every page after login."""

from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class Header:
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.CSS_SELECTOR, "[data-test='logout-sidebar-link']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-button']")

    def __init__(self, page: BasePage) -> None:
        self.page = page

    def cart_count(self) -> int:
        badges = [
            badge
            for badge in self.page.driver.find_elements(*self.CART_BADGE)
            if badge.is_displayed() and badge.text.strip()
        ]
        if not badges:
            return 0
        return int(badges[0].text.strip())

    def wait_for_count(self, expected: int) -> None:
        self.page.wait.until(lambda _driver: self.cart_count() == expected)

    def open_cart(self) -> None:
        self.page.click_until(
            self.CART_LINK,
            lambda driver: "cart.html" in driver.current_url,
        )

    def logout(self) -> None:
        self.page.click_until(
            self.MENU,
            lambda driver: _visible(driver, self.LOGOUT),
        )
        self.page.click_until(
            self.LOGOUT,
            lambda driver: _visible(driver, self.LOGIN_BUTTON),
        )


def _visible(driver, locator) -> bool:
    elements = driver.find_elements(*locator)
    return bool(elements) and elements[0].is_displayed()
