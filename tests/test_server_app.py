from fastapi.testclient import TestClient

from .helpers import (
    add_key_value_pair,
    delete_key_value_pair,
    get_and_verify_key_value_pair,
    update_key_value_pair,
    verify_key_does_not_exist,
)
from .utils import generate_random_value, generate_unique_key
from server.src.app import app


test_client = TestClient(app)


def test_get_homepage():
    "Gets the homepage and verifies that the response is HTML."

    response = test_client.get("/")

    assert response.status_code == 200
    assert response.headers['content-type'] == "text/html; charset=utf-8"


# def test_add_key_value_pair():
#     "Adds a key-value pair to the store, then gets it and verifies."
    
#     test_key = generate_unique_key()
#     test_value = generate_random_value()

#     add_key_value_pair(test_client, test_key, test_value) # Add new key-value pair

#     get_and_verify_key_value_pair(test_client, test_key, test_value) # Get the newly added key-value pair and verify it


# def test_update_key_value_pair():
#     "Adds a new key-value pair to the store, updates it, then gets it and verifies."

#     test_key = generate_unique_key()
#     initial_value = generate_random_value() # initial value of the key
#     new_value = generate_random_value() # later value of the key (to be updated)

#     add_key_value_pair(test_client, test_key, initial_value) # Add new key-value pair with initial value

#     update_key_value_pair(test_client, test_key, new_value) # Update the key-value pair

#     get_and_verify_key_value_pair(test_client, test_key, new_value)


# def test_delete_key_value_pair():
#     "Adds a new key-value pair to the store, verifies it exists, then deletes it and verifies it does not exist."

#     test_key = generate_unique_key()
#     test_value = generate_random_value()

#     add_key_value_pair(test_client, test_key, test_value) # Add new key-value pair

#     get_and_verify_key_value_pair(test_client, test_key, test_value) # Get the newly added key-value pair and verify it

#     delete_key_value_pair(test_client, test_key) # Delete the newly added key-value pair

#     verify_key_does_not_exist(test_client, test_key) # Verify that this key no longer exists in the store


# def test_get_non_existent_key_value_pair():
#     "Tries to get a key-value pair that does not exist in the store."

#     test_key = generate_unique_key()

#     get_response = test_client.get(f"/api/data/get/{test_key}")

#     assert get_response.status_code == 404
#     assert get_response.headers['content-type'] == "application/json"

#     get_response_data = get_response.json()
    
#     assert get_response_data.get('success', None) == False
#     assert get_response_data.get('error', {}).get('message', None) == "Key does not exist."


# def test_try_update_non_existent_key_value_pair():
#     "Tries to update the value of a key that does not exist."

#     test_key = generate_unique_key()
#     test_value = generate_random_value()

#     update_response = test_client.put(
#         f"/api/data/update/{test_key}",
#         json={
#             'value': test_value,
#         },
#         headers={
#             'Content-Type': "application/json"
#         }
#     )

#     assert update_response.status_code == 404
#     assert update_response.headers['content-type'] == "application/json"

#     update_response_data = update_response.json()
    
#     assert update_response_data.get('success', None) == False
#     assert update_response_data.get('error', {}).get('message', None) == "Key does not exist."


# def test_try_delete_non_existent_key_value_pair():
#     "Tries to delete a key that does not exist."

#     test_key = generate_unique_key()

#     # Add the same key again
#     delete_response = test_client.delete(f"/api/data/delete/{test_key}")

#     assert delete_response.status_code == 404
#     assert delete_response.headers['content-type'] == "application/json"

#     delete_response_data = delete_response.json()
    
#     assert delete_response_data.get('success', None) == False
#     assert delete_response_data.get('error', {}).get('message', None) == "Key does not exist."


# def test_try_add_existent_key():
#     "Tries to add a key twice."
    
#     test_key = generate_unique_key()
#     test_value_1 = generate_random_value()
#     test_value_2 = generate_random_value()

#     add_key_value_pair(test_client, test_key, test_value_1) # Add new key-value pair

#     # Add the same key again
#     add_response = test_client.post(
#         "/api/data/add",
#         json={
#             'key': test_key,
#             'value': test_value_2,
#         },
#         headers={
#             'Content-Type': "application/json"
#         }
#     )

#     assert add_response.status_code == 400
#     assert add_response.headers['content-type'] == "application/json"

#     add_response_data = add_response.json()
    
#     assert add_response_data.get('success', None) == False
#     assert add_response_data.get('error', {}).get('message', None) == f"Key already exists"
