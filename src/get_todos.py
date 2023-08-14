import boto3
import json
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TODO') 
    query = event['queryStringParameters']
    limit = int(query.get('limit', 10))
    done = query.get('done', False)
    deleted = query.get('deleted', False)
    last_evaluated_key_id = query.get('last_evaluated_key', None)
    
    filter_expression = 'done = :done AND deleted = :deleted'
    expression_attribute_values = {
        ':done': done,
        ':deleted': deleted
    }
    
    # If last_evaluated_key_id is present, use it as ExclusiveStartKey
    exclusive_start_key = None
    if last_evaluated_key_id is not None:
        exclusive_start_key = {
            'id': last_evaluated_key_id
        }
    
    # Perform the scan operation
    scan_kwargs = {
        'Limit': limit, 
        'FilterExpression': filter_expression,
        'ExpressionAttributeValues': expression_attribute_values
    }
    
    if exclusive_start_key:
        scan_kwargs['ExclusiveStartKey'] = exclusive_start_key
    try:
        response = table.scan(**scan_kwargs)
    except ClientError as e:
        e.response['Query'] = scan_kwargs
        raise e
    return {
        "statusCode": 200,
        "body": json.dumps({
            "items": response['Items'],
            "last_evaluated_key": response.get('LastEvaluatedKey'),
            "message": "Todos retrieved successfully!"
        })
    }
