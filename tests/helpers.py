def add_key_value_pair(test_client, key, value):
    "Reusuable function for adding a key-value pair to the store."

    add_response = test_client.post(
        "/api/data/add",
        json={
            'key': key,
            'value': value,
        },
        headers={
            'Content-Type': "application/json"
        }
    )

    assert add_response.status_code == 200
    assert add_response.headers['content-type'] == "application/json"

    add_response_data = add_response.json()
    
    assert add_response_data.get('success', None) == True
    assert add_response_data.get('result', {}).get('key', None) == key
    assert add_response_data.get('result', {}).get('value', None) == value


def get_and_verify_key_value_pair(test_client, key, expected_value):
    "Reusuable function to get a key-value pair and verify it."

    get_response = test_client.get(f"/api/data/get/{key}")

    assert get_response.status_code == 200
    assert get_response.headers['content-type'] == "application/json"

    get_response_data = get_response.json()
    
    assert get_response_data.get('success', None) == True
    assert get_response_data.get('result', {}).get('key', None) == key
    assert get_response_data.get('result', {}).get('value', None) == expected_value


def update_key_value_pair(test_client, key, new_value):
    "Reusuable function for updating a key-value pair."

    update_response = test_client.put(
        f"/api/data/update/{key}",
        json={
            'value': new_value,
        },
        headers={
            'Content-Type': "application/json"
        }
    )

    assert update_response.status_code == 200
    assert update_response.headers['content-type'] == "application/json"

    update_response_data = update_response.json()
    
    assert update_response_data.get('success', None) == True
    assert update_response_data.get('result', {}).get('key', None) == key
    assert update_response_data.get('result', {}).get('value', None) == new_value


def delete_key_value_pair(test_client, key):
    delete_response = test_client.delete(f"/api/data/delete/{key}")

    assert delete_response.status_code == 204


def verify_key_does_not_exist(test_client, key):
    "Reusuable function to get a key-value pair and verify it."
    
    get_response = test_client.get(f"/api/data/get/{key}")

    assert get_response.status_code == 404
    assert get_response.headers['content-type'] == "application/json"

    get_response_data = get_response.json()
    
    assert get_response_data.get('success', None) == False
    assert get_response_data.get('error', {}).get('message', None) == "Key does not exist."
