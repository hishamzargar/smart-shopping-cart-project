# --- Product Catalog ---
# Using a list of dictionaries to represent products
# Each dictionary has 'id', 'name', and 'price'

products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse", "price": 25.50},
    {"id": 3, "name": "Keyboard", "price": 75.00},
    {"id": 4, "name": "Monitor", "price": 300.00},
    {"id": 5, "name": "Webcam", "price": 50.00},
    {"id": 6, "name": "Docking Station", "price": 150.00},
]

# --- Data Structures ---

# For efficient lookup by product ID (LeetCode: Hashing)
# Create a dictionary mapping product ID to the product dictionary
product_lookup = {product['id']: product for product in products}


# The shopping cart (LeetCode: Hashing)
# Dictionary mapping product ID to quantity
shopping_cart = {}   # Example: {1: 2, 3: 1} means 2 Laptops, 1 Keyboard

# --- Core Functions ---

def display_products(product_list):
    """Prints the details of all available products."""
    print("\n--- Available Products ---")
    if not product_list:
        print("No products available")
        return 
    for product in product_list:
        print(f"ID: {product['id']}, Name: {product['name']}, Price: ${product['price']:.2f}")
    print("------------------------\n")

def add_to_cart(cart, lookup, product_id, quantity=1):
    """Adds a specified quantity of a product to the cart."""
    if product_id not in lookup:
        print(f"Error: Product ID {product_id} not found.")
        return False # Indicate failure
    
    if quantity <= 0:
        print("Error: Quantity must be positive.")
        return False # Indicate failure
    
    # Add quantity to existing entry or create a new entry
    cart[product_id] = cart.get(product_id, 0) + quantity
    product_name = lookup[product_id]['name']
    print(f"Added {quantity} x {product_name} to cart.")
    return True

def remove_from_cart(cart, lookup, product_id, quantity=1):
    """Removes a specified quantity of a product from the cart."""
    if product_id not in cart:
        print(f"Error: Product ID {product_id} not in cart.")
        return False

    if quantity <= 0:
        print("Error: Quantity must be positive.")
        return False

    product_name = lookup[product_id]['name']

    # Decrease quantity or remove item completely
    if cart[product_id] > quantity:
        cart[product_id] -= quantity
        print(f"Removed {quantity} x {product_name} from cart. ({cart[product_id]} remaining)")
    else:
        remove_qty = cart[product_id]
        del cart[product_id]
        if quantity > remove_qty:
            print(f"Removed remaining {remove_qty} x {product_name} from cart (requested {quantity}). Item removed.")
        else:
             print(f"Removed {quantity} x {product_name} from cart. Item removed.")
    return True

def view_cart(cart, lookup):
    """Displays the current contents of the shopping cart."""
    print("\n--- Shopping Cart ---")
    if not cart:
        print("Your cart is empty.")
        print("---------------------\n")
        return
    total_items = 0
    for product_id, quantity in cart.items():
        product = lookup[product_id]
        item_total = product['price'] * quantity
        print(f"- {product['name']} (ID: {product_id}): {quantity} x ${product['price']:.2f} = ${item_total:.2f}")
        total_items += quantity

    print(f"Total items in cart: {total_items}")
    print("---------------------\n")
    # We calculate the final total separately

def calculate_total(cart, lookup):
    """Calculates and returns the total price of items in the cart."""
    total_price = 0.0
    for product_id, quantity in cart.items():
        product = lookup[product_id]
        total_price += product["price"] * quantity
    return total_price

# --- Phase 2 Functions ---

def search_products_by_name(product_list, keyword):
    """
    Searches for products containing the keyword in their name (case-insensitive).
    Returns a list of matching products.
    (LeetCode: String Manipulation)
    """
    results = []
    search_term = keyword.lower()
    for product in product_list:
        if search_term in product['name'].lower():
            results.append(product)
    return results


def get_sorted_products(product_list, criteria='name', reverse=False):
    """
    Returns a new list of products sorted by the given criteria ('name' or 'price').
    (LeetCode: Sorting Algorithms - using built-in sort with custom key)
    """
    if criteria not in ['name', 'price']:
        print("Warning: Invalid sort criteria. Defaulting to sorting by name.")
        criteria = 'name'
    
    sorted_list = sorted(product_list, key=lambda p: p[criteria], reverse=True)
    return sorted_list

