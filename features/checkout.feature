@checkout
Feature: Checkout
  A shopper with an item in the cart places an order. Missing information
  is rejected. The overview is checked two ways: the amounts Sauce Demo
  shows for the backpack, and a calculation that the line price, 8% tax
  rounded to the cent, and the grand total agree with each other.

  Background:
    Given a standard user is logged in
    And the user has "Sauce Labs Backpack" in the cart
    And the user is on the checkout information page

  @smoke
  Scenario: A completed checkout confirms the order
    When the user enters checkout details:
      | first_name | last_name | postal_code |
      | Vasyl      | Popovich  | 01001       |
    And the user submits the checkout information
    Then the checkout overview is displayed
    And the overview contains "Sauce Labs Backpack"
    And the item total is "$29.99"
    And the tax is "$2.40"
    And the order total is "$32.39"
    And the overview totals are consistent
    When the user finishes the checkout
    Then the confirmation header is "Thank you for your order!"
    And the confirmation text is "Your order has been dispatched, and will arrive just as fast as the pony can get there!"

  @negative
  Scenario Outline: Checkout requires every information field
    When the user enters checkout details:
      | first_name   | last_name   | postal_code   |
      | <first_name> | <last_name> | <postal_code> |
    And the user submits the checkout information
    Then the checkout error is "<message>"

    Examples:
      | first_name | last_name | postal_code | message                       |
      |            | Popovich  | 01001       | Error: First Name is required |
      | Vasyl      |           | 01001       | Error: Last Name is required  |
      | Vasyl      | Popovich  |             | Error: Postal Code is required |

  Scenario: Cancelling checkout returns to the cart
    When the user cancels checkout
    Then the cart page is displayed
    And the cart contains "Sauce Labs Backpack"
