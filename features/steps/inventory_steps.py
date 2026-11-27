"""Inventory and product-detail steps."""

from __future__ import annotations

import re

from behave import then, when

_PRICE = re.compile(r"^\$\d+\.\d{2}$")


@then('the products heading is "{heading}"')
def step_heading(context, heading: str) -> None:
    actual = context.pages.inventory.heading()
    assert actual == heading, f"Heading was {actual!r}, expected {heading!r}"


@then("the inventory lists these products:")
def step_product_list(context) -> None:
    expected = [row["name"].strip() for row in context.table]
    actual = context.pages.inventory.names()
    assert sorted(actual) == sorted(expected), (
        f"Catalog names were {actual}, expected {expected}"
    )


@then("each product has a price and an add-to-cart button")
def step_product_details_present(context) -> None:
    cards = context.pages.inventory.cards()
    assert cards, "The inventory did not list any products"
    for card in cards:
        assert card["name"], f"A product is missing its name: {card}"
        assert _PRICE.match(card["price"]), f"Unexpected price for {card['name']}: {card['price']!r}"
        assert card["action"] == "Add to cart", (
            f"{card['name']} action was {card['action']!r}, expected 'Add to cart'"
        )


@when('the user sorts products by "{option}"')
def step_sort(context, option: str) -> None:
    context.pages.inventory.sort_by(option)


@then("product names are in {order} order")
def step_name_order(context, order: str) -> None:
    _assert_order(context.pages.inventory.names(), order, "names")


@then("product prices are in {order} order")
def step_price_order(context, order: str) -> None:
    _assert_order(context.pages.inventory.prices(), order, "prices")


@when('the user opens the product "{product}"')
def step_open_product(context, product: str) -> None:
    context.pages.inventory.open_product(product)


@then('the product details show "{product}" at "{price}"')
def step_product_details(context, product: str, price: str) -> None:
    actual_name = context.pages.product.name()
    actual_price = context.pages.product.price()
    assert actual_name == product, f"Product name was {actual_name!r}, expected {product!r}"
    assert actual_price == price, f"Product price was {actual_price!r}, expected {price!r}"


def _assert_order(actual: list, order: str, label: str) -> None:
    if order == "any":
        return
    if order == "ascending":
        expected = sorted(actual)
    elif order == "descending":
        expected = sorted(actual, reverse=True)
    else:
        raise AssertionError(f"Unknown order {order!r}")
    assert actual == expected, f"Product {label} were {actual}, expected {expected}"
