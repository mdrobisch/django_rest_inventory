import unittest
import requests
import json
import os

# This allows running the script from the 'backend' directory
BASE_URL = "http://127.0.0.1:8000/api"
USERNAME = "unittest_user"
PASSWORD = "testpassword"

class TestInventoryAPI(unittest.TestCase):
    """
    A test suite for the inventory API.
    Tests are ordered to ensure a logical flow (create -> list -> update -> delete).
    """
    access_token = None
    headers = None
    item_id = None

    @classmethod
    def setUpClass(cls):
        """
        This method runs once before any tests in the class.
        It handles user registration and login to get an access token.
        """
        print("--- Setting up test suite ---")
        
        # Ensure the server is running
        try:
            requests.get("http://127.0.0.1:8000/", timeout=2)
        except requests.exceptions.ConnectionError:
            print("\n❌ FATAL: Cannot connect to the Django development server.")
            print("Please make sure the server is running before starting tests.")
            # This is a bit of a hack to stop the test suite
            # A better solution would use a test runner configuration
            os._exit(1)


        # 1. Register a new user (or ignore if user already exists)
        print("1. Registering user...")
        requests.post(
            f"{BASE_URL}/auth/register/",
            json={"username": USERNAME, "password": PASSWORD}
        )
        print(f"ℹ️  Ensured user '{USERNAME}' exists.")

        # 2. Log in to get an access token
        print("2. Logging in...")
        login_response = requests.post(
            f"{BASE_URL}/auth/token/",
            json={"username": USERNAME, "password": PASSWORD}
        )
        
        if login_response.status_code != 200:
            raise Exception("Could not log in to get access token. Tests cannot proceed.")

        cls.access_token = login_response.json().get("access")
        cls.headers = {"Authorization": f"Bearer {cls.access_token}"}
        print("✅ Setup complete. Got access token.\n")

    def test_1_create_item(self):
        """
        Tests creating a new item.
        """
        print("--- Running test_1_create_item ---")
        self.assertIsNotNone(self.headers, "Authentication headers are not set.")
        
        item_data = {"name": "Unittest Item", "description": "Created by unittest", "quantity": 123}
        response = requests.post(f"{BASE_URL}/items/", json=item_data, headers=self.headers)
        
        self.assertEqual(response.status_code, 201, f"Expected 201, got {response.status_code}. Body: {response.text}")
        response_data = response.json()
        self.assertIn("id", response_data)
        
        # Store the item_id as a class variable to use in other tests
        TestInventoryAPI.item_id = response_data['id']
        print(f"✅ Item created with ID: {self.item_id}")

    def test_2_list_items(self):
        """
        Tests listing all items and ensures the newly created item is present.
        """
        print("\n--- Running test_2_list_items ---")
        self.assertIsNotNone(self.item_id, "Prerequisite test_1_create_item must pass.")
        
        response = requests.get(f"{BASE_URL}/items/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        
        items = response.json()
        self.assertIsInstance(items, list)
        
        # Check if our created item is in the list
        item_ids = [item['id'] for item in items]
        self.assertIn(self.item_id, item_ids, "Newly created item not found in list.")
        print("✅ Item list verified.")

    def test_3_update_item(self):
        """
        Tests updating the item created in the first test.
        """
        print("\n--- Running test_3_update_item ---")
        self.assertIsNotNone(self.item_id, "Prerequisite test_1_create_item must pass.")
        
        updated_data = {"name": "Updated Unittest Item", "description": "Updated by unittest", "quantity": 321}
        response = requests.put(f"{BASE_URL}/items/{self.item_id}/", json=updated_data, headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], updated_data['name'])
        print("✅ Item updated successfully.")

    def test_4_delete_item(self):
        """
        Tests deleting the item and verifies it's gone.
        """
        print("\n--- Running test_4_delete_item ---")
        self.assertIsNotNone(self.item_id, "Prerequisite test_1_create_item must pass.")
        
        # Delete the item
        delete_response = requests.delete(f"{BASE_URL}/items/{self.item_id}/", headers=self.headers)
        self.assertEqual(delete_response.status_code, 204)

        # Verify it's gone by trying to fetch it again
        verify_response = requests.get(f"{BASE_URL}/items/{self.item_id}/", headers=self.headers)
        self.assertEqual(verify_response.status_code, 404, "Item was not actually deleted.")
        print("✅ Item deleted successfully.")

if __name__ == '__main__':
    unittest.main()
