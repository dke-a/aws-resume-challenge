import json
import boto3

def lambda_handler(event,context):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('visitCounter')

    # response = table.update_item(
    #     Key={
    #       'id':'counter'
    #     },
    #     UpdateExpression='SET visit_count = visit_count + :i',
    #     ExpressionAttributeValues={
    #         ':i':1
    #     },
    #     ReturnValues='UPDATED_NEW'
    # )
    # print(response)
    
    # apiResponse = {
    #     "body": response['Attributes']['visit_count']
    # }
    
    
    # const response = {
    #     statusCode: 200,
    #     headers: {
    #         "Access-Control-Allow-Headers" : "Content-Type",
    #         "Access-Control-Allow-Origin": "https://www.example.com",
    #         "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
    #     },
    #     body: JSON.stringify('Hello from Lambda!'),
    # };
    # return response;
    
    
    try:
        response = table.update_item(
        Key={
          'id':'counter'
        },
        UpdateExpression='SET visit_count = visit_count + :i',
        ExpressionAttributeValues={
            ':i':1
        },
        ReturnValues='UPDATED_NEW')
        
        # response['headers'] = { 
        #     "Access-Control-Allow-Headers" : "Content-Type",
        #     "Access-Control-Allow-Origin": "https://www.donangeles.com",
        #     "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        # };
        
        # response['ResponseMetadata']['HTTPHeaders'] = {
        #     "Access-Control-Allow-Headers" : "Content-Type",
        #     "Access-Control-Allow-Origin": "https://www.donangeles.com",
        #     "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
        # }
        
        # response['ResponseMetadata']['HTTPHeaders']['Access-Control-Allow-Headers'] = "content-type"
        # response['ResponseMetadata']['HTTPHeaders']['Access-Control-Allow-Origin'] = "*"
        # response['ResponseMetadata']['HTTPHeaders']['Access-Control-Allow-Methods'] = "OPTIONS,POST,GET"
        
        response = {
        "isBase64Encoded": False,
        'statusCode': 200,
        'headers': {
            "content-type": "application/json",
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': response['Attributes']['visit_count']
        }
    
        
    except ClientError as err:
        logger.error(
            "Couldn't update count %s. Here's why: %s: %s",
            title,
            err.response['Error']['Code'], err.response['Error']['Message'])
        raise
    else:
        return response#['ResponseMetadata']#['HTTPHeaders']#['Attributes']#['visit_count']


    
    # return apiResponse['body']
    
#https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-cors.html
#https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
#https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html
