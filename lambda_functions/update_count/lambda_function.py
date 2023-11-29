import json
import os
import boto3
import logging

# Initialize a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Function to update the visit count in DynamoDB
def update_visit_count(table):
    try:
        response = table.update_item(
            Key={
                'id': 'counter'
            },
            UpdateExpression='SET visit_count = visit_count + :i',
            ExpressionAttributeValues={
                ':i': 1
            },
            ReturnValues='UPDATED_NEW')
        
        return response['Attributes']['visit_count']
    except Exception as e:
        # Log the error and re-raise the exception
        logger.error("Error updating visit count: %s", str(e))
        raise

# Lambda handler function
def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'visitCounter')
    table = dynamodb.Table(table_name)

    # Check if the request is a POST request
    if event['requestContext']['http']['method'] == 'POST':
        try:
            visit_count = update_visit_count(table)
            body = str(visit_count)
            statusCode = 200
            logger.info("Successfully updated visit count")
        except Exception as e:
            logger.error("Lambda execution failed: %s", str(e))
            body = "Internal Server Error"
            statusCode = 500
    else:
        # If not a POST request, return a 405 Method Not Allowed response
        body = "Method Not Allowed"
        statusCode = 405

    response = {
        "isBase64Encoded": False,
        'statusCode': statusCode,
        'headers': {
            "content-type": "application/json",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': body
    }

    return response

