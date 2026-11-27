"""Page objects for the Sauce Demo store."""

from __future__ import annotations

from dataclasses import dataclass

from selenium.webdriver.remote.webdriver import WebDriver

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.product_page import ProductPage


@dataclass
class Pages:
    login: LoginPage
    inventory: InventoryPage
    product: ProductPage
    cart: CartPage
    checkout: CheckoutPage


def build_pages(driver: WebDriver) -> Pages:
    return Pages(
        login=LoginPage(driver),
        inventory=InventoryPage(driver),
        product=ProductPage(driver),
        cart=CartPage(driver),
        checkout=CheckoutPage(driver),
    )
