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
product_lookup = {products["id"]: product for product in products}


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
        print(f"ID: {product["id"]}, Name: {product["name"]}, Price: ${product['price']:.2f}")
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
            print(f"Removed remaining {removed_qty} x {product_name} from cart (requested {quantity}). Item removed.")
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

# --- Main Program Loop (Simple Console UI) ---

def main():
    """Runs the main shopping cart interaction loop."""
    while True:
        print("\n===== Main Menu =====")
        print("1. View Products")
        print("2. Add Item to Cart")
        print("3. Remove Item from Cart")
        print("4. View Cart")
        print("5. View Cart Total")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            display_products(products)
        elif choice == '2':
            try:
                product_id = int(input("Enter Product ID to add: "))
                quantity = int(input("Enter quantity: "))
                add_to_cart(shopping_cart, product_lookup, product_id, quantity)
            except ValueError:
                print("Invalid input. Please enter numbers for ID and quantity.")
        elif choice == '3':
            try:
                product_id = int(input("Enter Product ID to remove: "))
                quantity = int(input("Enter quantity to remove: "))
                remove_from_cart(shopping_cart, product_lookup, product_id, quantity)
            except ValueError:
                print("Invalid input. Please enter numbers for ID and quantity.")
        elif choice == '4':
            view_cart(shopping_cart, product_lookup)
        elif choice == '5':
            total = calculate_total(shopping_cart, product_lookup)
            print(f"\n>>> Current Cart Total: ${total:.2f} <<<")
        elif choice == '6':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    # This ensures the main() function runs only when the script is executed directly
    main()












    