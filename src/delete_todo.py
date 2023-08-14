import boto3
import json


def lambda_handler(event, context):
    item_id = event['pathParameters']['id']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TODO')    

    item = table.get_item(Key={'id': item_id})
    if 'Item' not in item:
        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Todo not found!"
            })
        }

    table.delete_item(
        Key={
            'id': item_id
        }
    )
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Todo deleted successfully!"
        })
    }
    