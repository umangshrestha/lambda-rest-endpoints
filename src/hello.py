import json

def lambda_handler(event, context):
    name = event['pathParameters'].get('name', 'World')
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Hello, {name}!"
        }),
    }
