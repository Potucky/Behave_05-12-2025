"""Checkout steps."""

from __future__ import annotations

from decimal import Decimal

from behave import given, then, when

from framework.money import parse_money, tax_on


@given("the user is on the checkout information page")
def step_on_information_page(context) -> None:
    context.pages.inventory.header.open_cart()
    context.pages.cart.checkout()


@when("the user enters checkout details:")
def step_enter_details(context) -> None:
    row = context.table[0]
    context.pages.checkout.fill_information(
        row["first_name"].strip(),
        row["last_name"].strip(),
        row["postal_code"].strip(),
    )


@when("the user submits the checkout information")
def step_submit_information(context) -> None:
    context.pages.checkout.submit_information()


@then('the checkout error is "{message}"')
def step_checkout_error(context, message: str) -> None:
    actual = context.pages.checkout.error_message()
    assert actual == message, f"Checkout error was {actual!r}, expected {message!r}"


@then("the checkout overview is displayed")
def step_overview(context) -> None:
    assert context.pages.checkout.on_overview(), (
        f"Expected the checkout overview. URL: {context.driver.current_url}. "
        f"Page heading: {_heading(context)!r}"
    )


@then('the overview contains "{product}"')
def step_overview_contains(context, product: str) -> None:
    names = context.pages.checkout.item_names()
    assert product in names, f"Expected {product!r} on the overview, got {names}"


@then('the item total is "{amount}"')
def step_item_total(context, amount: str) -> None:
    _assert_money(context.pages.checkout.item_total(), amount, "item total")


@then('the tax is "{amount}"')
def step_tax(context, amount: str) -> None:
    _assert_money(context.pages.checkout.tax(), amount, "tax")


@then('the order total is "{amount}"')
def step_order_total(context, amount: str) -> None:
    _assert_money(context.pages.checkout.total(), amount, "order total")


@then("the overview totals are consistent")
def step_totals_consistent(context) -> None:
    prices = context.pages.checkout.line_prices()
    item_total = context.pages.checkout.item_total()
    tax = context.pages.checkout.tax()
    total = context.pages.checkout.total()
    summed = sum(prices, Decimal("0.00"))
    expected_tax = tax_on(item_total)
    assert summed == item_total, f"Line prices {prices} sum to {summed}, item total is {item_total}"
    assert tax == expected_tax, f"Tax was {tax}, expected {expected_tax} on {item_total}"
    assert total == item_total + tax, f"Total was {total}, expected {item_total + tax}"


@when("the user finishes the checkout")
def step_finish(context) -> None:
    context.pages.checkout.finish()


@then('the confirmation header is "{header}"')
def step_confirmation_header(context, header: str) -> None:
    actual = context.pages.checkout.confirmation_header()
    assert actual == header, f"Confirmation header was {actual!r}, expected {header!r}"


@then('the confirmation text is "{text}"')
def step_confirmation_text(context, text: str) -> None:
    actual = context.pages.checkout.confirmation_text()
    assert actual == text, f"Confirmation text was {actual!r}, expected {text!r}"


@when("the user cancels checkout")
def step_cancel(context) -> None:
    context.pages.checkout.cancel()


def _assert_money(actual: Decimal, expected_text: str, label: str) -> None:
    expected = parse_money(expected_text)
    assert actual == expected, f"The {label} was {actual}, expected {expected}"


def _heading(context) -> str:
    titles = context.driver.find_elements(*context.pages.checkout.TITLE)
    if not titles:
        return ""
    return titles[0].text.strip()
