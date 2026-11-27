"""Login steps."""

from __future__ import annotations

from behave import then, use_step_matcher, when

from config.settings import settings


@when('the user logs in as "{username}"')
def step_login_as(context, username: str) -> None:
    context.pages.login.login(username, settings.password_for(username))


# Empty example cells must match, and the default parse fields do not.
use_step_matcher("re")


@when(r'the user logs in with username "(?P<username>.*)" and password "(?P<password>.*)"')
def step_login_with_credentials(context, username: str, password: str) -> None:
    context.pages.login.login(username.strip(), password.strip())


use_step_matcher("parse")


@then('the login error is "{message}"')
def step_login_error(context, message: str) -> None:
    actual = context.pages.login.error_message()
    assert actual == message, f"Login error was {actual!r}, expected {message!r}"


@then("the user remains on the login page")
def step_remains_on_login(context) -> None:
    assert context.pages.login.is_displayed(), (
        f"Login form is not visible. URL: {context.driver.current_url}"
    )
    assert "inventory.html" not in context.driver.current_url
