import sys
from datetime import datetime, timedelta


# --- Phase 4: Recommendation Engine Data ---

# Stores co-purchase counts: {product_id_A: {product_id_B: count}}
# Example: {1: {3: 5}} means Laptop(1) and Keyboard(3) were bought together 5 times.

copurchase_counts = {}


# --- Phase 3: Deals and Discounts ---

# Set of product IDs eligible for Buy One Get One Free
BOGO_ELIGIBLE_IDS = {2, 5}  # Mouse (ID 2), Webcam (ID 5)

# Tiered discounts: List of (threshold, percentage) tuples, sorted high-to-low
# A percentage of 0.10 means 10% off.
TIERED_DISCOUNTS = [
    (200.00, 0.15),  # 15% off if subtotal (after item discounts) >= $200
    (100.00, 0.08),  # 8% off if subtotal >= $100 (and < $200)
]

# Optional: Flash Sales
# Using a simulated 'now' based on when the prompt context was set.
# In a real continuously running app, you'd replace simulated_now with datetime.now()
# Current time reference: Saturday, April 26, 2025 at 11:41:15 AM CEST
try:
    # Attempt to create a specific datetime for reproducibility based on context
    simulated_now = datetime(2025, 4, 26, 11, 41, 15)
except ValueError:
    # Fallback if the date is invalid (e.g., running in a different year)
    print("Warning: Could not simulate specific context time. Using current system time for flash sales.")
    simulated_now = datetime.now()

print(f"(Simulating time as: {simulated_now.strftime('%Y-%m-%d %H:%M:%S')})") # Info for user

FLASH_SALES = [
    {
        'product_id': 1,  # Laptop
        'start_time': simulated_now - timedelta(hours=1),  # Started 1 hour ago
        'end_time': simulated_now + timedelta(hours=1),  # Ends in 1 hour
        'discount_type': 'percent',  # 'percent' or 'fixed'
        'value': 0.20  # 20% off
    },
    {
        'product_id': 4,  # Monitor
        'start_time': simulated_now + timedelta(days=1),  # Starts tomorrow
        'end_time': simulated_now + timedelta(days=1, hours=2),  # Ends 2 hours after start
        'discount_type': 'fixed',
        'value': 50.00  # $50 off
    }
]



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

# --- Helper Function for Flash Sales ---
def get_active_flash_sale(product_id, current_time):
    """Checks if there's an active flash sale for the product."""
    for sale in FLASH_SALES:
        if sale['product_id'] == product_id:
            start = sale.get('start_time')
            end = sale.get('end_time')
            if isinstance(start, datetime) and isinstance(end, datetime):
                if start <= current_time <= end:
                    return sale
    return None

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

def view_cart(cart, lookup, current_time):
    """Displays the current cart contents and calculated totals including discounts."""
    print("\n--- Shopping Cart ---")

    if not cart:
        print("Your cart is empty.")
        print("---------------------\n")
        return
    
    total_items = 0
    item_discount_notes = {detail['id']: detail['note'] for detail in calculate_total(cart, lookup, current_time)['discount_details']}
    for product_id, quantity in cart.items():
        product = lookup[product_id]
        item_total = product['price'] * quantity
        discount_note = item_discount_notes.get(product_id, "")
        print(f"- {product['name']} (ID: {product_id}): {quantity} x ${product['price']:.2f} = ${item_total:.2f} {discount_note}")
        total_items += quantity

    print(f"Total items in cart: {total_items}")
    # Calculate totals and display breakdown
    totals = calculate_total(cart, lookup, current_time)

    print(f"Subtotal:                     ${totals['subtotal_before_discounts']:.2f}")
    if totals['total_item_discount'] > 0:
        print(f"Item Discounts (BOGO/Flash): -${totals['total_item_discount']:.2f}")
    if totals['tiered_discount_amount'] > 0:
        print(f"Tiered Discount ({totals['tiered_discount_percentage']:.0f}%):       -${totals['tiered_discount_amount']:.2f}")
    if totals['total_discount_applied'] > 0:
        print(f"Total Discounts:             -${totals['total_discount_applied']:.2f}")
        print("---------------------")
        print(f"Final Total:                  ${totals['final_total']:.2f}")
    else:
        print("---------------------")
        print(f"Total:                        ${totals['final_total']:.2f}")



