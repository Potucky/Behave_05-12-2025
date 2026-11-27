@login
Feature: Customer login
  A shopper signs in with the public Sauce Demo accounts before browsing
  the store, and can sign out again. Rejected attempts stay on the login
  page and explain what is wrong.

  @smoke
  Scenario: Standard user signs in
    Given the login page is open
    When the user logs in as "standard_user"
    Then the inventory page is displayed
    And the products heading is "Products"

  @smoke
  Scenario: Standard user can log out
    Given a standard user is logged in
    When the user logs out
    Then the login page is displayed

  @negative
  Scenario Outline: Invalid credentials are rejected
    Given the login page is open
    When the user logs in with username "<username>" and password "<password>"
    Then the login error is "<message>"
    And the user remains on the login page

    # The locked-out password is the public demo password printed on the login page.
    Examples:
      | username        | password     | message                                                                     |
      |                 |              | Epic sadface: Username is required                                          |
      | standard_user   |              | Epic sadface: Password is required                                          |
      | standard_user   | wrong_pass   | Epic sadface: Username and password do not match any user in this service  |
      | locked_out_user | secret_sauce | Epic sadface: Sorry, this user has been locked out.                         |
