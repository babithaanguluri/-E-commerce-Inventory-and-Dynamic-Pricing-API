import httpx
import time
import threading

BASE_URL = "http://localhost:8000/api/v1"

def test_price_calculation():
    print("\n--- Testing Price Calculation ---")
    with httpx.Client() as client:
        # Test 1 unit
        resp = client.get(f"{BASE_URL}/products/1/price?quantity=1")
        print(f"Price for 1 unit: {resp.json()['final_price']}")
        
        # Test 5 units (Bulk discount)
        resp = client.get(f"{BASE_URL}/products/1/price?quantity=5")
        print(f"Price for 5 units: {resp.json()['final_price']}")
        print(f"Applied Rules: {[r['rule_name'] for r in resp.json()['applied_rules']]}")

def test_inventory_concurrency():
    print("\n--- Testing Inventory Concurrency ---")
    results = []
    
    def attempt_reserve(user_id):
        with httpx.Client() as client:
            try:
                resp = client.post(f"{BASE_URL}/cart/add", json={
                    "variant_id": 1,
                    "quantity": 6, # Total stock is 10. Two users requesting 6 should result in one failure.
                    "cart_id": f"cart_{user_id}"
                })
                results.append((user_id, resp.status_code, resp.text))
            except Exception as e:
                results.append((user_id, "ERROR", str(e)))

    t1 = threading.Thread(target=attempt_reserve, args=(1,))
    t2 = threading.Thread(target=attempt_reserve, args=(2,))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    for res in results:
        print(f"User {res[0]}: Status {res[1]}")

if __name__ == "__main__":
    # Note: Assumes server is running and DB is seeded
    try:
        test_price_calculation()
        test_inventory_concurrency()
    except Exception as e:
        print(f"Verification failed: {e}")
