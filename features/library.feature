Feature: Library Book Borrowing and Returning

  Scenario: Borrowing an available book
    Given the library_app has a copy of "The Hobbit"
    When I borrow "The Hobbit"
    Then I should have "The Hobbit" in my borrowed list

  Scenario: Returning a borrowed book
    Given I have "The Hobbit" borrowed from the library_app
    When I return "The Hobbit"
    Then "The Hobbit" should be available in the library_app again
