"""Browser lifecycle for every scenario, and a screenshot when one fails."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import allure
from behave.model_core import Status

from config.settings import settings
from framework.driver_factory import create_driver
from pages import build_pages

REPORTS = Path("reports")
SCREENSHOTS = REPORTS / "screenshots"
ALLURE_RESULTS = REPORTS / "allure-results"


def before_all(context) -> None:
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s %(name)s - %(message)s",
        force=True,
    )
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)
    context.settings = settings


def before_scenario(context, scenario) -> None:
    context.driver = create_driver()
    context.pages = build_pages(context.driver)


def after_scenario(context, scenario) -> None:
    driver = getattr(context, "driver", None)
    if driver is None:
        return
    try:
        if scenario.status == Status.failed:
            _capture_failure(context, scenario)
    finally:
        driver.quit()


def after_all(context) -> None:
    ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)
    lines = [
        f"Browser={settings.browser}",
        f"Headless={settings.headless}",
        f"BaseUrl={settings.base_url}",
        f"ExplicitWaitSeconds={settings.explicit_wait}",
        f"TaxRate={settings.tax_rate}",
    ]
    (ALLURE_RESULTS / "environment.properties").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _capture_failure(context, scenario) -> None:
    driver = context.driver
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", scenario.name).strip("-").lower()[:80]
    path = SCREENSHOTS / f"{slug}-{scenario.line}.png"
    png = driver.get_screenshot_as_png()
    path.write_bytes(png)
    logging.error("Failed %s at %s. Screenshot: %s", scenario.name, driver.current_url, path)
    try:
        allure.attach(png, name=scenario.name, attachment_type=allure.attachment_type.PNG)
        allure.attach(driver.current_url, name="url", attachment_type=allure.attachment_type.TEXT)
    except Exception:
        logging.warning("Could not attach the failure screenshot to Allure", exc_info=True)
