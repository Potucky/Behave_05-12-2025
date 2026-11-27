@inventory
Feature: Product inventory
  A signed-in shopper sees the demo catalog, can sort it, and can open a
  product to confirm its name and price.

  Background:
    Given a standard user is logged in

  @smoke
  Scenario: The catalog lists the demo products
    Then the inventory lists these products:
      | name                                  |
      | Sauce Labs Backpack                   |
      | Sauce Labs Bike Light                 |
      | Sauce Labs Bolt T-Shirt               |
      | Sauce Labs Fleece Jacket              |
      | Sauce Labs Onesie                     |
      | Test.allTheThings() T-Shirt (Red)     |
    And each product has a price and an add-to-cart button

  @sorting
  Scenario Outline: The shopper can sort the catalog
    When the user sorts products by "<option>"
    Then product names are in <name_order> order
    And product prices are in <price_order> order

    Examples:
      | option              | name_order | price_order |
      | Name (A to Z)       | ascending  | any         |
      | Name (Z to A)       | descending | any         |
      | Price (low to high) | any        | ascending   |
      | Price (high to low) | any        | descending  |

  @smoke
  Scenario: Opening a product shows its name and price
    When the user opens the product "Sauce Labs Backpack"
    Then the product details show "Sauce Labs Backpack" at "$29.99"
