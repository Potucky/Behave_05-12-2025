"""Cart steps."""

from __future__ import annotations

from behave import given, then, when


@given('the user has "{product}" in the cart')
@when('the user adds "{product}" to the cart')
def step_add_product(context, product: str) -> None:
    context.pages.inventory.add(product)


@when("the user adds the following products to the cart:")
def step_add_products(context) -> None:
    for row in context.table:
        context.pages.inventory.add(row["product"].strip())


@then("the cart badge shows {count:d}")
def step_badge(context, count: int) -> None:
    context.pages.inventory.wait_for_badge(count)
    actual = context.pages.inventory.header.cart_count()
    assert actual == count, f"Cart badge was {actual}, expected {count}"


@then("the cart badge is not shown")
def step_badge_hidden(context) -> None:
    context.pages.inventory.wait_for_badge(0)


@when('the user removes "{product}" from the inventory')
def step_remove_from_inventory(context, product: str) -> None:
    context.pages.inventory.remove(product)


@when("the user opens the cart")
def step_open_cart(context) -> None:
    context.pages.inventory.header.open_cart()


@then('the cart contains "{product}"')
def step_cart_contains(context, product: str) -> None:
    names = context.pages.cart.wait_for_names()
    assert product in names, f"Expected {product!r} in the cart, got {names}"


@then("the cart lists {count:d} product")
@then("the cart lists {count:d} products")
def step_cart_count(context, count: int) -> None:
    if count == 0:
        names = context.pages.cart.names()
    else:
        names = context.pages.cart.wait_for_names()
    assert len(names) == count, f"Cart had {names}, expected {count} products"


@then('the cart does not contain "{product}"')
def step_cart_excludes(context, product: str) -> None:
    names = context.pages.cart.names()
    assert product not in names, f"{product!r} is still in the cart: {names}"


@when('the user removes "{product}" from the cart')
def step_remove_from_cart(context, product: str) -> None:
    context.pages.cart.remove(product)
