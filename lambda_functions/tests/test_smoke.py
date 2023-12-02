import requests
import json

import boto3

# The URL of the deployed API
API_URL = "https://9drbe81ae7.execute-api.us-east-1.amazonaws.com/countVisit"

def get_visit_count_from_dynamodb():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Replace 'us-east-1' with your region
    table = dynamodb.Table('visitCounter')
    response = table.get_item(Key={'id': 'counter'})
    return int(response['Item']['visit_count'])

def test_api_returns_updated_value():
    # Send a POST request to the API to increment the visitor count
    response = requests.post(API_URL)
    assert response.status_code == 200
    # Parse the response body to get the visitor count after the first increment
    body = json.loads(response.text)
    initial_count = int(body)  # Assuming the response contains the count directly

    # Send another POST request to increment the visitor count again
    response = requests.post(API_URL)
    assert response.status_code == 200
    body = json.loads(response.text)
    updated_count = int(body)

    # Check if the visitor count has incremented
    assert updated_count == initial_count + 1

    # Get the current count from DynamoDB directly
    dynamodb_count = get_visit_count_from_dynamodb()

    # Check if the DynamoDB count matches the updated count
    assert dynamodb_count == updated_count



def test_api_response_to_get_request():
    # Send a GET request which is not the expected method for the API
    response = requests.get(API_URL)
    # The API should return a 404 error
    assert response.status_code in [404]


# Execute the tests
if __name__ == "__main__":
    test_api_returns_updated_value()
    test_api_response_to_get_request()
