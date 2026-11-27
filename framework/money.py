"""Parse and check the money amounts Sauce Demo prints."""

from __future__ import annotations

import re
from decimal import Decimal, ROUND_HALF_UP

from config.settings import settings

_AMOUNT = re.compile(r"-?\$?\s*([0-9][0-9,]*(?:\.[0-9]{2})?)")


def parse_money(text: str) -> Decimal:
    """Return the first currency amount in ``text`` as dollars and cents.

    Accepts ``$29.99`` and labeled strings such as ``Item total: $29.99``.
    """
    match = _AMOUNT.search(text.replace(" ", ""))
    if match is None:
        raise ValueError(f"No money amount in {text!r}")
    return Decimal(match.group(1).replace(",", ""))


def tax_on(amount: Decimal, rate: Decimal | None = None) -> Decimal:
    """Tax rounded half-up to the cent. Sauce Demo uses 8%."""
    applied = settings.tax_rate if rate is None else rate
    return (amount * applied).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
