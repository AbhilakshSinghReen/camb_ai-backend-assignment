import requests
import unittest

from utils import generate_random_value, generate_unique_key


class TestAPIs(unittest.TestCase):
    base_url = "http://localhost:8000"

    def test_get_homepage(self):
        "Gets the homepage and verifies that the response is HTML."

        response = requests.get(self.base_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], "text/html; charset=utf-8")

    def test_add_key_value_pair(self):
        "Adds a key-value pair to the store, then gets it and verifies."
        
        test_key = generate_unique_key()
        test_value = generate_random_value()
        
        # Add new key-value pair
        add_response = requests.post(
            f"{self.base_url}/api/data/add",
            json={
                'key': test_key,
                'value': test_value,
            },
            headers={
                'Content-Type': "application/json"
            }
        )

        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.headers['content-type'], "application/json")

        add_response_data = add_response.json()

        self.assertEqual(add_response_data.get('success', None), True)
        self.assertEqual(add_response_data.get('result', {}).get('message', None), "Addition scheduled.")

        # Get newly added key-value pair and verify
        get_response = requests.get(f"{self.base_url}/api/data/get/{test_key}")

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.headers['content-type'], "application/json")

        get_response_data = get_response.json()

        self.assertEqual(get_response_data.get('success', None), True)
        self.assertEqual(get_response_data.get('result', {}).get('key', None), test_key)
        self.assertEqual(get_response_data.get('result', {}).get('value', None), test_value)

    def test_update_key_value_pair(self):
        "Adds a key-value pair to the store, verify the addition, update it, and verify the update."
        
        test_key = generate_unique_key()
        test_value_1 = generate_random_value()
        test_value_2 = generate_random_value()
        
        # Add new key-value pair
        add_response = requests.post(
            f"{self.base_url}/api/data/add",
            json={
                'key': test_key,
                'value': test_value_1,
            },
            headers={
                'Content-Type': "application/json"
            }
        )

        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.headers['content-type'], "application/json")

        add_response_data = add_response.json()

        self.assertEqual(add_response_data.get('success', None), True)
        self.assertEqual(add_response_data.get('result', {}).get('message', None), "Addition scheduled.")

        # Get newly added key-value pair
        get_response = requests.get(f"{self.base_url}/api/data/get/{test_key}")

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.headers['content-type'], "application/json")

        get_response_data = get_response.json()

        self.assertEqual(get_response_data.get('success', None), True)
        self.assertEqual(get_response_data.get('result', {}).get('key', None), test_key)
        self.assertEqual(get_response_data.get('result', {}).get('value', None), test_value_1)

        # Update the key-value pair
        update_response = requests.put(
            f"{self.base_url}/api/data/update/{test_key}",
            json={
                'value': test_value_2,
            },
            headers={
                'Content-Type': "application/json"
            }
        )

        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.headers['content-type'], "application/json")

        update_response_data = update_response.json()

        self.assertEqual(update_response_data.get('success', None), True)
        self.assertEqual(update_response_data.get('result', {}).get('message', None), "Updation scheduled.")
        
        # Get updated key-value pair and verify
        get_response = requests.get(f"{self.base_url}/api/data/get/{test_key}")

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.headers['content-type'], "application/json")

        get_response_data = get_response.json()

        self.assertEqual(get_response_data.get('success', None), True)
        self.assertEqual(get_response_data.get('result', {}).get('key', None), test_key)
        self.assertEqual(get_response_data.get('result', {}).get('value', None), test_value_2)
    
    def test_delete_key_value_pair(self):
        "Adds a new key-value pair to the store, verifies it exists, then deletes it and verifies it does not exist."
        
        test_key = generate_unique_key()
        test_value_1 = generate_random_value()
        
        # Add new key-value pair
        add_response = requests.post(
            f"{self.base_url}/api/data/add",
            json={
                'key': test_key,
                'value': test_value_1,
            },
            headers={
                'Content-Type': "application/json"
            }
        )

        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.headers['content-type'], "application/json")

        add_response_data = add_response.json()

        self.assertEqual(add_response_data.get('success', None), True)
        self.assertEqual(add_response_data.get('result', {}).get('message', None), "Addition scheduled.")

        # Get newly added key-value pair
        get_response = requests.get(f"{self.base_url}/api/data/get/{test_key}")

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.headers['content-type'], "application/json")

        get_response_data = get_response.json()

        self.assertEqual(get_response_data.get('success', None), True)
        self.assertEqual(get_response_data.get('result', {}).get('key', None), test_key)
        self.assertEqual(get_response_data.get('result', {}).get('value', None), test_value_1)

        # Delete the key-value pair
        delete_response = requests.delete(f"{self.base_url}/api/data/delete/{test_key}")
        
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.headers['content-type'], "application/json")

        delete_response_data = delete_response.json()

        self.assertEqual(delete_response_data.get('success', None), True)
        self.assertEqual(delete_response_data.get('result', {}).get('message', None), "Deletion scheduled.")
        
        # Get updated added key-value-pair
        get_response = requests.get(f"{self.base_url}/api/data/get/{test_key}")

        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_response.headers['content-type'], "application/json")

        get_response_data = get_response.json()

        self.assertEqual(get_response_data.get('success', None), False)
        self.assertEqual(get_response_data.get('error', {}).get('message', None), "Key does not exist.")

    def test_try_get_non_existent_key(self):
        "Tries to get a key-value pair that does not exist."

        test_key = generate_unique_key()

        get_response = requests.get(f"{self.base_url}/api/data/get/{test_key}")

        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_response.headers['content-type'], "application/json")

        get_response_data = get_response.json()
        
        self.assertEqual(get_response_data.get('success', None), False)
        self.assertEqual(get_response_data.get('error', {}).get('message', None), "Key does not exist.")

    def test_try_add_key_twice(self):
        "Tries to add a key-value pair twice."

        test_key = generate_unique_key()
        test_value_1 = generate_random_value()
        test_value_2 = generate_random_value()

        # Add new key-value pair
        add_response = requests.post(
            f"{self.base_url}/api/data/add",
            json={
                'key': test_key,
                'value': test_value_1,
            },
            headers={
                'Content-Type': "application/json"
            }
        )

        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.headers['content-type'], "application/json")

        add_response_data = add_response.json()

        self.assertEqual(add_response_data.get('success', None), True)
        self.assertEqual(add_response_data.get('result', {}).get('message', None), "Addition scheduled.")

        # Get newly added key-value pair
        get_response = requests.get(f"{self.base_url}/api/data/get/{test_key}")

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.headers['content-type'], "application/json")

        get_response_data = get_response.json()

        self.assertEqual(get_response_data.get('success', None), True)
        self.assertEqual(get_response_data.get('result', {}).get('key', None), test_key)
        self.assertEqual(get_response_data.get('result', {}).get('value', None), test_value_1)

        # Add new key-value pair 2
        add_response_2 = requests.post(
            f"{self.base_url}/api/data/add",
            json={
                'key': test_key,
                'value': test_value_2,
            },
            headers={
                'Content-Type': "application/json"
            }
        )

        self.assertEqual(add_response_2.status_code, 400)
        self.assertEqual(add_response_2.headers['content-type'], "application/json")

        add_response_2_data = add_response_2.json()

        self.assertEqual(add_response_2_data.get('success', None), False)
        self.assertEqual(add_response_2_data.get('error', {}).get('message', None), "Key already exists")

    def try_update_non_existent_key_value_pair(self):
        "Tries to update the value of a key that does not exist."

        test_key = generate_unique_key()
        test_value = generate_random_value()

        update_response = requests.put(
            f"{self.base_url}/api/data/update/{test_key}",
            json={
                'value': test_value,
            },
            headers={
                'Content-Type': "application/json"
            }
        )

        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(update_response.headers['content-type'], "application/json")

        update_response_data = update_response.json()
        
        self.assertEqual(update_response_data.get('success', None), False)
        self.assertEqual(update_response_data.get('error', {}).get('message', None), "Key does not exist.")

    def test_try_delete_non_existent_key_value_pair(self):
        "Tries to delete a key that does not exist."

        test_key = generate_unique_key()

        delete_response = requests.delete(f"{self.base_url}/api/data/delete/{test_key}")

        self.assertEqual(delete_response.status_code, 404)
        self.assertEqual(delete_response.headers['content-type'], "application/json")
        
        delete_response_data = delete_response.json()
        
        self.assertEqual(delete_response_data.get('success', None), False)
        self.assertEqual(delete_response_data.get('error', {}).get('message', None), "Key does not exist.")


if __name__ == "__main__":
    unittest.main()
