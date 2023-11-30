import requests
import json

# The URL of the deployed API
API_URL = "https://9drbe81ae7.execute-api.us-east-1.amazonaws.com/countVisit"

def test_api_returns_updated_value():
    # Send a request to the API
    response = requests.get(API_URL)
    assert response.status_code == 200
    # Parse the response body to get the visitor count
    body = json.loads(response.text)
    initial_count = int(response.text)#body['visitorCount']

    # Send another request to increment the visitor count
    response = requests.get(API_URL)
    assert response.status_code == 200
    body = json.loads(response.text)
    updated_count = int(response.text)#body['visitorCount']

    # Check if the visitor count has incremented
    assert updated_count == initial_count + 1

    # Optionally, you can add another check to query the database directly (if accessible)
    # to verify that the count is also incremented there.

def test_api_response_to_get_request():
    # Send a GET request which is not the expected method for the API
    response = requests.get(API_URL)
    # The API should return a status code indicating a bad request (e.g., 400 or 405)
    assert response.status_code in [400, 405]


# Execute the tests
if __name__ == "__main__":
    test_api_returns_updated_value()
    test_api_response_to_get_request()
