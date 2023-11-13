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
    
    # Get the DynamoDB table name from environment variables
    table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'visitCounter')
    table = dynamodb.Table(table_name)
    
    try:
        visit_count = update_visit_count(table)
        
        response = {
            "isBase64Encoded": False,
            'statusCode': 200,
            'headers': {
                "content-type": "application/json",
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': str(visit_count)
        }
        
        # Log successful update
        logger.info("Successfully updated visit count")
        
    except Exception as e:
        # Log the error and re-raise the exception
        logger.error("Lambda execution failed: %s", str(e))
        return {
            "isBase64Encoded": False,
            'statusCode': 500,
            'body': "Internal Server Error"
        }

    return response
