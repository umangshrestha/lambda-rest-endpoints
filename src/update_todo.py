import boto3
import json
from utils.timestamp import get_date_string


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

    body = event['body']
    body["title"] = body.get("title", "")
    body["description"] = body.get("description", "")
    body["done"] = body.get("done", False)
    body["deleted"] = body.get("deleted", False)
    
    update_expression = 'SET title = :title, done = :done, deleted = :deleted, deletedAt = :deletedAt, updatedAt = :updatedAt, completedAt = :completedAt, description = :description'
    expression_attribute_values = {
        ':title': body["title"],
        ':description': body["description"],
        ':done': body["done"],
        ':deleted': body["deleted"],
        ':deletedAt': get_date_string() if body["deleted"] else None,
        ':updatedAt': get_date_string(),
        ':completedAt': get_date_string() if body["done"] else None
    }
    table.update_item(
        Key={
            'id': item_id
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Todo updated successfully!"
        })
    }
    