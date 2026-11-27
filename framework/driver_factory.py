"""Create the Chrome session used by every scenario."""

from __future__ import annotations

import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings

logger = logging.getLogger(__name__)


def create_driver() -> WebDriver:
    if settings.browser != "chrome":
        raise RuntimeError(
            f"Unsupported BROWSER={settings.browser!r}. This suite runs on Chrome."
        )

    options = Options()
    if settings.chrome_binary:
        options.binary_location = settings.chrome_binary
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-search-engine-choice-screen")
    options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
    options.add_argument("--window-position=0,0")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        },
    )

    logger.debug(
        "Starting Chrome headless=%s window=%sx%s",
        settings.headless,
        settings.window_width,
        settings.window_height,
    )
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(settings.page_load_timeout)
    return driver