def calculate_total(cart, lookup, current_time):
    """
    Calculates the total price including discounts (BOGO, Flash, Tiered).
    Returns a dictionary with detailed breakdown.
    (LeetCode Concepts: Hashing, Conditional Logic, Interval checks)
    """
    subtotal_before_discounts = 0.0
    total_item_discount = 0.0
    discount_details = []

    for product_id, quantity in cart.items():
        product = lookup[product_id]
        price = product['price']
        line_item_total = price * quantity
        subtotal_before_discounts += line_item_total

        # --- Calculate potential discounts for this item ---
        bogo_discount_amount = 0.0
        flash_discount_amount = 0.0
        applied_discount_note = ""

        # Check BOGO (LeetCode: Hashing for quick check
        if product_id in BOGO_ELIGIBLE_IDS:
            free_items = quantity // 2
            if free_items > 0:
                bogo_discount_amount = free_items * price
                print(f"Debug: BOGO for {product['name']} - free items: {free_items}, discount: {bogo_discount_amount}")

        # Check Flash Sales (LeetCode: Interval check)
        active_sale = get_active_flash_sale(product_id, current_time)
        if active_sale:
            if active_sale['discount_type'] == 'percent':
                flash_discount_amount = line_item_total  * active_sale['value']
            elif active_sale['discount_type'] == 'fixed':
                # Apply fixed discount but don't make item price negative
                flash_discount_amount = min(line_item_total, active_sale['value'] * quantity)
                print(f"Debug: Flash Sale for {product['name']} - discount: {flash_discount_amount}")

        # Apply the BEST item-specific discount (BOGO vs Flash)
        best_item_discount = 0.0

        # Decide which discount is better (or if none apply)
        if bogo_discount_amount > 0 and bogo_discount_amount >= flash_discount_amount:
            # Apply BOGO if it exists and is better than or equal to flash
            best_item_discount = bogo_discount_amount
            applied_discount_note = f"(-${best_item_discount:.2f} BOGO)" # Corrected BOGO note
            print(f"Debug Calc Loop: Product {product_id}, Applied BOGO as best discount: {best_item_discount:.2f}")
        elif flash_discount_amount > 0 and flash_discount_amount > bogo_discount_amount:
            # Apply Flash if it exists and is strictly better than BOGO
            best_item_discount = flash_discount_amount
            applied_discount_note = f"(-${best_item_discount:.2f} Flash Sale)" # Correct Flash note
            print(f"Debug Calc Loop: Product {product_id}, Applied Flash Sale as best discount: {best_item_discount:.2f}")
        else:
            # No discount or both are zero
             print(f"Debug Calc Loop: Product {product_id}, No item discount applied (BOGO={bogo_discount_amount:.2f}, Flash={flash_discount_amount:.2f})")

        # Update totals based on the determined best_item_discount (which could be 0.0)
        total_item_discount += best_item_discount
        print(f"Debug Calc Loop: Product {product_id}, Total Item Discount Cumulative Now: {total_item_discount:.2f}") # Renamed for clarity

        # Add the note to the details list if a discount was applied
        if applied_discount_note:
            discount_details.append({'id': product_id, 'note': applied_discount_note})
            print(f"Debug Calc Loop: Product {product_id}, Added discount note: {applied_discount_note}")

        
    # --- Calculate subtotal after item discounts ---
    subtotal_after_item_discounts = subtotal_before_discounts - total_item_discount
    print(f"Debug: Subtotal after item discounts: {subtotal_after_item_discounts}")

    # --- Apply Tiered Discount ---
    tiered_discount_amount = 0.0
    applied_tiered_percentage = 0.0

    # Iterate thresholds high to low (LeetCode: Conditional Logic)
    for threshold, percentage in TIERED_DISCOUNTS:
        if subtotal_after_item_discounts >= threshold:
            tiered_discount_amount = subtotal_after_item_discounts * percentage
            applied_tiered_percentage = percentage * 100
            break
    print(f"Debug: Tiered discount amount: {tiered_discount_amount}")

    # --- Calculate Final Total ---
    final_total = subtotal_after_item_discounts - tiered_discount_amount
    total_discount_applied = total_item_discount + tiered_discount_amount

    return {
        'subtotal_before_discounts': subtotal_before_discounts,
        'total_item_discount': total_item_discount, # Combined BOGO/Flash
        'tiered_discount_percentage': applied_tiered_percentage,
        'tiered_discount_amount': tiered_discount_amount,
        'total_discount_applied': total_discount_applied,
        'final_total': final_total,
        'discount_details': discount_details # List of notes for specific items
    }


    

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

# --- Phase 4 Functions ---

def update_copurchase_history(cart, history_map):
    """
    Updates the co-purchase history based on items bought together in the cart.
    Increments counts for every unique pair of distinct items in the cart.
    """
    product_ids_in_cart = list(cart.keys())

    # Need at least two distinct items to form a pair
    if len(product_ids_in_cart) < 2:
        print("Debug Reco: Cart needs at least 2 distinct items to update co-purchase history.")
        return
    
    print(f"Debug Reco Update: Processing pairs for cart items {product_ids_in_cart}")

    # Iterate through all unique pairs of items in the cart
    # (LeetCode: Combination generation concept)
    for i in range(len(product_ids_in_cart)):
        for j in range(i+1, len(product_ids_in_cart)):
            item_a_id = product_ids_in_cart[i]
            item_b_id = product_ids_in_cart[j]

            # Ensure dictionaries exist, then increment count for A -> B
            history_map.setdefault(item_a_id, {})
            history_map[item_a_id][item_b_id] = history_map[item_a_id].get(item_b_id, 0) + 1
            print(f"Debug Reco Update: Increased count for {item_a_id} -> {item_b_id}")

            # Ensure dictionaries exist, then increment count for B -> A (for easy lookup later)
            history_map.setdefault(item_b_id, {})
            history_map[item_b_id][item_a_id] = history_map[item_b_id].get(item_a_id, 0) + 1
            print(f"Debug Reco Update: Increased count for {item_b_id} -> {item_a_id}")
    
    print(f"Debug Reco Update: History map updated: {history_map}")


