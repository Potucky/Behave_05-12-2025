"""Checks for the checkout arithmetic, independent of the browser."""

from __future__ import annotations

import unittest
from decimal import Decimal

from framework.money import parse_money, tax_on


class ParseMoneyTests(unittest.TestCase):
    def test_plain_price(self) -> None:
        self.assertEqual(parse_money("$29.99"), Decimal("29.99"))

    def test_labeled_summary(self) -> None:
        self.assertEqual(parse_money("Item total: $29.99"), Decimal("29.99"))
        self.assertEqual(parse_money("Tax: $2.40"), Decimal("2.40"))
        self.assertEqual(parse_money("Total: $32.39"), Decimal("32.39"))

    def test_thousands_separator(self) -> None:
        self.assertEqual(parse_money("$1,299.99"), Decimal("1299.99"))

    def test_rejects_text_without_an_amount(self) -> None:
        with self.assertRaises(ValueError):
            parse_money("Thank you for your order!")


class TaxTests(unittest.TestCase):
    def test_backpack_matches_sauce_demo(self) -> None:
        item_total = Decimal("29.99")
        tax = tax_on(item_total, Decimal("0.08"))
        self.assertEqual(tax, Decimal("2.40"))
        self.assertEqual(item_total + tax, Decimal("32.39"))

    def test_half_up_to_the_cent(self) -> None:
        self.assertEqual(tax_on(Decimal("15.99"), Decimal("0.08")), Decimal("1.28"))

    def test_two_items(self) -> None:
        item_total = Decimal("29.99") + Decimal("15.99")
        self.assertEqual(item_total, Decimal("45.98"))
        self.assertEqual(tax_on(item_total, Decimal("0.08")), Decimal("3.68"))


if __name__ == "__main__":
    unittest.main()