def filter_products_by_price(product_list, min_price=0.0, max_price=float('inf')):
    """
    Filters products within the specified price range (inclusive).
    Returns a list of matching products.
    """
    results = []
    try:
        # Ensure min/max are valid numbers
        min_p = float(min_price)
        max_p = float(max_price)
        if min_p < 0 or max_p < 0:
             print("Warning: Prices cannot be negative. Using 0 instead.")
             min_p = max(0, min_p)
             max_p = max(0, max_p)
        if min_p > max_p:
            print("Warning: Minimum price is greater than maximum price. Swapping them.")
            min_p, max_p = max_p, min_p
    except ValueError:
        print("Error: Invalid price range provided. Using default range (all products).")
        min_p = 0.0
        max_p = float('inf') # Represents infinity
    
    for product in product_list:
        if min_p <= product['price'] <= max_p:
            results.append(product)
    return results


# --- Main Program Loop (Simple Console UI) ---

def main():
    """Runs the main shopping cart interaction loop."""
   
    current_product_view = list(products) # Start with the full list

    while True:
        print("\n===== Main Menu =====")
        print("--- Catalog ---")
        print("1. View Products (Current View)") # Changed wording slightly
        print("2. Search Products by Name")
        print("3. View Sorted Products")
        print("4. Filter Products by Price")
        print("5. Reset Product View") # Added option to go back to full list
        print("--- Cart ---")
        print("6. Add Item to Cart")
        print("7. Remove Item from Cart")
        print("8. View Cart")
        print("9. View Cart Total")
        print("0. Exit") # Changed exit to 0 for convention
        choice = input("Enter your choice: ")

        # --- Catalog Actions ---
        if choice == '1':
            print("\n--- Current Product View ---")
            display_products(current_product_view) # Display the potentially filtered/sorted list
        elif choice == '2':
            keyword = input("Enter search keyword: ")
            search_results = search_products_by_name(products, keyword) # Search the original list
            print(f"\n--- Search Results for '{keyword}' ---")
            display_products(search_results)
            # current_product_view = search_results
        elif choice == '3':
            criteria = input("Sort by (name/price): ").lower()
            order = input("Order (asc/desc): ").lower()
            reverse_order = (order == 'desc')
            # Sort the original list to show all products sorted
            sorted_list = get_sorted_products(products, criteria, reverse_order)
            print(f"\n--- Products Sorted by {criteria} ({order}) ---")
            display_products(sorted_list)
            # current_product_view = sorted_list
        elif choice == '4':
            try:
                min_p = float(input("Enter minimum price (e.g., 50.0): "))
                max_p = float(input("Enter maximum price (e.g., 500.0): "))
                filtered_list = filter_products_by_price(products, min_p, max_p) # Filter original list
                print(f"\n--- Products between ${min_p:.2f} and ${max_p:.2f} ---")
                display_products(filtered_list)
                # current_product_view = filtered_list
            except ValueError:
                print("Invalid price input. Please enter numbers.")
        elif choice == '5':
             print("Resetting product view to show all products.")
             current_product_view = list(products) # Go back to the full list
             display_products(current_product_view)

        # --- Cart Actions (Adjust numbers) ---
        elif choice == '6':
            try:
                product_id = int(input("Enter Product ID to add: "))
                # Optional: Check if ID exists in current_product_view or always allow from full catalog?
                # Let's allow adding any valid ID from the main catalog for simplicity
                if product_id not in product_lookup:
                     print(f"Error: Product ID {product_id} does not exist in the catalog.")
                else:
                    quantity = int(input("Enter quantity: "))
                    add_to_cart(shopping_cart, product_lookup, product_id, quantity)
            except ValueError:
                print("Invalid input. Please enter numbers for ID and quantity.")
        elif choice == '7':
            try:
                product_id = int(input("Enter Product ID to remove: "))
                if product_id not in shopping_cart:
                     print(f"Error: Product ID {product_id} is not in your cart.")
                else:
                    quantity = int(input("Enter quantity to remove: "))
                    remove_from_cart(shopping_cart, product_lookup, product_id, quantity)
            except ValueError:
                print("Invalid input. Please enter numbers for ID and quantity.")
        elif choice == '8':
            view_cart(shopping_cart, product_lookup)
        elif choice == '9':
            total = calculate_total(shopping_cart, product_lookup)
            print(f"\n>>> Current Cart Total: ${total:.2f} <<<")

        # --- Exit ---
        elif choice == '0':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()












    