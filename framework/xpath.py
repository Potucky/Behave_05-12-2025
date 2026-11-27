"""Small XPath helpers."""

from __future__ import annotations


def literal(value: str) -> str:
    """Return ``value`` as a safe XPath string literal."""
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    parts = value.split("'")
    quoted = ", \"'\", ".join(f"'{part}'" for part in parts)
    return f"concat({quoted})"