def get_recommendations(cart, history_map, lookup, num_recommendations=3):
    """
    Generates product recommendations based on cart contents and co-purchase history.
    Returns a list of top recommended product IDs.
    (LeetCode Concepts: Hashing, Sorting)
    """
    if not cart:
        return []
    
    recommendation_scores = {}
    items_in_cart_ids = set(cart.keys())

    print(f"\n--- Generating Recommendations based on items: {list(items_in_cart_ids)} ---")

    #Iterate through items in the cart
    for item_id in items_in_cart_ids:
        # Check if this item exists in our co-purchase history
        if item_id in history_map:
            # Iterate through items commonly bought with this item
            for other_item_id, count in history_map[item_id].items():
                # Don't recommend items already in the cart!
                if other_item_id not in items_in_cart_ids:
                    # Add the co-purchase count to the score for the potential recommendation
                    recommendation_scores[other_item_id] = recommendation_scores.get(other_item_id, 0) + count
                    #print(f"Debug Reco Gen: Item {item_id} suggests {other_item_id} with count {count}. Total score for {other_item_id}: {recommendation_scores[other_item_id]}")

    if not recommendation_scores:
        print("No co-purchase data found for items in cart. Cannot generate recommendations yet.")
        return []
    
    # Sort the potential recommendations by score (descending)
    # Uses a lambda function similar to Phase 2 sorting
    sorted_recommendations = sorted(recommendation_scores.items(), key=lambda item: item[1], reverse=True)
    # Format: [(product_id1, score1), (product_id2, score2), ...]
    #print(f"Debug Reco Gen: Sorted scores: {sorted_recommendations}")

    # Get the product IDs of the top N recommendations
    recommended_ids = [item_id for item_id, score in sorted_recommendations[:num_recommendations]]

    return recommended_ids


# --- Main Program Loop (Simple Console UI) ---

def main():
    """Runs the main shopping cart interaction loop."""

    copurchase_counts = {}
   
    current_product_view = list(products) # Start with the full list
    current_time = simulated_now

    while True:
        print("\n===== Main Menu =====")
        print(f"(Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')})") 
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
        print("9. Checkout & Get Recommendations")
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
            view_cart(shopping_cart, product_lookup, current_time)
        elif choice == '9':
            print("\n--- Checking Out ---")
            if not shopping_cart:
                print("\nYour cart is empty. Total is $0.00")
            else:
                totals = calculate_total(shopping_cart, product_lookup, current_time)
                print("\n--- Cart Total Breakdown ---")
                print(f"Subtotal:                     ${totals['subtotal_before_discounts']:.2f}")
                if totals['total_item_discount'] > 0:
                    print(f"Item Discounts (BOGO/Flash): -${totals['total_item_discount']:.2f}")
                if totals['tiered_discount_amount'] > 0:
                    print(f"Tiered Discount ({totals['tiered_discount_percentage']:.0f}%):       -${totals['tiered_discount_amount']:.2f}")
                if totals['total_discount_applied'] > 0:
                    print(f"Total Discounts:             -${totals['total_discount_applied']:.2f}")
                    print("----------------------------")
                    print(f"Final Total:                  ${totals['final_total']:.2f}")
                else:
                     print("----------------------------")
                     print(f"Total:                        ${totals['final_total']:.2f}")
                print("----------------------------\n")
                print("Processing order...") # Simulate processing

                # 2. Update co-purchase history (LEARN from this purchase)
                print("Updating purchase history...")
                update_copurchase_history(shopping_cart, copurchase_counts)


                # 3. Generate recommendations based on the cart just checked out
                print("Generating recommendations for your next purchase...")
                recommended_ids = get_recommendations(shopping_cart, copurchase_counts, product_lookup, num_recommendations=3)

                if recommended_ids:
                    print("\n--- You might also be interested in ---")
                    for rec_id in recommended_ids:
                        # Lookup name - handle if ID somehow isn't in lookup (shouldn't happen)
                        rec_name = product_lookup.get(rec_id, {}).get('name', f"Unknown Product ID: {rec_id}")
                        print(f"- {rec_name} (ID: {rec_id})")
                else:
                    print("No recommendations available at this time.")
                
                # 4. Clear the cart for the next shopping session
                print("Order complete. Your cart is now empty.")
                shopping_cart.clear()

        # --- Exit ---
        elif choice == '0':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()












    