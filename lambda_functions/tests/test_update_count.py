import json
import os

import boto3
import pytest
from moto.dynamodb import mock_dynamodb  # Updated import only
from botocore.exceptions import ClientError

from lambda_functions.update_count.lambda_function import lambda_handler

# Mock AWS Services
@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

@pytest.fixture(scope='function')
def dynamodb(aws_credentials: None):
    with mock_dynamodb():  # Updated usage only
        yield boto3.resource('dynamodb', region_name='us-east-1')

@pytest.fixture(scope='function')
def dynamodb_table(dynamodb):
    # Create a DynamoDB table
    table = dynamodb.create_table(
        TableName='visitCounter',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST'
    )

    # Wait for table to be created
    table.meta.client.get_waiter('table_exists').wait(TableName='visitCounter')

    # Insert a counter item
    table.put_item(Item={'id': 'counter', 'visit_count': 0})
    
    return table

# Tests
def test_lambda_handler(dynamodb_table):
    # Simulate Lambda event for a POST request
    event = {
        'requestContext': {
            'http': {
                'method': 'POST'
            }
        }
    }
    context = {}

    # Call the lambda handler
    response = lambda_handler(event, context)

    # Check if HTTP status code is 200
    assert response['statusCode'] == 200
    # Check if the response body is correct
    response['body'] = int(response['body'])
    body = json.dumps(response['body'])
    
    assert body == str(1)  # Assuming start at 0, first call should return 1.


def test_lambda_handler_failure(dynamodb_table):
    # Inject an error by deleting the table
    dynamodb_table.delete()
    dynamodb_table.meta.client.get_waiter('table_not_exists').wait(TableName='visitCounter')

    # Simulate Lambda event for a POST request
    event = {
        'requestContext': {
            'http': {
                'method': 'POST'
            }
        }
    }
    context = {}

    # Call the lambda handler
    response = lambda_handler(event, context)

    # Check if HTTP status code is 500
    assert response['statusCode'] == 500
    # Check if the body contains the correct error message
    assert response['body'] == "Internal Server Error"


def test_lambda_handler_get_request(dynamodb_table):
    # Simulate Lambda event for a GET request
    event = {
        'requestContext': {
            'http': {
                'method': 'GET'
            }
        }
    }
    context = {}

    # Call the lambda handler
    response = lambda_handler(event, context)

    # Check if HTTP status code is 405 (Method Not Allowed) or the expected code for GET requests
    assert response['statusCode'] == 405