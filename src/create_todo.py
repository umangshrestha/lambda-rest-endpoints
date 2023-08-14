import json
import boto3
from botocore.errorfactory import ClientError
from uuid import uuid4 as uuid

from utils.timestamp import get_date_string


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TODO')
    data = {}
    body = event['body']
    data["id"] = body.get("id", str(uuid()))
    data["title"] = body.get("title", "")
    data["description"] = body.get("description", "")
    data["done"] = body.get("done", False)
    data["deleted"] = body.get("deleted", False)
    data["createdAt"] = get_date_string()
    data["updatedAt"] = get_date_string()
    data["deletedAt"] = get_date_string() if body.get("deleted", False) else None
    try:
        table.put_item(Item=data, ConditionExpression='attribute_not_exists(id)')
        return {
            "statusCode": 201,
            "body": json.dumps({
                "id": data["id"],
                "message": "Todo created successfully!",
            }),
        }
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return {
                "statusCode": 409,
                "body": json.dumps({
                    "error": "Todo already exists!"
                }),
            }
        else:
            raise