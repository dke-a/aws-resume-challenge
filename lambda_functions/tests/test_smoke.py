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

# def test_api_response_to_unexpected_input():
#     # Send a malformed request (for example, a POST request instead of expected GET)
#     response = requests.post(API_URL, json={"bad": "data"})
#     # The API should return a 400 or 405 status code for bad requests
#     assert response.status_code in [400, 404, 405]

# def test_uninitialized_visitor_count():
#     # For this test, you would typically reset the environment or use a separate test environment
#     # Assuming that the API creates an initial count if not present
#     # Reset the environment or use a new database entry to simulate first-time invocation

#     # Send a request to the API as if it is the first invocation
#     response = requests.get(API_URL)
#     assert response.status_code == 200
#     body = json.loads(response.text)
#     # Check if the visitor count is initialized properly (assuming it starts at 1)
#     assert body['visitorCount'] == 1

# Execute the tests
if __name__ == "__main__":
    test_api_returns_updated_value()
    #test_api_response_to_unexpected_input()
    #test_uninitialized_visitor_count()