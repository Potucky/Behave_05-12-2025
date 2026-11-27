@cart
Feature: Shopping cart
  Products added from the inventory show up in the cart badge and on the
  cart page, and they can be removed from either place.

  Background:
    Given a standard user is logged in

  @smoke
  Scenario: Adding products updates the badge and the cart
    When the user adds the following products to the cart:
      | product                 |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Then the cart badge shows 2
    When the user opens the cart
    Then the cart lists 2 products
    And the cart contains "Sauce Labs Bike Light"
    And the cart contains "Sauce Labs Bolt T-Shirt"

  Scenario Outline: A product can be removed from the inventory
    When the user adds "<product>" to the cart
    Then the cart badge shows 1
    When the user removes "<product>" from the inventory
    Then the cart badge is not shown

    Examples:
      | product                 |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |

  Scenario: A product can be removed from the cart page
    When the user adds "Sauce Labs Fleece Jacket" to the cart
    And the user adds "Sauce Labs Onesie" to the cart
    And the user opens the cart
    Then the cart lists 2 products
    When the user removes "Sauce Labs Onesie" from the cart
    Then the cart contains "Sauce Labs Fleece Jacket"
    And the cart does not contain "Sauce Labs Onesie"
    And the cart lists 1 product
