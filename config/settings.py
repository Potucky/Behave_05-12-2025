"""Project settings.

Values come from the process environment, with defaults that point at the
public Sauce Demo store. A local `.env` file is loaded when it exists and
does not override variables that are already set (CI can export them).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env", override=False)


def _flag(name: str, default: str) -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    raw = os.getenv(name, str(default)).strip()
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got {raw!r}") from exc
    if value <= 0:
        raise RuntimeError(f"{name} must be positive, got {value}")
    return value


def _decimal(name: str, default: str) -> Decimal:
    raw = os.getenv(name, default).strip()
    try:
        return Decimal(raw)
    except Exception as exc:
        raise RuntimeError(f"{name} must be a decimal, got {raw!r}") from exc


@dataclass(frozen=True)
class Settings:
    base_url: str
    browser: str
    headless: bool
    explicit_wait: int
    page_load_timeout: int
    window_width: int
    window_height: int
    username: str
    password: str
    locked_username: str
    tax_rate: Decimal
    chrome_binary: str | None

    @classmethod
    def from_env(cls) -> Settings:
        binary = os.getenv("CHROME_BINARY", "").strip() or None
        return cls(
            base_url=os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/"),
            browser=os.getenv("BROWSER", "chrome").strip().lower(),
            headless=_flag("HEADLESS", "true"),
            explicit_wait=_int("EXPLICIT_WAIT", 20),
            page_load_timeout=_int("PAGE_LOAD_TIMEOUT", 45),
            window_width=_int("WINDOW_WIDTH", 1440),
            window_height=_int("WINDOW_HEIGHT", 1080),
            username=os.getenv("SAUCE_USERNAME", "standard_user").strip(),
            password=os.getenv("SAUCE_PASSWORD", "secret_sauce"),
            locked_username=os.getenv("SAUCE_LOCKED_USERNAME", "locked_out_user").strip(),
            tax_rate=_decimal("TAX_RATE", "0.08"),
            chrome_binary=binary,
        )

    def password_for(self, username: str) -> str:
        """Password for a known public demo account.

        Every Sauce Demo user shares the password published on the login page.
        """
        known = {self.username, "standard_user", self.locked_username, "locked_out_user"}
        if username not in known:
            raise KeyError(
                f"No password configured for {username!r}. "
                "Set SAUCE_USERNAME or pass the password in the scenario."
            )
        return self.password


settings = Settings.from_env()
