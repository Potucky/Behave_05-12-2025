"""Steps shared by more than one feature."""

from __future__ import annotations

from behave import given, then, when

from config.settings import settings


@given("the login page is open")
def step_login_page_open(context) -> None:
    context.pages.login.open()


@given("a standard user is logged in")
def step_standard_user_logged_in(context) -> None:
    context.pages.login.open()
    context.pages.login.login(settings.username, settings.password)
    assert context.pages.inventory.is_displayed(), (
        f"Inventory did not open for {settings.username}. URL: {context.driver.current_url}"
    )


@when("the user logs out")
def step_logout(context) -> None:
    context.pages.inventory.header.logout()


@then("the inventory page is displayed")
def step_inventory_displayed(context) -> None:
    assert context.pages.inventory.is_displayed(), (
        f"Expected the inventory page. URL: {context.driver.current_url}"
    )


@then("the login page is displayed")
def step_login_displayed(context) -> None:
    assert context.pages.login.is_displayed(), (
        f"Expected the login page. URL: {context.driver.current_url}"
    )


@then("the cart page is displayed")
def step_cart_displayed(context) -> None:
    assert context.pages.cart.is_displayed(), (
        f"Expected the cart page. URL: {context.driver.current_url}"
    )
