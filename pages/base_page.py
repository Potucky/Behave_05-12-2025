"""Shared waits and actions.

Clicks are dispatched on the element and then the caller waits until the UI
shows the result (a new URL, a new button label, an error). Headless Chrome
sometimes delivers a WebDriver pointer click that the React page ignores, so
a click is repeated only while that result is still missing.

Checkout and login fields are controlled inputs. ``fill`` types with
``send_keys`` and, when the value does not stick, sets it through the input's
native value setter and an ``input`` event. Either way the call returns only
after the field shows the expected value.
"""

from __future__ import annotations

from collections.abc import Callable

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings

Locator = tuple[str, str]
Predicate = Callable[[WebDriver], bool]


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int | None = None) -> None:
        self.driver = driver
        self.timeout = settings.explicit_wait if timeout is None else timeout
        self.wait = WebDriverWait(
            driver,
            self.timeout,
            poll_frequency=0.25,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        )

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text.strip()

    def fill(self, locator: Locator, text: str) -> None:
        expected = text

        def _applied(driver: WebDriver) -> bool:
            element = driver.find_element(*locator)
            if (element.get_attribute("value") or "") == expected:
                return True
            self._scroll_into_view(element)
            try:
                element.clear()
                if expected:
                    element.send_keys(expected)
            except StaleElementReferenceException:
                return False
            if (element.get_attribute("value") or "") == expected:
                return True
            self._set_controlled_input(element, expected)
            return (element.get_attribute("value") or "") == expected

        self.wait.until(_applied)

    def click_until(self, locator: Locator, predicate: Predicate) -> None:
        """Click ``locator`` until ``predicate`` is true.

        The predicate is checked before every click, so a click that already
        worked is not sent again on the next poll.
        """

        def _done(driver: WebDriver) -> bool:
            if predicate(driver):
                return True
            element = driver.find_element(*locator)
            self._scroll_into_view(element)
            driver.execute_script("arguments[0].click();", element)
            return False

        self.wait.until(_done)

    def _scroll_into_view(self, element: WebElement) -> None:
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )

    def _set_controlled_input(self, element: WebElement, value: str) -> None:
        self.driver.execute_script(
            """
            const element = arguments[0];
            const value = arguments[1];
            const descriptor = Object.getOwnPropertyDescriptor(
                Object.getPrototypeOf(element),
                "value"
            );
            descriptor.set.call(element, value);
            element.dispatchEvent(new Event("input", { bubbles: true }));
            element.dispatchEvent(new Event("change", { bubbles: true }));
            """,
            element,
            value,
        )
