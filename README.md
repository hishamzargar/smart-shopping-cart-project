# Smart Shopping Cart & Recommendation Engine

This project simulates core features of an e-commerce platform's backend, focusing on product management, cart operations, discounts, and basic product recommendations. It serves as a hands-on exercise to apply common data structures and algorithms (often seen in LeetCode problems) in a practical, interactive context.

## Features Implemented

* **Product Catalog Management:**
    * View a list of available products with details (ID, Name, Price).
    * Search products by name keyword (case-insensitive).
    * Sort products by name or price (ascending/descending).
    * Filter products to show only those within a specific price range.

* **Shopping Cart Operations:**
    * Add items to the shopping cart using Product ID and desired quantity.
    * Remove items from the shopping cart.
    * View the current contents of the cart, including item details and quantities.

* **Discount & Pricing Engine:**
    * Calculate the cart total accurately.
    * Apply various types of discounts automatically:
        * **Buy One Get One Free (BOGO):** For specifically designated items.
        * **Time-Limited Flash Sales:** Offer percentage or fixed discounts on specific items during defined time windows.
        * **Tiered Discounts:** Apply increasing percentage discounts based on the cart's subtotal (calculated after item-specific discounts).
    * Display a clear breakdown of the subtotal, applied discounts, and the final payable total.

* **Simple Recommendation Engine:**
    * Tracks which items are frequently bought together within the same transaction (maintains co-purchase history).
    * Provides basic product recommendations ("You might also be interested in...") based on the items currently present in the user's cart and the learned co-purchase history.

## LeetCode Concepts Applied

This project provides practical application for several fundamental concepts often encountered in coding challenges and real-world development:

* **Lists/Arrays:** Used for storing the initial product catalog structure.
* **Hashing (Python Dictionaries & Sets):** Utilized extensively for efficiency:
    * Creating an efficient product lookup map by ID (`O(1)` average time complexity).
    * Implementing the shopping cart itself (mapping Product ID to quantity for fast updates/access).
    * Storing BOGO eligible item IDs (using sets for efficient `O(1)` membership checking).
    * Storing and accessing the co-purchase history counts for the recommendation engine.
* **String Manipulation:** Used in the product search feature.
* **Sorting Algorithms:** Employing Python's built-in `sorted()` function with custom `lambda` key functions to sort the product list based on different criteria (name, price).
* **Conditional Logic:** Implementing the complex rules for applying various discounts based on item eligibility, time windows, and cart value thresholds.
* **Date/Time Handling (`datetime` module):** Used for checking the validity windows for Flash Sales.
* **Iteration & Basic Algorithms:** Essential for traversing lists and dictionaries to perform calculations (like total price), filtering, searching, and updating history.
* **(Conceptual) Graphs:** The recommendation engine implicitly models products as nodes and co-purchases as weighted edges between them. Generating recommendations involves traversing these implicit connections.

## How to Run

1.  **Prerequisites:** Ensure you have Python 3 installed on your system.
2.  **Get the Code:** Clone the repository or download the `main.py` file.
3.  **Navigate:** Open your terminal or command prompt and navigate to the directory containing `main.py`.
4.  **Execute:** Run the script using the command:
    ```bash
    python main.py
    ```
5.  **Interact:** Follow the instructions presented in the console menu to interact with the shopping cart system.

## Project Structure

* `main.py`: The primary Python file containing all the application logic, data structures, functions, and the interactive console interface.
* `.gitignore`: (Optional) Specifies intentionally untracked files for Git version control.
* `README.md`: This documentation file.

## Potential Future Enhancements

* **Inventory Management:** Track stock levels and prevent ordering unavailable items.
* **Persistence:** Save and load the product catalog and co-purchase history to/from a file (e.g., JSON) so data isn't lost when the program closes.
* **User Accounts:** Add basic user registration/login and associate carts/history with specific users.
* **Undo/Redo:** Implement undo/redo functionality for cart actions using Stacks.
* **Order Fulfillment Simulation:** Use a Queue data structure to manage completed orders.
* **Unit Testing:** Add automated tests to verify the correctness of different functions (e.g., discount calculation, cart updates).
* **Refactoring:** Improve code organization by introducing classes (e.g., `Product`, `ShoppingCart`, `DiscountRule`) instead of relying solely on dictionaries and functions.