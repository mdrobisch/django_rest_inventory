import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
USERNAME = "testuser_py"
PASSWORD = "testpassword"

def main():
    """
    Runs a sequence of tests against the API:
    1. Register a new user.
    2. Log in to get an access token.
    3. Use the token to create a new item.
    4. List all items.
    5. Update the newly created item.
    6. Delete the item.
    """
    print("--- Starting API Test ---")

    # 1. Register a new user
    print("\n1. Registering a new user...")
    try:
        register_response = requests.post(
            f"{BASE_URL}/auth/register/",
            json={"username": USERNAME, "password": PASSWORD}
        )
        if register_response.status_code == 201:
            print(f"✅ User '{USERNAME}' registered successfully.")
        elif register_response.status_code == 400 and "already exists" in register_response.json().get("username", [])[0]:
             print(f"ℹ️ User '{USERNAME}' already exists. Proceeding to login.")
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            print(register_response.json())
            return
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: Could not connect to the server at {BASE_URL}.")
        print("Please make sure the Django development server is running.")
        return


    # 2. Log in to get an access token
    print("\n2. Logging in...")
    login_response = requests.post(
        f"{BASE_URL}/auth/token/",
        json={"username": USERNAME, "password": PASSWORD}
    )
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.json())
        return
    
    access_token = login_response.json().get("access")
    print("✅ Login successful. Got access token.")
    headers = {"Authorization": f"Bearer {access_token}"}

    # 3. Create a new item
    print("\n3. Creating a new item...")
    item_data = {"name": "Test Item from Script", "description": "This is a test.", "quantity": 50}
    create_response = requests.post(f"{BASE_URL}/items/", json=item_data, headers=headers)
    if create_response.status_code != 201:
        print(f"❌ Item creation failed: {create_response.status_code}")
        print(create_response.json())
        return
    
    item_id = create_response.json().get("id")
    print(f"✅ Item created successfully with ID: {item_id}")
    print(json.dumps(create_response.json(), indent=2))

    # 4. List all items
    print("\n4. Listing all items...")
    list_response = requests.get(f"{BASE_URL}/items/", headers=headers)
    if list_response.status_code != 200:
        print(f"❌ Listing items failed: {list_response.status_code}")
        return
    
    print("✅ Items listed successfully:")
    print(json.dumps(list_response.json(), indent=2))

    # 5. Update the newly created item
    print(f"\n5. Updating item with ID: {item_id}...")
    updated_item_data = {"name": "Updated Test Item", "description": "This item has been updated.", "quantity": 75}
    update_response = requests.put(f"{BASE_URL}/items/{item_id}/", json=updated_item_data, headers=headers)
    if update_response.status_code != 200:
        print(f"❌ Item update failed: {update_response.status_code}")
        print(update_response.json())
        return
        
    print("✅ Item updated successfully:")
    print(json.dumps(update_response.json(), indent=2))

    # 6. Delete the item
    print(f"\n6. Deleting item with ID: {item_id}...")
    delete_response = requests.delete(f"{BASE_URL}/items/{item_id}/", headers=headers)
    if delete_response.status_code != 204:
        print(f"❌ Item deletion failed: {delete_response.status_code}")
        # No JSON body is returned on a 204 response, so we don't print it
        return

    print("✅ Item deleted successfully.")
    
    print("\n--- API Test Finished ---")


if __name__ == "__main__":
    main()
