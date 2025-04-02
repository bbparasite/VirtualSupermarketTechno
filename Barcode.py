# Import necessary libraries
import openfoodfacts
from pythonosc import udp_client

def send_product_data(client, product):
    """
    Send selected product data via OSC.

    Args:
    - client: OSC UDP client instance.
    - product: Product dictionary obtained from OpenFoodFacts API.
    """
    try:
        # Get product name, default to "Unknown" if not found
        product_name = product.get("product_name", "Unknown")

        # Access the 'nutriments' dictionary first, then get 'sugars'.
        # Provide default empty dictionary {} for nutriments if it doesn't exist.
        nutriments = product.get("nutriments", {})
        fibers_value = nutriments.get("fiber", 0)
        energy_value = nutriments.get("energy-kcal", 0)
        carbohydrates_value = nutriments.get("carbohydrates", 0)
        fat_value = nutriments.get("fat", 0)
        saturated_fat_value = nutriments.get("saturated-fat", 0)
        proteins_value = nutriments.get("proteins", 0)
        sugars_value = nutriments.get("sugars", 0)

        # Get nutrition grade, default to "Unknown" if not found
        nutrition_grade = product.get("nutrition_grades", "z") # Using .get() for safety

        # Send selected product information via OSC messages
        client.send_message("/product/name", product_name)
        client.send_message("/product/nutrition_grade", nutrition_grade)
        client.send_message("/product/nutriments/sugars", sugars_value)
        client.send_message("/product/nutriments/fibers", fibers_value)
        client.send_message("/product/nutriments/energy", energy_value)
        client.send_message("/product/nutriments/carbohydrates", carbohydrates_value)
        client.send_message("/product/nutriments/fat", fat_value)
        client.send_message("/product/nutriments/saturated_fat", saturated_fat_value)
        client.send_message("/product/nutriments/proteins", proteins_value)

        print(f"Sent product data for {product_name} via OSC")
    except Exception as e:
        # Print error if sending OSC message fails
        print(f"Error sending OSC message: {e}")

def main():
    """
    Main function to run the barcode scanner and OSC sender.
    """
    # Setup OSC Client Configuration
    # Replace with the IP address and port of your OSC receiver application
    osc_ip = "127.0.0.1"  # Default to localhost
    osc_port = 5005       # Common OSC port, adjust if your receiver uses a different one

    # Create an OSC UDP Client instance
    client = udp_client.SimpleUDPClient(osc_ip, osc_port)
    print(f"OSC client configured to send to {osc_ip}:{osc_port}")

    # Initialize OpenFoodFacts API client
    # A User-Agent is required by the API
    api = openfoodfacts.API(user_agent="VirtualSupermarketTechno/1.0") # Use a descriptive user agent

    # List to store products added to the recipe
    recipe = []

    # Main loop to get barcode input from the user
    while True:
        barcode = input("Please enter a product barcode or type 'quit' to exit: ")
        try:
            # Check if the user wants to quit
            if barcode.lower() == "quit":
                if not recipe: # Check if the recipe list is empty
                    print("No recipe was created.")
                else:
                    # Print the final recipe if items were added
                    print("\nYour final recipe:")
                    for item in recipe:
                        print(f"- {item.get('product_name', 'Unknown Product')}")
                break # Exit the loop

            # Validate barcode length (basic check)
            elif len(barcode) < 8:
                print("Invalid barcode - barcodes usually have 8 or more digits.")

            # Process the barcode if it seems valid
            else:
                # Fetch product data from OpenFoodFacts API
                product_data = api.product.get(barcode, fields=["product_name", "categories", "ingredients_text", "nutrition_grades", "nutriments"]) # Specify fields for efficiency
                
                # Check if product data was found
                if product_data is None:
                    print(f"No product found for barcode: {barcode}")
                else:
                    # Print some product details to the console
                    print("\n--- Product Found ---")
                    print(f"Name: {product_data.get('product_name', 'N/A')}")
                    print(f"Categories: {product_data.get('categories', 'N/A')}")
                    print(f"Ingredients: {product_data.get('ingredients_text', 'N/A')}")
                    print(f"Nutrition Grade: {product_data.get('nutrition_grades', 'N/A')}")
                    print("---------------------\n")

                    # Send relevant product data via OSC
                    send_product_data(client, product_data)

                    # Add the fetched product data to the recipe list
                    recipe.append(product_data)

        # Handle potential errors during API call or processing
        except Exception as e:
            print(f"An error occurred: {e}")

# Ensure the main function runs only when the script is executed directly
if __name__ == "__main__":
    main()
