import boto3
import json


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TODO') 
    item_id = event['pathParameters']['id']
    item = table.get_item(Key={'id': item_id})
    if 'Item' not in item:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Todo not found!"
            })
        }
    return {
        "statusCode": 200,
        "body": json.dumps(item['Item'])
    }
