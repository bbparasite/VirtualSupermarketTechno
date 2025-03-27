import openfoodfacts
from pythonosc import udp_client

def send_product_data(client, product):
    """
    Send selected product data via OSC
    
    Args:
    - client: OSC UDP client
    - product: Product dictionary from OpenFoodFacts
    """
    try:
        # Send selected product information via OSC
        client.send_message("/product/name", product.get("product_name", "Unknown"))
        client.send_message("/product/categories", product.get("categories", "Unknown"))
        client.send_message("/product/nutrition_grade", product.get("nutrition_grades", "Unknown"))
        
        # Optional: Send ingredients if you want more detailed data
        client.send_message("/product/ingredients", product.get("ingredients_text", "Unknown"))
        
        print(f"Sent product data for {product.get('product_name', 'Unknown')} via OSC")
    except Exception as e:
        print(f"Error sending OSC message: {e}")

def main():
    # Setup OSC Client
    # Replace with the IP and port of your OSC receiver
    osc_ip = "127.0.0.1"  # localhost
    osc_port = 5005       # common OSC port, adjust as needed
    
    # Create OSC Client
    client = udp_client.SimpleUDPClient(osc_ip, osc_port)
    
    # User-Agent is mandatory
    api = openfoodfacts.API(user_agent="VirtualSupermarketTechno/1.0")
    recipe = []

    while True:
        barcode = input("Please enter a barcode or type 'quit' to quit: ")
        try:
            if barcode == "quit":
                if len(recipe) == 0:
                    print("No recipe created")
                    break
                else:
                    print("Your recipe:")
                    for product in recipe:
                        print(product["product_name"])
                    break
            elif len(barcode) < 8:
                print("Invalid barcode - must be 8+ digits")
            else:
                product = api.product.get(barcode)
                if product is None:
                    print("No product found")
                else:
                    # Print local console output
                    print("Product name: " + product["product_name"])
                    print("Categories: " + product["categories"])
                    print("Ingredients: " + product["ingredients_text"])
                    print("Nutrition grade: " + product["nutrition_grades"])
                    
                    # Send product data via OSC
                    send_product_data(client, product)
                    
                    # Add to recipe
                    recipe.append(product)
        
        except Exception as e:
            print(f"Invalid barcode: {e}")

if __name__ == "__main__":
    main()