import requests
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
base_url = "http://127.0.0.1:8000"
order_id = 3


def confirm_reject_order(status: str) -> None:
    requests.put(f"{base_url}/orders/{order_id}", json={"status": status})


def validate_stock(order: dict):
    out_of_stock = False
    prev_quantities = []

    for order_item in order["order_items"]:
        product = order_item["product"]
        prev_index = next((index for (index, d) in enumerate(prev_quantities) if d['product_id'] == product["id"]), -1)

        # CHECK IF THERE ARE OTHER ORDER ITEM TRYING TO BUY MORE QUANTITY FOR THE SAME PRODUCT
        quantity = order_item["quantity"]
        if prev_index >= 0:
            quantity += prev_quantities[prev_index]["quantity"]
            prev_quantities[prev_index]["quantity"] = quantity
        else:
            prev_quantities.append({"product_id": product["id"], "quantity": quantity})

        if product["stock"] < quantity:
            out_of_stock = True
    
    return out_of_stock, prev_quantities


def capture_order():

    # 1. GET A ORDER
    logging.info("GETTING ORDER INFORMATION")
    order_response = requests.get(f"{base_url}/orders/{order_id}")
    if order_response.status_code == 404:
        logging.info("ORDER NOT FOUND")
        sys.exit(0) 

    order = order_response.json()
    if len(order["order_items"]) == 0:
        logging.error("NOT FOUND ORDER ITEMS ON THIS ORDER")
        sys.exit(0) 

    # 2. VALIDATE IF THERE ARE ENOGHT STOCK OF THE ORDERS PRODUCTS
    logging.info("VALIDATING STOCK OF PRODUCTS")
    out_stock, prev_quantities = validate_stock(order=order)

    if out_stock:
        confirm_reject_order("rejected")
        logging.error("SOME PRODUCTS ARE OUT OF STOCK")
        sys.exit(0) 

    # 3. SAVE MOVEMENT ON INVENTORY
    logging.info("UPDATING INVENTORY MOVEMENTS")
    for item in prev_quantities:
        data = {
            "product_id": item["product_id"],
            "movement_type": "sale",
            "quantity": item["quantity"]
        }
        requests.post(f"{base_url}/inventory-movements", json=data)

    # 4. UPDATE THE ORDER STATUS
    confirm_reject_order("confirmed")

    # 5. REGISTER THE RESULT OF PROCESSING
    logging.info("ORDER SUCCESSFULLY STOCKED")


capture_order()